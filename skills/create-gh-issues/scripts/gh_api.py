"""Gói `gh api` của skill: REST và GraphQL qua phiên `gh` đã đăng nhập — không đọc, không in, không lưu token.

Nhịp: lệnh tạo nội dung (REST POST/PATCH/PUT/DELETE, GraphQL mutation) ≤ `gioi_han_phut`/phút (mặc định 40) và
≤ `gioi_han_gio`/giờ (mặc định 450) theo cửa sổ trượt; cứ
`kiem_diem_moi` lệnh thì đọc `rate_limit`, điểm còn dưới `diem_toi_thieu` thì chờ tới giờ đặt lại.
Thử lại: 403/429 do trần tốc độ → chờ `retry-after` (không có thì 60 giây) nhân đôi mỗi lần, quá `so_lan_thu` thì DungLoat;
bị chặn quá `chan_toi_da_gio` lần trong một giờ → DungLoat (dừng cả loạt). 5xx, hết giờ chờ, mất mạng: lệnh thường thử lại;
lệnh TẠO trả KHONG_RO để bên gọi hoà map trước rồi mới quyết tạo lại (không tạo trùng). 403 không phải trần tốc độ, 404, 422
→ LoiGh ngay. Nhật ký JSONL mỗi lần gọi: {ts, op, path, status, points_remaining, resource, lan} — không thân, không token.
`dry_run=True`: ghi lại lệnh vào `goi`, không chạy `gh`, trả kết quả giả từ `gia_lap(op, args, body)`.
"""
import json
import subprocess
import time
from collections import deque
from datetime import datetime
from pathlib import Path

from gh_api_loi import KHONG_RO, DungLoat, LoiGh, PhanHoi, chay_gh, tach, thong_diep  # noqa: F401 (tái xuất)


class GhClient:
    def __init__(self, runner=chay_gh, clock=time.monotonic, sleep=time.sleep, now=time.time, dry_run=False, gia_lap=None,
                 log_path: Path | None = None, gioi_han_phut=40, gioi_han_gio=450, kiem_diem_moi=50, diem_toi_thieu=200,
                 chan_toi_da_gio=3, so_lan_thu=5, timeout=60.0):
        self.runner, self.clock, self.sleep, self.now = runner, clock, sleep, now
        self.dry_run, self.gia_lap, self.log_path = dry_run, gia_lap, log_path
        self.gioi_han_phut, self.gioi_han_gio = gioi_han_phut, gioi_han_gio
        self.kiem_diem_moi, self.diem_toi_thieu = kiem_diem_moi, diem_toi_thieu
        self.chan_toi_da_gio, self.so_lan_thu, self.timeout = chan_toi_da_gio, so_lan_thu, timeout
        self.ghi_gan: deque = deque()   # mốc giờ các lệnh tạo nội dung trong một giờ qua
        self.bi_chan: deque = deque()   # mốc giờ các lần bị chặn 403/429
        self.goi: list[dict] = []       # dry-run: lệnh đã ghi lại
        self.dem = 0

    def dat_log(self, path: Path | None) -> None:
        self.log_path = path

    # ---------- gọi ----------
    def rest(self, method: str, path: str, body=None, tao=False, op: str | None = None):
        args = [path] + ([] if method == "GET" else ["-X", method])
        stdin = None if body is None else json.dumps(body, ensure_ascii=False)
        if stdin is not None:
            args += ["--input", "-"]
        return self._goi(op or f"{method} {path.split('?')[0]}", args, stdin, tao=tao, ghi=method != "GET",
                         graphql=False, body=body)

    def graphql(self, query: str, variables: dict, op: str, ghi=False) -> dict:
        body = {"query": query, "variables": variables}
        r = self._goi(op, ["graphql", "--input", "-"], json.dumps(body, ensure_ascii=False), tao=False, ghi=ghi,
                      graphql=True, body=body)
        return (r.json or {}).get("data") or {}

    def _goi(self, op, args, stdin, tao, ghi, graphql, body):
        if self.dry_run:
            self.goi.append({"op": op, "path": args[0], "ghi": ghi, "tao": tao})
            return self.gia_lap(op, args, body) if self.gia_lap else PhanHoi(200, {}, {})
        self._kiem_diem()
        status = None
        for lan in range(1, self.so_lan_thu + 1):
            if ghi:
                self._cho_nhip()
            try:
                _, out, err = self.runner(args, stdin, self.timeout)
                status, headers, data = tach(out)
            except subprocess.TimeoutExpired:
                status, headers, data, err = None, {}, None, "hết giờ chờ"
            except OSError as e:  # không có `gh` trên PATH: lỗi cấu hình, không thử lại
                raise LoiGh(None, op, f"không chạy được gh: {e}") from e
            self._log(op, args[0], status, headers, lan)
            loi_gql = graphql and isinstance(data, dict) and data.get("errors")
            if status is not None and 200 <= status < 300 and not loi_gql:
                return PhanHoi(status, headers, data)
            cho = self._cho_khi_chan(status, headers, data, lan)
            if cho is not None:
                self._dem_chan(op)
            elif status is None or status >= 500:
                if tao:
                    return KHONG_RO
                cho = min(60, 5 * 2 ** (lan - 1))
            else:
                raise LoiGh(status, op, thong_diep(data, err))
            if lan < self.so_lan_thu:  # lần cuối không chờ vô ích
                self.sleep(cho)
        raise DungLoat(status, op, f"hết {self.so_lan_thu} lần thử")

    # ---------- nhịp và trần ----------
    def _cho_nhip(self) -> None:
        while True:
            t = self.clock()
            while self.ghi_gan and t - self.ghi_gan[0] >= 3600:
                self.ghi_gan.popleft()
            phut = [x for x in self.ghi_gan if t - x < 60]
            if len(phut) >= self.gioi_han_phut:
                self.sleep(60 - (t - phut[0]) + 0.01)
            elif len(self.ghi_gan) >= self.gioi_han_gio:
                self.sleep(3600 - (t - self.ghi_gan[0]) + 0.01)
            else:
                self.ghi_gan.append(t)
                return

    def _cho_khi_chan(self, status, headers, data, lan) -> float | None:
        """Số giây phải chờ nếu đây là chặn do trần tốc độ; None nếu không phải."""
        gql_chan = isinstance(data, dict) and any(isinstance(e, dict) and e.get("type") == "RATE_LIMITED"
                                                  for e in data.get("errors") or [])
        if status not in (403, 429) and not gql_chan:
            return None
        if "retry-after" in headers:
            return min(3600.0, float(headers["retry-after"]) * 2 ** (lan - 1))
        if headers.get("x-ratelimit-remaining") == "0" and headers.get("x-ratelimit-reset"):
            return max(1.0, float(headers["x-ratelimit-reset"]) - self.now()) + 1
        if status == 429 or gql_chan or "rate limit" in thong_diep(data).lower():
            return min(3600.0, 60.0 * 2 ** (lan - 1))
        return None  # 403 vì quyền: không thử lại

    def _dem_chan(self, op: str) -> None:
        t = self.clock()
        self.bi_chan.append(t)
        while self.bi_chan and t - self.bi_chan[0] >= 3600:
            self.bi_chan.popleft()
        if len(self.bi_chan) > self.chan_toi_da_gio:
            raise DungLoat(403, op, f"bị chặn {len(self.bi_chan)} lần trong một giờ — dừng cả loạt, chờ một giờ, báo điều phối")

    def _kiem_diem(self) -> None:
        self.dem += 1
        if self.kiem_diem_moi <= 0 or (self.dem - 1) % self.kiem_diem_moi:
            return
        try:
            _, out, _ = self.runner(["rate_limit"], None, self.timeout)
        except subprocess.TimeoutExpired:
            return
        except OSError as e:
            raise LoiGh(None, "rate_limit", f"không chạy được gh: {e}") from e
        status, headers, data = tach(out)
        if status != 200 or not isinstance(data, dict):
            return
        res = data.get("resources") or {}
        for ten in ("graphql", "core"):
            r = res.get(ten) or {}
            self._log("rate_limit", ten, status, {"x-ratelimit-remaining": r.get("remaining"), "x-ratelimit-resource": ten}, 1)
            if r.get("remaining") is not None and r["remaining"] < self.diem_toi_thieu:
                self.sleep(max(1.0, float(r.get("reset", 0)) - self.now()) + 5)

    def _log(self, op, path, status, headers, lan) -> None:
        if not self.log_path:
            return
        con = headers.get("x-ratelimit-remaining")
        dong = {"ts": datetime.fromtimestamp(self.now()).isoformat(timespec="seconds"), "op": op,
                "path": str(path).split("?")[0], "status": status,
                "points_remaining": int(con) if str(con or "").isdigit() else con,
                "resource": headers.get("x-ratelimit-resource"), "lan": lan}
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dong, ensure_ascii=False) + "\n")

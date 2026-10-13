"""Lệnh `push`: đẩy seed theo lô epic — issue → item Project → field → sub-issue (cha trước con), chạy lại an toàn.

  --dry-run      ghi lại lệnh, không chạy lệnh ghi nào, không ghi map; in số lệnh theo loại và giờ ước theo nhịp
  --cap-nhat     khoá đã có trong map mà băm (title, thân, nhãn) khác seed → PATCH issue, đặt lại nhãn
  --chi-field    chỉ đặt lại field Project cho khoá đã có item
  --ghi-than     (chỉ đi với --dry-run) ghi thân từng khoá vào <than-dir>/ để gate của dự án quét trước khi đăng
  --da-quet      người chạy xác nhận thân ở <than-dir>/ đã qua gate quét của dự án — lượt thật bắt buộc có cờ này
  --lenh-quet    (lặp được) lệnh gate chạy lại ngay trước khi đăng, phải thoát 0
Lượt thật từ chối khi thiếu --da-quet, thân sắp đăng khác bản ở <than-dir>/, hoặc một --lenh-quet không thoát 0.
Mỗi lô in: «<epic>: tạo mới N · nhận lại M · lỗi K · bước dở J». Cờ <evidence-dir>/PUSH_RUNNING đặt khi chạy, gỡ trong finally.
"""
import os
import shlex
import subprocess
from collections import Counter

import cau_hinh as ch
from ban_do import doc_map, ghi_map, hoa_map, liet_ke_issue
from day_buoc import Day, Viec, xong
from gh_api import DungLoat, GhClient, LoiGh, PhanHoi
from lib import LoiBoSinh, chan_khi_co, doc_yaml
from seed_doc import TANG, cac_ban_ghi, doc_seed, tieu_de
from than_issue import nap_ctx, than


class GiaLap:
    """Kết quả giả cho dry-run: số issue 900001… để không lẫn với số thật."""
    def __init__(self):
        self.n = 900000

    def __call__(self, op, args, body):
        self.n += 1
        if op == "tao-issue":
            return PhanHoi(201, {}, {"number": self.n, "id": -self.n, "node_id": f"DRY_I_{self.n}", "html_url": None})
        if op == "addProjectV2ItemById":
            return PhanHoi(200, {}, {"data": {"addProjectV2ItemById": {"item": {"id": f"DRY_PVTI_{self.n}"}}}})
        return PhanHoi(200, {}, {"data": {}})


def dung_viec(seed: dict, lo: str, team: dict, ids: dict, chon, ctx) -> list[Viec]:
    """Việc của một lô theo tầng: epic → story/điều tra → leaf, giữ thứ tự seed trong mỗi tầng. Thân hỏng → dừng cả lô."""
    if lo not in seed:
        raise LoiBoSinh(f"không có lô {lo} trong seed (có: {', '.join(sorted(seed))})")
    ds = sorted((it for _, it in cac_ban_ghi({lo: seed[lo]})), key=lambda it: TANG[it["tracker"]])
    return [Viec(it["key"], it.get("cha"), tieu_de(it["tracker"], it["key"], it["title_vi"]), than(it["key"], ctx),
                 list(it["labels"]), ch.lenh_field(it, team, ids, chon)) for it in ds]


def ghi_than(viec: list[Viec], thu_muc) -> int:
    thu_muc.mkdir(parents=True, exist_ok=True)
    for v in viec:
        (thu_muc / ch.ten_file_than(v.key)).write_text(v.body + "\n", encoding="utf-8")
    return len(viec)


def kiem_than_da_quet(viec: list[Viec], cfg, a) -> list[str]:
    """Chặn đăng thân chưa quét: cần --da-quet, thân trùng byte bản ở <than-dir>/, mọi --lenh-quet thoát 0."""
    loi = [] if a.da_quet else ["thiếu --da-quet: chạy --dry-run --ghi-than, quét <than-dir> bằng gate của dự án, rồi chạy lại"]
    for v in viec:
        p = cfg.than_dir / ch.ten_file_than(v.key)
        if not p.is_file() or p.read_text(encoding="utf-8").rstrip("\n") != v.body:
            loi.append(f"{v.key}: thân chưa ghi hoặc khác {p} — chạy --dry-run --ghi-than rồi quét lại")
    for lenh in a.lenh_quet or []:
        r = subprocess.run(shlex.split(lenh), capture_output=True, text=True)
        if r.returncode != 0:
            loi.append(f"--lenh-quet «{lenh}» chưa PASS (exit {r.returncode}): {(r.stdout or r.stderr).strip().splitlines()[:1]}")
    return loi


def tom_tat(lo: str, d: Day, viec: list[Viec], m: dict, chua_toi: int) -> str:
    do = sum(1 for v in viec if v.key in m and not xong(m[v.key]))
    s = f"{lo}: tạo mới {d.dem.tao_moi} · nhận lại {d.dem.nhan_lai} · lỗi {d.dem.loi} · bước dở {do}"
    s += f" · cập nhật {d.dem.cap_nhat}" if d.dem.cap_nhat else ""
    s += f" · lệch seed chưa đẩy {d.dem.lech} (chạy lại với --cap-nhat)" if d.dem.lech else ""
    return s + (f" · chưa tới {chua_toi}" if chua_toi else "")


def gio_uoc(so_ghi: int, phut: int = 40, gio: int = 450) -> str:
    uoc = (so_ghi // gio) * 60 + (so_ghi % gio) / phut
    return f"{so_ghi} lệnh ghi ≈ {uoc:.1f} phút theo nhịp {phut}/phút, {gio}/giờ (chưa tính thời gian phản hồi)"


def chay(a, cfg, client=None, doc_client=None, kiem_quet=kiem_than_da_quet) -> int:
    seed, team = doc_seed(cfg.backlog), doc_yaml(cfg.team)
    chon = tuple(x.strip() for x in a.field.split(",") if x.strip())
    fl = ch.doc_field_list(cfg, doc_client or GhClient(log_path=cfg.log_dir / "field-list.jsonl", kiem_diem_moi=0),
                           a.doc_lai_field)
    ids, pid, ctx = ch.field_ids(fl), ch.project_id(fl), nap_ctx(cfg)
    cac_lo = [x.strip() for x in a.lo.split(",") if x.strip()]
    viec = {lo: dung_viec(seed, lo, team, ids, chon, ctx) for lo in cac_lo}
    if a.ghi_than:
        print(f"ghi thân: {sum(ghi_than(v, cfg.than_dir) for v in viec.values())} file → {cfg.than_dir}")
    if not a.dry_run and not a.chi_field and (loi := kiem_quet([v for ds in viec.values() for v in ds], cfg, a)):
        print("TỪ CHỐI ĐĂNG (thân chưa quét):\n  - " + "\n  - ".join(loi[:20])
              + (f"\n  … và {len(loi) - 20} dòng nữa" if len(loi) > 20 else ""))
        return 1
    client = client or GhClient(dry_run=a.dry_run, gia_lap=GiaLap(), gioi_han_phut=cfg.nhip_phut, gioi_han_gio=cfg.nhip_gio)
    m = doc_map(cfg.map_file)
    luu = (lambda: None) if a.dry_run else (lambda: ghi_map(cfg.map_file, m))
    seed_cha = {it["key"]: it.get("cha") for _, it in cac_ban_ghi(seed)}
    if nhan := hoa_map(m, None if a.dry_run else liet_ke_issue(client, cfg.repo), seed_cha):
        luu()
        print(f"hoà map: nhận {nhan} khoá đã có issue trên GitHub mà map chưa ghi")
    uoc = lambda goi: gio_uoc(sum(1 for g in goi if g["ghi"]), cfg.nhip_phut, cfg.nhip_gio)  # noqa: E731
    for lo in cac_lo:
        bat_dau = len(client.goi)
        client.dat_log(None if a.dry_run else cfg.log_dir / f"{lo}.jsonl")
        d = Day(client, cfg.repo, pid, team["assignee"], m, luu, seed_cha, cap_nhat=a.cap_nhat)
        dung, lam = None, d.chi_field if a.chi_field else d.day
        for i, v in enumerate(viec[lo]):
            try:
                lam(v)
            except (LoiBoSinh, LoiGh) as e:
                d.dem.loi += 1
                dung = (i, e)
                break
        chua_toi = len(viec[lo]) - dung[0] - 1 if dung else 0
        if a.chi_field:
            print(f"{lo} (--chi-field): đặt field {len(viec[lo]) - chua_toi - d.dem.loi} khoá · lỗi {d.dem.loi}")
        else:
            print(tom_tat(lo, d, viec[lo], m, chua_toi))
        if a.dry_run:
            dem = Counter(g["op"] for g in client.goi[bat_dau:])
            print(f"  dry-run {lo}: {len(viec[lo])} khoá · " + " · ".join(f"{k} {n}" for k, n in sorted(dem.items()))
                  + f" · {uoc(client.goi[bat_dau:])}")
        if dung:
            loai = "DỪNG CẢ LOẠT (trần tốc độ)" if isinstance(dung[1], DungLoat) else "DỪNG"
            print(f"  {loai} ở {viec[lo][dung[0]].key}: {dung[1]} — map đã ghi tới bước cuối cùng xong")
            return 1
    if a.dry_run:
        print(f"dry-run tổng: {uoc(client.goi)} · không chạy lệnh ghi nào, nhận lại tính theo board-map.json")
    return 0


def main(a, cfg) -> int:
    cfg.can("repo", "seed_dir", "evidence_dir", "project_owner", "project_number")
    if a.ghi_than and not a.dry_run:
        print("TỪ CHỐI: --ghi-than chỉ đi với --dry-run (ghi thân → quét bằng gate của dự án → mới đăng)")
        return 2
    chan_khi_co(cfg.co_chan)
    if cfg.co_push.exists():
        print(f"TỪ CHỐI: {cfg.co_push} đang có — lượt đẩy khác đang chạy hoặc chết dở; kiểm rồi gỡ cờ tay")
        return 3
    cfg.evidence_dir.mkdir(parents=True, exist_ok=True)
    cfg.co_push.write_text(str(os.getpid()), encoding="utf-8")
    try:
        return chay(a, cfg)
    except LoiGh as e:
        print(f"✗ GitHub: {e} — map đã ghi tới bước cuối cùng xong")
        return 1
    finally:
        cfg.co_push.unlink(missing_ok=True)

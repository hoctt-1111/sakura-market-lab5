"""Phần không trạng thái của gói `gh api`: lỗi, kết quả, gọi tiến trình `gh api -i`, tách header/thân, lấy lời báo lỗi."""
import json
import re
import subprocess
from dataclasses import dataclass, field


class LoiGh(Exception):
    def __init__(self, status, op: str, thong_diep: str):
        super().__init__(f"{op}: HTTP {status} — {thong_diep}")
        self.status, self.op, self.thong_diep = status, op, thong_diep


class DungLoat(LoiGh):
    """Trần tốc độ chặn quá ngưỡng — dừng cả loạt, giữ map, báo điều phối."""


class _KhongRo:
    def __repr__(self) -> str:
        return "KHONG_RO"


KHONG_RO = _KhongRo()  # lệnh tạo không rõ kết quả: bên gọi phải hoà map trước khi tạo lại


@dataclass
class PhanHoi:
    status: int
    headers: dict = field(default_factory=dict)
    json: object = None


def chay_gh(args: list[str], stdin: str | None, timeout: float) -> tuple[int, str, str]:
    p = subprocess.run(["gh", "api", "-i", *args], input=stdin, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def tach(stdout: str) -> tuple[int | None, dict, object]:
    """Đầu ra `gh api -i` → (mã HTTP, header chữ thường, thân JSON). Không có dòng trạng thái (mất mạng) → (None, {}, None)."""
    m = re.match(r"HTTP/\S+ (\d{3})", stdout or "")
    if not m:
        return None, {}, None
    dau, than = _chia(stdout)
    headers = {}
    for dong in dau.splitlines()[1:]:
        k, _, v = dong.partition(":")
        headers[k.strip().lower()] = v.strip()
    try:
        data = json.loads(than) if than.strip() else None
    except ValueError:
        data = than
    return int(m.group(1)), headers, data


def _chia(s: str) -> tuple[str, str]:
    """(phần header, phần thân) — tách ở dòng trống đầu tiên."""
    p = re.split(r"\r?\n\r?\n", s, maxsplit=1)
    return p[0], (p[1] if len(p) > 1 else "")


def thong_diep(data, err: str = "") -> str:
    if isinstance(data, dict):
        if data.get("errors"):
            return "; ".join(str(e.get("message", e)) for e in data["errors"])[:300]
        if data.get("message"):
            return str(data["message"])[:300]
    return (err or str(data or "")).strip()[:300]

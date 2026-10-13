"""Hàm dùng chung của skill create-gh-issues: lỗi dữ liệu, đọc/ghi YAML và JSON, ghi nguyên tử, cờ chặn, khuôn in kết quả kiểm.

Không có đường dẫn cố định: mọi file đến từ tham số dòng lệnh hoặc file cấu hình (xem cau_hinh.py).
"""
import json
import os
import re
from pathlib import Path

import yaml

CO_MIEN = "BREAK_TEST_CHU_CO"  # tiến trình do bộ phá thử của dự án chạy (=1) được miễn cờ chặn


class LoiBoSinh(Exception):
    """Lỗi dữ liệu — thông báo nêu đường dẫn hoặc khoá để người đọc sửa đúng chỗ."""


def chuan(s: str) -> str:
    """Bỏ mọi khoảng trắng — so khớp không phụ thuộc xuống dòng."""
    return re.sub(r"\s+", "", s)


def doc_yaml(path):
    p = Path(path)
    if not p.is_file():
        raise LoiBoSinh(f"thiếu file nguồn: {p}")
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise LoiBoSinh(f"{p}: yaml hỏng — {e}") from e


def doc_yaml_neu_co(path, mac_dinh=None):
    """Như doc_yaml nhưng thiếu file thì trả `mac_dinh` (file tuỳ chọn: premise.yaml, gaps.yaml)."""
    return doc_yaml(path) if Path(path).is_file() else mac_dinh


def ghi_yaml(path, data) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=10**6), encoding="utf-8")


def doc_json(path, mac_dinh=None):
    p = Path(path)
    if not p.is_file():
        if mac_dinh is not None:
            return mac_dinh
        raise LoiBoSinh(f"thiếu {p}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError as e:
        raise LoiBoSinh(f"{p}: JSON hỏng — {e}") from e


def ghi_json_nguyen_tu(path, data) -> None:
    """Ghi file tạm cùng thư mục rồi đổi tên: rớt giữa chừng thì bản cũ còn nguyên."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_name(p.name + ".tmp")
    tam.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tam, p)


def chan_khi_co(cac_co) -> None:
    """Còn một cờ chặn (vd. `<evidence-dir>/BREAK_RUNNING`) thì dừng: tiến trình khác đang sửa tạm nguồn chung."""
    if os.environ.get(CO_MIEN) == "1":
        return
    for co in cac_co or []:
        if Path(co).exists():
            raise LoiBoSinh(f"cờ chặn {co} đang có — tiến trình khác đang sửa tạm nguồn chung; đợi gỡ cờ")


class KetQua:
    """Gom vi phạm của một phép kiểm, in một lần: `✗ <ten>  FAIL (N vi phạm)` + từng dòng, hoặc `✓ <ten>  PASS`."""

    def __init__(self, ten: str, mo_ta: str, goc: Path | None = None):
        self.ten, self.mo_ta, self.goc = ten, mo_ta, goc
        self.loi: list[str] = []
        self.ghi_chu: list[str] = []  # dòng tóm tắt in sau dòng PASS/FAIL (không phải vi phạm)

    def vi_pham(self, path, dong, chi_tiet: str) -> None:
        loc = str(path)
        if isinstance(path, Path) and self.goc and self.goc in path.parents:
            loc = str(path.relative_to(self.goc))
        self.loi.append(f"{loc}:{dong} {chi_tiet}" if dong is not None else f"{loc} {chi_tiet}")

    def in_ra(self) -> bool:
        """In kết quả, trả True khi PASS."""
        if self.loi:
            print(f"✗ {self.ten}  FAIL ({len(self.loi)} vi phạm)")
            for dong in self.loi:
                print(f"  - {dong}")
        else:
            print(f"✓ {self.ten}  PASS")
        for g in self.ghi_chu:
            print(g)
        return not self.loi

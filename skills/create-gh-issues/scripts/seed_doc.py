"""Quy ước seed của skill (docs/seed-schema.md): tracker, tiền tố title, loại leaf; đọc `backlog/*.yaml` theo thứ tự tên.

Title = `<TIỀN TỐ> <key> <title_vi>`; key là từ thứ hai, khớp `^\\[[A-Z ]+\\] (\\S+) ` — push, snapshot, check đều tìm
issue theo key trong title, nên key duy nhất toàn backlog và không đổi sau lần đẩy đầu.
"""
import re
from pathlib import Path

import yaml

from lib import LoiBoSinh

TIEN_TO = {"epic": "[EPIC]", "story": "[STORY]", "devtask": "[DEV TASK]", "testdesign": "[TEST DESIGN]",
           "investigation": "[INVESTIGATION]"}
TANG = {"epic": 0, "story": 1, "investigation": 1, "devtask": 2, "testdesign": 2}  # thứ tự đẩy: cha trước con
LEAF_LOAI = ("FE", "BE", "DB", "TEST", "INFRA")
LEAF_TRACKER = {"FE": "devtask", "BE": "devtask", "DB": "devtask", "INFRA": "devtask", "TEST": "testdesign"}
VAN = ("mo_ta", "pham_vi", "luong_chinh", "tieu_chi_nghiem_thu", "dinh_nghia_xong")
MANG_THEO = VAN + ("gap_refs", "premise_refs")  # trường người viết; `check --so` không so các trường này
REF_GOC = ("sc", "api", "tech", "bang", "fr", "adr", "nfr")
REF_THEM = ("khuon", "ac", "sd", "hoi")
TITLE_RE = re.compile(r"^\[[A-Z ]+\] (\S+) ")


def tieu_de(tracker: str, key: str, title_vi: str) -> str:
    return f"{TIEN_TO[tracker]} {key} {title_vi}"


def khoa_tu_title(title: str) -> str | None:
    m = TITLE_RE.match(title or "")
    return m.group(1) if m else None


def la_leaf(key: str) -> bool:
    return "/" in key and key.rsplit("/", 1)[1] in LEAF_LOAI


def doc_seed(thu_muc: Path) -> dict[str, dict]:
    """{tên file (không đuôi): nội dung} theo thứ tự tên. YAML hỏng → dừng (LoiBoSinh)."""
    thu_muc = Path(thu_muc)
    if not thu_muc.is_dir():
        raise LoiBoSinh(f"thiếu thư mục seed: {thu_muc}")
    ra = {}
    for p in sorted(thu_muc.glob("*.yaml")):
        try:
            ra[p.stem] = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            raise LoiBoSinh(f"{p}: yaml hỏng — {e}") from e
    return ra


def cac_ban_ghi(seed: dict) -> list[tuple[str, dict]]:
    """[(tên file, bản ghi)] gồm epic và items, theo thứ tự file."""
    return [(f, it) for f, d in seed.items() for it in [d.get("epic") or {}] + list(d.get("items") or [])]

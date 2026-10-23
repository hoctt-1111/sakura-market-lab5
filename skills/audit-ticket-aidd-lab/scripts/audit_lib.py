"""Hàm dùng chung của skill audit-ticket-aidd-lab: đọc tệp, khoá và tracker từ tiêu đề, bản thay thế, phát hiện.
Khuôn tiêu đề `[TRACKER] KHOÁ …` và luật bản thay thế (đóng + nhãn thay thế) theo cấu hình, không viết cứng."""
import json
import re
from pathlib import Path

import yaml


class LoiBoSinh(Exception):
    """Lỗi đầu vào (tệp thiếu, hỏng, cấu hình sai) — dừng có thông báo, không traceback."""


def _doc_tep(p, phan_tich, loi_hong, ten_dang: str):
    """Đọc tệp văn bản rồi phân tích; tệp thiếu hoặc hỏng → LoiBoSinh."""
    p = Path(p)
    if not p.is_file():
        raise LoiBoSinh(f"thiếu tệp: {p}")
    try:
        return phan_tich(p.read_text(encoding="utf-8"))
    except loi_hong as e:
        raise LoiBoSinh(f"{p}: {ten_dang} hỏng — {e}") from e


def doc_yaml(p) -> dict:
    return _doc_tep(p, lambda s: yaml.safe_load(s) or {}, yaml.YAMLError, "yaml")


def doc_json(p) -> dict:
    return _doc_tep(p, json.loads, json.JSONDecodeError, "json")


def ghi_text(p, noi_dung: str) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_suffix(p.suffix + ".tam")
    tam.write_text(noi_dung, encoding="utf-8")
    tam.replace(p)


def khoa_tu_title(title: str, cfg: dict) -> str | None:
    m = re.match(cfg["tieu_de_re"], title or "")
    return m.group(1) if m else None


def tracker_tu_title(title: str, cfg: dict) -> str | None:
    m = re.match(r"^(\[[A-Z ]+\])", title or "")
    nguoc = {v: k for k, v in cfg["tracker_tien_to"].items()}
    return nguoc.get(m.group(1)) if m else None


def la_ban_thua(item: dict, cfg: dict) -> bool:
    return str(item.get("state")).upper() == "CLOSED" and cfg["nhan_thay_the"] in (item.get("labels") or [])


def hau_to(khoa: str | None) -> str | None:
    return khoa.rsplit("/", 1)[1] if khoa and "/" in khoa else None


def story_cua_la(khoa: str | None) -> str | None:
    return khoa.rsplit("/", 1)[0] if khoa and "/" in khoa else None


def ph(ma: str, item: dict | None, ly_do: str, khoa: str | None = None) -> dict:
    """Một phát hiện. `item` None khi phát hiện gắn nhóm (Owner × Sprint) hoặc khoá không có issue."""
    return {"ma": ma, "so": item["so"] if item else None, "khoa": khoa, "title": (item or {}).get("title") or khoa or "",
            "ly_do": ly_do}

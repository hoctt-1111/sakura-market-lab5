"""Thứ tự mục của thân issue theo loại (epic, story, investigation, FE, BE, DB, INFRA, TEST), đọc từ khuôn Markdown.

Khuôn (`--khuon`, mẫu ở templates/khuon-issue.md): mỗi tiêu đề `### …` mở một loại, bảng ngay dưới có cột đầu là tên mục,
từ trên xuống là thứ tự trong thân. Loại nhận từ phần tiêu đề trước dấu «—»: có «(leaf A / B …)» thì là các loại leaf đó,
không thì là từ Epic / Story / Investigation. Khuôn được bỏ bớt hay đổi chỗ mục; mục lạ (bộ dựng không biết) → LoiBoSinh.
Không có khuôn → MAC_DINH (trùng thứ tự của templates/khuon-issue.md).
"""
import re
from pathlib import Path

from lib import LoiBoSinh

_LEAF = ["Mô tả", "Tiêu chí nghiệm thu", "Định nghĩa xong", "Dữ liệu từ spec", "Ràng buộc đặc thù", "Spec nguồn"]
MAC_DINH = {
    "epic": ["Mục tiêu", "Phạm vi", "Tiêu chí hoàn thành epic", "Ràng buộc đặc thù", "Spec nguồn"],
    "story": ["Mô tả", "Phạm vi", "Luồng chính", "Tiêu chí nghiệm thu", "Định nghĩa xong", "Ràng buộc đặc thù",
              "Dữ liệu từ spec", "Tiền đề", "Chỗ hở", "Spec nguồn"],
    "investigation": ["Câu hỏi", "Giả định đang dùng", "Người trả lời · Mốc", "Issue bị ảnh hưởng", "Định nghĩa xong"],
    "FE": _LEAF, "BE": _LEAF, "DB": _LEAF, "INFRA": _LEAF,
    "TEST": ["Mô tả", "Ca kiểm thử bắt buộc", "Định nghĩa xong", "Dữ liệu từ spec", "Spec nguồn"],
}
LEAF_RE = re.compile(r"\(leaf ([A-Z]+(?:\s*/\s*[A-Z]+)*)\)")


def loai_tu_tieu_de(tieu_de: str) -> list[str]:
    dau = tieu_de.split("—")[0]
    if m := LEAF_RE.search(dau):
        return [x.strip() for x in m.group(1).split("/")]
    return [w.lower() for w in ("Epic", "Story", "Investigation") if re.search(rf"\b{w}\b", dau, re.I)][:1]


def doc_khuon(path) -> dict[str, list[str]]:
    p = Path(path)
    if not p.is_file():
        raise LoiBoSinh(f"thiếu khuôn: {p}")
    ra, loai, hang = {}, [], 0
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            loai, hang = (loai_tu_tieu_de(line[4:]) if line.startswith("### ") else []), 0
            continue
        if not line.lstrip().startswith("|"):
            hang = 0
            continue
        hang += 1
        o = line.strip().strip("|").split("|")[0].strip()
        if loai and hang > 2 and o:  # hàng 1 = tiêu đề cột, hàng 2 = vạch ngăn
            for k in loai:
                ra.setdefault(k, []).append(o)
    if not ra:
        raise LoiBoSinh(f"{p}: không đọc được bảng mục nào (cần `### … Epic/Story/Investigation/(leaf …)` + bảng)")
    for k, ds in ra.items():
        if k not in MAC_DINH:
            raise LoiBoSinh(f"{p}: loại `{k}` lạ (biết: {', '.join(MAC_DINH)})")
        if la := [m for m in ds if m not in MAC_DINH[k]]:
            raise LoiBoSinh(f"{p}: loại {k} có mục bộ dựng không biết {la} (biết: {MAC_DINH[k]})")
    return ra


def thu_tu(khuon: dict | None, loai: str) -> list[str]:
    return (khuon or {}).get(loai) or MAC_DINH[loai]

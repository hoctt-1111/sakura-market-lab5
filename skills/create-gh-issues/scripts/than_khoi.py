"""Khối máy sinh không cần registry spec: Định nghĩa xong, Ràng buộc đặc thù, Tiền đề, Chỗ hở, và các hàm làm sạch câu.

Hàm nhận `ctx` kiểu vịt (xem than_issue.Ctx) và trả danh sách dòng. Quy ước: không đường dẫn tệp trong thân issue (câu lấy
từ premise/gaps được bỏ đường dẫn); nhãn `constraint:*` là nhãn ràng buộc đặc thù, câu giải thích ở `team.yaml › rang_buoc`.
"""
import re

from lib import LoiBoSinh
from seed_doc import la_leaf

DUONG_DAN = (r"`[^`]*/[^`]*`", r"\b[\w.-]+\.(?:md|ya?ml|py|sql|json|txt|csv)\b")
NHAN_RB = "constraint:"
XU_LY_RE = re.compile(r"^(premise|gia_dinh|issue):(\S+)$")
XU_LY_CHU = {"premise": "đã sửa thiết kế (PREMISE {})", "gia_dinh": "giả định (PREMISE {})", "issue": "issue {}"}
# Mục «Nguồn» của điều tra: trường `nguon` tách theo « · », mỗi chỗ một dòng; khoá registry viết lại thành câu, tên tệp bỏ đuôi.
# Bảng mặc định theo bố cục registry của dự án mẫu; dự án khác đặt `than.nguon_doi: [[mẫu regex, chữ thay], …]`.
NGUON_DOI_MAC_DINH = (
    (r"system-design\.yaml › cau_hoi_mo\[([^\]]+)\]", r"câu hỏi mở \1 của thiết kế hệ thống (LAB-4)"),
    (r"detail-flows\.yaml › details\[([^\]]+)\]\.cau_hoi_mo\[(\d+)\]", r"câu hỏi mở số \2 của luồng \1 (LAB-4)"),
    (r"\bHANDOFF\.md\b", "ghi chú bàn giao"), (r"\brfp\b", "RFP"), (r"\b([\w-]+)\.(?:md|ya?ml)\b", r"\1"))


def loai_mau(it: dict) -> str:
    """Loại issue cho khuôn và mẫu định nghĩa xong: hậu tố leaf (FE, BE…) hoặc tracker (epic, story, investigation)."""
    return it["key"].rsplit("/", 1)[1] if la_leaf(it["key"]) else it["tracker"]


def lam_sach(s: str) -> str:
    """Bỏ đường dẫn/tên tệp (và cả ngoặc chứa chúng) khỏi câu lấy từ premise hoặc gaps."""
    s = re.sub(r"\s*\([^()]*(?:" + "|".join(DUONG_DAN) + r")[^()]*\)", "", str(s))
    s = re.sub("|".join(DUONG_DAN), "", s)
    return re.sub(r"\s+([,.:;])", r"\1", re.sub(r" {2,}", " ", s)).strip()


def cau_dau(s: str, toi_da: int = 260) -> str:
    c = re.split(r"\.\s+", lam_sach(s).replace("\n", " "), maxsplit=1)[0].rstrip(".")
    return (c[:toi_da - 1].rstrip() + "…" if len(c) > toi_da else c) + "."


def gom(*ds) -> list[str]:
    return list(dict.fromkeys(x for d in ds for x in d))


def dinh_nghia_xong(it: dict, ctx, them: list[str]) -> list[str]:
    """Mẫu theo loại (`team.yaml › dinh_nghia_xong_mau`) + dòng thêm cho story mang nhãn (`than.dinh_nghia_xong_story_theo_nhan`)
    + phần riêng của bản ghi."""
    mau = list((ctx.team.get("dinh_nghia_xong_mau") or {}).get(loai_mau(it)) or [])
    if it.get("tracker") == "story":
        for nhan, dong in (ctx.than_cfg.get("dinh_nghia_xong_story_theo_nhan") or {}).items():
            if nhan in (it.get("labels") or []):
                mau += list(dong)
    return gom(mau, them)


def rang_buoc(it: dict, ctx, cua_nguoi_viet: str | None) -> list[str]:
    """Câu người viết đặt trong trường văn nếu có; không thì `ten: vi_sao` của từng nhãn constraint:* trong team.yaml."""
    if cua_nguoi_viet:
        return [cua_nguoi_viet]
    theo = {x["nhan"]: x for x in ctx.team.get("rang_buoc") or []}
    ra = []
    for n in (n for n in it.get("labels") or [] if n.startswith(NHAN_RB)):
        if n not in theo:
            raise LoiBoSinh(f"{it['key']}: nhãn {n} không có trong team.yaml › rang_buoc")
        ra.append(f"{theo[n]['ten']}: {theo[n]['vi_sao']}")
    return ra


def tien_de(it: dict, ctx) -> list[str]:
    """P-xx từ premise_refs, cộng mọi dòng premise có `anh_huong` chứa key này hoặc leaf của nó."""
    ma = list(it.get("premise_refs") or [])
    ma += [p["ma"] for p in ctx.premise.values()
           if any(a == it["key"] or a.split("/")[0] == it["key"] for a in p.get("anh_huong") or [])]
    ra = []
    for m in dict.fromkeys(ma):
        if m not in ctx.premise:
            raise LoiBoSinh(f"{it['key']}: premise_refs {m} không có trong premise.yaml")
        ra.append(f"{m} — {cau_dau(lam_sach(ctx.premise[m]['spec']), 100)}")  # chỉ mã + tên ngắn, chi tiết ở tài liệu premise
    return ra


def cho_ho(it: dict, ctx) -> list[str]:
    ra = []
    for m in it.get("gap_refs") or []:
        if m not in ctx.gaps:
            raise LoiBoSinh(f"{it['key']}: gap_refs {m} không có trong gaps")
        xl = ctx.gaps[m]["xu_ly"]  # chỗ hở xử lý ngay ở chính issue này thì nói thẳng, không tự trỏ về mình
        tu = (m2 := XU_LY_RE.match(str(xl).strip())) and m2[1] == "issue" and m2[2] == it["key"]
        ra.append(f"{m} — {cau_dau(ctx.gaps[m]['mo_ta'])} (xử lý: {'ngay trong story này' if tu else xu_ly_than(xl, ctx)})")
    return ra


def xu_ly_than(s, ctx) -> str:
    """Khoá xử lý của gaps → chữ đọc được; `issue:<key>` kèm #số khi board-map có (ctx.so_issue), `de-mo` → «để mở»."""
    if str(s).strip() == "de-mo":
        return "để mở"
    m = XU_LY_RE.match(str(s).strip())
    return XU_LY_CHU[m[1]].format(ctx.so_issue(m[2]) if m[1] == "issue" else m[2]) if m else lam_sach(s)


def nguon_inv(s, ctx) -> list[str]:
    """`nguon` của điều tra → gạch đầu dòng (tách theo « · »), sau khi đổi chữ theo `than.nguon_doi` hoặc bảng mặc định."""
    for mau, thay in ctx.than_cfg.get("nguon_doi") or NGUON_DOI_MAC_DINH:
        s = re.sub(mau, thay, str(s or ""))
    return [f"- {x.strip()}" for x in s.split(" · ") if x.strip()]

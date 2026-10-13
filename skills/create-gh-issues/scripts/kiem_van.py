"""`check --seed --van`: 5 trường văn đủ theo luật độ dài và thân dựng thử không vượt trần.

`than_thu` chỉ là bản dựng tạm để đo độ dài (ghép mục theo thứ tự cố định); thân thật do than_issue.py dựng. Luật mặc định
(KHOANG, CAN_CHU) đổi được bằng khoá `van.khoang`, `van.can_chu`, trần bằng `than.tran` của --config.
Mặc định: epic — mo_ta khác rỗng, tieu_chi_nghiem_thu ≥ 1 · story — mo_ta, pham_vi khác rỗng, luong_chinh 3–7 bước,
tieu_chi_nghiem_thu 2–6 mục, dinh_nghia_xong ≥ 1 · leaf và điều tra — mo_ta khác rỗng, leaf có tieu_chi_nghiem_thu 1–3 mục.
"""
from seed_doc import REF_GOC, REF_THEM, cac_ban_ghi

KHOANG = {"epic": {"tieu_chi_nghiem_thu": (1, 99)},
          "story": {"luong_chinh": (3, 7), "tieu_chi_nghiem_thu": (2, 6), "dinh_nghia_xong": (1, 99)},
          "la": {"tieu_chi_nghiem_thu": (1, 3)}, "inv": {}}
CAN_CHU = {"epic": ("mo_ta",), "story": ("mo_ta", "pham_vi"), "la": ("mo_ta",), "inv": ("mo_ta",)}


def nhom(tracker: str) -> str:
    if tracker == "investigation":
        return "inv"
    return tracker if tracker in ("epic", "story") else "la"


def _rong(v) -> bool:
    return not (v.strip() if isinstance(v, str) else v)


def _dong(v) -> list[str]:
    return [v] if isinstance(v, str) and v.strip() else [str(x) for x in (v if isinstance(v, list) else [])]


def mau_xong(it: dict, team: dict) -> list[str]:
    mau = team.get("dinh_nghia_xong_mau") or {}
    loai = it["key"].rsplit("/", 1)[-1] if "/" in it["key"] else it["tracker"]
    return list(mau.get(loai) or [])


def than_thu(it: dict, team: dict) -> str:
    """Thân dựng thử: Mô tả · Phạm vi · Luồng chính · Tiêu chí nghiệm thu · Định nghĩa xong (mẫu + phần thêm) · Dữ liệu."""
    r = it.get("spec_refs") or {}
    phan = [("Mô tả", [str(it.get("mo_ta") or "")], ""), ("Phạm vi", _dong(it.get("pham_vi")), "- "),
            ("Luồng chính", _dong(it.get("luong_chinh")), "1. "),
            ("Tiêu chí nghiệm thu", _dong(it.get("tieu_chi_nghiem_thu")), "- "),
            ("Định nghĩa xong", mau_xong(it, team) + _dong(it.get("dinh_nghia_xong")), "- "),
            ("Dữ liệu từ spec", [f"{k}: {', '.join(r[k])}" for k in REF_GOC + REF_THEM if r.get(k)]
             + [f"Owner {it.get('owner')} · Priority {it.get('priority')} · Nhãn {', '.join(it.get('labels') or [])}"], "- ")]
    return "\n\n".join(f"## {ten}\n" + "\n".join(f"{dau}{x}" for x in ds if x) for ten, ds, dau in phan if any(ds)) + "\n"


def kiem_van(seed: dict, kq, team: dict, tran: int = 65536, khoang: dict | None = None, can_chu: dict | None = None) -> int:
    """Trả về số bản ghi đạt; mỗi bản ghi thiếu văn hoặc thân quá dài là một vi phạm (gộp lý do)."""
    khoang = {**KHOANG, **{k: {t: tuple(v) for t, v in d.items()} for k, d in (khoang or {}).items()}}
    can_chu = {**CAN_CHU, **(can_chu or {})}
    dat = 0
    for f, it in cac_ban_ghi(seed):
        g, loi = nhom(it.get("tracker", "")), []
        loi += [f"{t} rỗng" for t in can_chu[g] if _rong(it.get(t))]
        for t, (a, b) in khoang[g].items():
            n = len(it.get(t) or []) if isinstance(it.get(t), list) else 0
            if not a <= n <= b:
                loi.append(f"{t} có {n} mục, cần {a}–{b}" if b < 99 else f"{t} có {n} mục, cần ≥ {a}")
        if (dai := len(than_thu(it, team))) > tran:
            loi.append(f"thân dựng thử {dai} ký tự > {tran}")
        if loi:
            kq.vi_pham(f"backlog/{f}.yaml", None, f"{it.get('key')}: " + "; ".join(loi))
        else:
            dat += 1
    return dat

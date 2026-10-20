"""Dựng thân issue Markdown từ seed: mục «máy sinh» lấy từ seed + team/premise/gaps (+ registry spec nếu có), mục «người viết»
chép nguyên 5 trường văn (rỗng thì để dòng giữ chỗ `than.cho_trong`). Thứ tự mục theo khuôn (khuon.py).

Mục rỗng không bắt buộc thì bỏ cả tiêu đề. Trần `than.tran` ký tự (mặc định 65.536 = trần thân issue của GitHub): bỏ dần dòng
«Dữ liệu từ spec», rồi cắt «Phạm vi» của epic, còn dài thì LoiBoSinh. `than.cjk_toi_da` > 0: chặn đoạn chữ Hán/kana liền
dài hơn ngưỡng (0 = không kiểm). Câu «Ràng buộc đặc thù: …» người viết đặt trong trường văn được tách ra mục riêng.
"""
import re
from dataclasses import dataclass, field

import than_spec
from khuon import doc_khuon, thu_tu
from lib import LoiBoSinh, doc_json, doc_yaml, doc_yaml_neu_co
from seed_doc import VAN
from than_khoi import NHAN_RB, cau_dau, cho_ho, dinh_nghia_xong, lam_sach, loai_mau, nguon_inv, rang_buoc, tien_de

TRAN_GITHUB = 65536
CHO_MAC_DINH = "_(chưa viết)_"
CJK = "　-〿぀-ゟ゠-ヿ㐀-䶿一-鿿＀-￯"
RB_DAU = "Ràng buộc đặc thù:"


@dataclass
class Ctx:
    """Nguồn tra cứu nạp một lần. Test dựng thẳng bằng dữ liệu tí hon."""
    muc: dict = field(default_factory=dict)       # key → bản ghi seed (epic lẫn item)
    con: dict = field(default_factory=dict)       # key cha → [key con] theo thứ tự seed
    team: dict = field(default_factory=dict)
    premise: dict = field(default_factory=dict)   # P-xx → dòng premise.yaml
    gaps: dict = field(default_factory=dict)      # G-xx → dòng gaps
    man: dict = field(default_factory=dict)       # registry: mã màn → bản ghi screens-design
    spec_id: dict = field(default_factory=dict)   # registry: mã màn → mã spec
    api: dict = field(default_factory=dict)       # registry: API-nnn → {api_id, method, route}
    bang_chu: dict = field(default_factory=dict)  # bảng → key story giữ migration (leaf DB)
    tien_to: dict = field(default_factory=dict)   # registry: tiền tố mã spec theo loại
    than_cfg: dict = field(default_factory=dict)
    spec_cfg: dict = field(default_factory=dict)
    khuon: dict | None = None
    so: dict = field(default_factory=dict)        # key → số issue (<evidence-dir>/board-map.json); rỗng thì in key

    def so_issue(self, key: str) -> str:
        """`SC-080/DB` → «#23 (SC-080/DB)» khi board-map có số; không thì giữ key."""
        return f"#{self.so[key]} ({key})" if key in self.so else key

    @property
    def co_spec(self) -> bool:
        return bool(self.man or self.spec_id or self.api)


def nap_ctx(cfg) -> Ctx:
    c = Ctx(than_cfg=dict(cfg.than or {}), spec_cfg=dict(cfg.spec or {}), khuon=doc_khuon(cfg.khuon) if cfg.khuon else None)
    for p in sorted(cfg.backlog.glob("*.yaml")):
        d = doc_yaml(p)
        for it in [d["epic"]] + list(d.get("items") or []):
            c.muc[it["key"]] = it
            if it.get("cha"):
                c.con.setdefault(it["cha"], []).append(it["key"])
            if it["key"].endswith("/DB"):
                for t in it["spec_refs"].get("bang", []):
                    c.bang_chu.setdefault(t, it["cha"])
    c.team = doc_yaml(cfg.team)
    c.premise = {p["ma"]: p for p in (doc_yaml_neu_co(cfg.seed_dir / "premise.yaml") or {}).get("p") or []}
    for f in [cfg.seed_dir / "gaps.yaml"] + sorted((cfg.seed_dir / "gaps").glob("*.yaml")):
        for g in (doc_yaml_neu_co(f) or {}).get("g") or []:
            c.gaps.setdefault(g["ma"], g)
    if cfg.spec_registry:
        than_spec.nap(c, cfg.spec_registry)
    if cfg.evidence_dir and cfg.map_file.is_file():
        c.so = {k: e["so"] for k, e in (doc_json(cfg.map_file) or {}).items() if e.get("so") is not None}
    return c


def than(key: str, ctx: Ctx) -> str:
    if key not in ctx.muc:
        raise LoiBoSinh(f"không có key {key} trong seed backlog")
    return than_tu_item(ctx.muc[key], ctx)


def _van(v, so=False) -> list[str]:
    """Trường văn → dòng Markdown; chuỗi là đoạn văn, danh sách là gạch đầu dòng (hoặc đánh số)."""
    if isinstance(v, str):
        return [v.strip()] if v.strip() else []
    ds = [str(x).strip() for x in v or [] if str(x).strip()]
    return [f"{i}. {x}" if so else f"- {x}" for i, x in enumerate(ds, 1)]


def _tach_rang_buoc(it: dict):
    """Lấy câu «Ràng buộc đặc thù: …» ra khỏi 5 trường văn; trả (bản ghi sạch, câu | None)."""
    it, cau = dict(it), None
    for f in VAN:
        v = it.get(f)
        ds = v.split("\n") if isinstance(v, str) else [str(x) for x in v or []]
        for d in ds:
            if d.strip().startswith(RB_DAU):
                cau = d.strip()[len(RB_DAU):].strip()
        giu = [d for d in ds if not d.strip().startswith(RB_DAU)]
        it[f] = "\n".join(giu) if isinstance(v, str) else giu
    return it, cau


def _muc(it: dict, ctx: Ctx, cau: str | None) -> list[tuple[str, list[str] | None]]:
    """[(tên mục, dòng)] theo thứ tự khuôn; None = mục không có (bỏ tiêu đề)."""
    loai = loai_mau(it)
    bb = lambda lines: lines or [ctx.than_cfg.get("cho_trong", CHO_MAC_DINH)]  # noqa: E731 (mục bắt buộc)
    gach = lambda f: _van(it.get(f))  # noqa: E731
    bullet = lambda ds: [f"- {x}" for x in ds]  # noqa: E731
    xong = dinh_nghia_xong(it, ctx, [str(x).strip() for x in it.get("dinh_nghia_xong") or [] if str(x).strip()])
    rb = rang_buoc(it, ctx, cau) if any(n.startswith(NHAN_RB) for n in it.get("labels") or []) else []
    dl, nguon = bullet(than_spec.du_lieu(it, ctx)), bullet(than_spec.spec_nguon(it, ctx))
    if loai == "epic":
        con = [k for k in ctx.con.get(it["key"], []) if ctx.muc[k]["tracker"] == "story"]
        muc = {"Mục tiêu": bb(_van(it.get("mo_ta"))), "Phạm vi": [f"- {k} — {ctx.muc[k]['title_vi']}" for k in con] or None,
               "Tiêu chí hoàn thành epic": bb(gach("tieu_chi_nghiem_thu")), "Ràng buộc đặc thù": bullet(rb) or None,
               "Spec nguồn": nguon or None}
    elif loai == "investigation":
        p = next((x for x in ctx.premise.values() if x.get("inv") == it["key"]), None) \
            or next((ctx.premise[m] for m in it.get("premise_refs") or [] if m in ctx.premise), None)
        hoi = _van(it.get("mo_ta")) or [f"Cần chốt: {it['title_vi']}." + (f" {lam_sach(p['cho_de_ngo'])}" if p and p.get("cho_de_ngo") else "")]
        muc = {"Câu hỏi": hoi, "Giả định đang dùng": [cau_dau(p.get("sau") or p.get("chot") or "")] if p else None,
               "Người trả lời · Mốc": [f"{it.get('nguoi_tra_loi', '')} · {it.get('han', '')}".strip(" ·")] or None,
               "Issue bị ảnh hưởng": bullet([ctx.so_issue(k) for k in p.get("anh_huong") or []]) if p else None, "Định nghĩa xong": bullet(xong),
               "Nguồn": nguon_inv(it.get("nguon"), ctx) or None}
    elif loai == "story":
        muc = {"Mô tả": bb(_van(it.get("mo_ta"))), "Phạm vi": bb(_van(it.get("pham_vi"))),
               "Luồng chính": bb(_van(it.get("luong_chinh"), so=True)), "Tiêu chí nghiệm thu": bb(gach("tieu_chi_nghiem_thu")),
               "Định nghĩa xong": bullet(xong), "Ràng buộc đặc thù": bullet(rb) or None, "Dữ liệu từ spec": dl or None,
               "Tiền đề": bullet(tien_de(it, ctx)) or None, "Chỗ hở": bullet(cho_ho(it, ctx)) or None, "Spec nguồn": nguon or None}
    else:
        ten_tc = "Ca kiểm thử bắt buộc" if loai == "TEST" else "Tiêu chí nghiệm thu"
        muc = {"Mô tả": bb(_van(it.get("mo_ta"))), ten_tc: bb(gach("tieu_chi_nghiem_thu")), "Định nghĩa xong": bullet(xong),
               "Dữ liệu từ spec": dl or None, "Ràng buộc đặc thù": bullet(rb) or None, "Spec nguồn": nguon or None}
    return [(t, muc[t]) for t in thu_tu(ctx.khuon, loai) if t in muc]


def _ghep(muc) -> str:
    return "\n\n".join(f"## {t}\n" + "\n".join(d) for t, d in muc if d)


def _vua_tran(muc: list, tran: int, key: str, epic: bool) -> str:
    """Bỏ dần dòng «Dữ liệu từ spec», rồi cắt «Phạm vi» (danh sách máy sinh của epic) cho vừa trần."""
    muc = [[t, list(d) if d else d] for t, d in muc]
    ten = [t for t, _ in muc]
    if "Dữ liệu từ spec" in ten:
        d = muc[ten.index("Dữ liệu từ spec")][1]
        while d and len(_ghep(muc)) > tran:
            d.pop()
    if epic and "Phạm vi" in ten and len(_ghep(muc)) > tran:
        d = muc[ten.index("Phạm vi")][1]
        goc = list(d or [])
        for giu in range(len(goc) - 1, 0, -1):
            d[:] = goc[:giu] + [f"… và {len(goc) - giu} story nữa"]
            if len(_ghep(muc)) <= tran:
                break
    body = _ghep(muc)
    if len(body) > tran:
        raise LoiBoSinh(f"{key}: thân {len(body)} ký tự > {tran} sau khi bỏ dòng dữ liệu và cắt phạm vi — rút văn người viết")
    return body


def than_tu_item(item: dict, ctx: Ctx) -> str:
    sach, cau = _tach_rang_buoc(item)
    body = _vua_tran(_muc(sach, ctx, cau), int(ctx.than_cfg.get("tran", TRAN_GITHUB)), item["key"], item["tracker"] == "epic")
    if (n := int(ctx.than_cfg.get("cjk_toi_da", 0))) and (m := re.search(f"[{CJK}]{{{n + 1},}}", body)):
        raise LoiBoSinh(f"{item['key']}: chữ Nhật liền {len(m.group())} ký tự (tối đa {n}): «{m.group()[:20]}»")
    return body

"""«Spec nguồn» và «Dữ liệu từ spec» của thân issue; registry spec là TUỲ CHỌN (`--spec-registry <thư mục>`).

Có registry: đọc ba file theo bố cục registry Spec Standard — `screens-design.yaml › man[]` (sc, ten_vi, items[], validation[],
fr_chi_phoi, tang_dac_quyen, thiet_bi, thuc_the_chinh, loai) · `spec-standard.yaml › screens[]` + `id_ranges.<loại>.{prefix,
start}` · `api-design.yaml › apis[]` (api_id, method, route) — để in mã spec của màn/API và khối «Dữ liệu từ spec» (validation
chỉ đếm, không chép điều kiện). Bảng diễn giải giá trị lấy từ khoá `spec` của --config (`loai_man`, `tang`, `thiet_bi`,
`ngoai_bang`, `ghi_chu_validation`, `trien_khai{tieu_de, ten}`); thiếu thì in nguyên giá trị.
Không có registry: «Dữ liệu từ spec» bỏ hẳn, «Spec nguồn» chỉ liệt mã trong `spec_refs` theo nhóm.
"""
from lib import LoiBoSinh, doc_yaml
from seed_doc import la_leaf
from than_khoi import gom, loai_mau

THU_TU = {  # thứ tự dòng «Dữ liệu từ spec» theo loại issue
    "story": ("item", "validation", "fr", "tang", "thiet_bi", "thuc_the", "loai_man", "api"),
    "FE": ("item", "validation", "thiet_bi", "nhan", "cha", "epic"),
    "BE": ("api", "bang", "ghi_doc", "validation", "nhan", "cha", "epic"),
    "DB": ("bang", "ghi_doc", "nhan", "cha", "epic"),
    "INFRA": ("nhan", "cha", "epic"),
    "TEST": ("validation", "fr", "api", "tang"),
}
TK_DAU = "trien_khai."
ID_RANGE = {"sc": "screen", "khuon": "khuon_bao_cao", "api": "api", "tech": "detail"}


def nap(ctx, thu_muc) -> None:
    """Điền ctx.man, ctx.spec_id, ctx.api, ctx.tien_to từ registry."""
    ss = doc_yaml(thu_muc / "spec-standard.yaml")
    ir = ss["id_ranges"]
    ctx.man = {m["sc"]: m for m in doc_yaml(thu_muc / "screens-design.yaml")["man"]}
    ctx.tien_to = {k: (ir.get(v) or ir["screen"])["prefix"] for k, v in ID_RANGE.items()}
    ctx.spec_id = {s["sc"]: f"{ctx.tien_to['sc']}-{ir['screen']['start'] + i}" for i, s in enumerate(ss["screens"])}
    ctx.api = {f"API-{ir['api']['start'] + i}": a for i, a in enumerate(doc_yaml(thu_muc / "api-design.yaml")["apis"])}


def _so(ma: str) -> str:
    return ma.rsplit("-", 1)[1]


def _ref_story(it: dict, ctx) -> dict:
    """spec_refs của issue; epic không có mã riêng nên gộp mã của story con."""
    r = {k: list(v) for k, v in (it.get("spec_refs") or {}).items()}
    if it["tracker"] == "epic":
        for k in ctx.con.get(it["key"], []):
            if ctx.muc[k]["tracker"] == "story":
                for f, v in (ctx.muc[k].get("spec_refs") or {}).items():
                    r[f] = gom(r.get(f, []), v)
    return r


def _co_registry(it: dict, r: dict, ctx) -> list[str]:
    ra, tt = [], ctx.tien_to
    if it["tracker"] == "epic":  # gọn: chỉ số mã spec, tên từng màn nằm ở mục Phạm vi
        for ten, f in (("Màn", "sc"), ("API", "api"), ("Luồng kỹ thuật", "tech")):
            so = [ctx.spec_id[x].rsplit("-", 1)[1] if f == "sc" else _so(x) for x in r.get(f, [])]
            if so:
                ra.append(f"{ten} ({tt[f]}): " + ", ".join(sorted(so)))
        return ra
    for sc in r.get("sc", []):
        if sc not in ctx.spec_id:
            raise LoiBoSinh(f"{it['key']}: màn {sc} không có trong spec-standard")
        ten = (ctx.muc.get(sc) or {}).get('title_vi') or (ctx.man.get(sc) or {}).get('ten_vi', '')  # tên ngắn theo seed
        ra.append(f"{ctx.spec_id[sc]} ({sc} {ten})".replace(" )", ")"))
    ra += [f"{tt['khuon']}-{_so(k)} ({k})" for k in r.get("khuon", [])]
    for a in r.get("api", []):
        if (x := ctx.api.get(a)) is None:
            raise LoiBoSinh(f"{it['key']}: {a} không có trong api-design")
        ra.append(f"{tt['api']}-{_so(a)} {x['api_id']} {x['method']} {x['route']}")
    return ra + [f"{tt['tech']}-{_so(t)} ({t})" for t in r.get("tech", [])]


def spec_nguon(it: dict, ctx) -> list[str]:
    r = _ref_story(it, ctx)
    ra = [f"Nhóm chức năng {it['key']} (feature {it['feature']})"] if it["tracker"] == "epic" and it.get("feature") else []
    if ctx.co_spec:
        ra += _co_registry(it, r, ctx)
    else:
        ra += [f"{ten}: " + ", ".join(r[f]) for ten, f in (("Màn", "sc"), ("Khuôn", "khuon"), ("API", "api"),
                                                            ("Luồng kỹ thuật", "tech")) if r.get(f)]
    tk_cfg = ctx.spec_cfg.get("trien_khai") or {}
    sd = r.get("sd", [])
    tk = [x[len(TK_DAU):] for x in sd if x.startswith(TK_DAU)] if tk_cfg else []
    khac = [x for x in sd if not (tk_cfg and x.startswith(TK_DAU))] + r.get("hoi", [])
    for ten, f in (("Bảng", "bang"), ("FR", "fr"), ("ADR", "adr"), ("NFR", "nfr"), ("Mã khác", "ac")):
        if v := r.get(f, []) + (khac if f == "ac" else []):
            ra.append(f"{ten}: " + ", ".join(v))
    if la := [k for k in tk if k not in (tk_cfg.get("ten") or {})]:
        raise LoiBoSinh(f"{it['key']}: khoá triển khai lạ {la} — thêm tên đọc được vào spec.trien_khai.ten")
    if tk:
        ra.append(f"{tk_cfg['tieu_de']}: " + ", ".join(tk_cfg["ten"][k] for k in tk))
    return ra


def _dong_bang(ctx, bang: list, sk: str) -> str:
    vt = [f"{t} ({'chủ migration' if ctx.bang_chu.get(t) == sk else 'migration thuộc ' + ctx.bang_chu.get(t, 'chưa có story nào')})"
          for t in bang]
    return "Bảng: " + ", ".join(vt)


def du_lieu(it: dict, ctx) -> list[str]:
    """Dòng «Dữ liệu từ spec»; không có registry → [] (mục bị bỏ)."""
    if not ctx.co_spec:
        return []
    key, loai, g = it["key"], loai_mau(it), ctx.spec_cfg
    sk = it["cha"] if la_leaf(key) else key
    story = ctx.muc.get(sk, it)
    m, r, sr = ctx.man.get(sk) or {}, it.get("spec_refs") or {}, story.get("spec_refs") or {}
    apis = [ctx.api[a] for a in (r.get("api") or sr.get("api") or []) if a in ctx.api]
    bang, its, ngoai = r.get("bang") or [], m.get("items") or [], set(g.get("ngoai_bang") or [])
    nhan = [n for n in it.get("labels") or [] if n.startswith("constraint:")]
    dien = lambda bang_ten, v: (g.get(bang_ten) or {}).get(v, v)  # noqa: E731
    fr = r.get("fr") or m.get("fr_chi_phoi")
    d = {
        "item": f"Số item trên màn: {len(its)}" if "items" in m else None,
        "validation": (f"Số điều kiện validation theo FR: {len(m['validation'])}{g.get('ghi_chu_validation', '')}"
                       if "validation" in m else None),
        "fr": ("FR chi phối: " + ", ".join(fr)) if fr else None,
        "tang": f"Tầng đặc quyền: {dien('tang', m['tang_dac_quyen'])}" if m.get("tang_dac_quyen") else None,
        "thiet_bi": f"Thiết bị: {dien('thiet_bi', m['thiet_bi'])}" if m.get("thiet_bi") else None,
        "thuc_the": f"Thực thể chính: {m['thuc_the_chinh']}" if m.get("thuc_the_chinh") else None,
        "loai_man": f"Loại màn: {dien('loai_man', m['loai'])}" if m.get("loai") else None,
        "api": ("API phục vụ: " + ", ".join(f"{a['method']} {a['route']}" for a in apis)) if apis else None,
        "bang": _dong_bang(ctx, bang, sk) if bang else None,
        "ghi_doc": (f"Item ghi: {sum(bool(i.get('ghi')) for i in its)} · item đọc bảng: "
                    f"{sum(1 for i in its if i.get('tu') and i['tu'] not in ngoai)}") if its and bang else None,
        "nhan": ("Nhãn ràng buộc: " + ", ".join(nhan)) if nhan else None,
        "cha": f"Story cha: {sk} — {story['title_vi']}" if la_leaf(key) else None,
        "epic": None,
    }
    ep = ctx.muc.get(story.get("cha"))
    if ep and la_leaf(key):
        d["epic"] = f"Epic: {ep['key']} — {ep['title_vi']}"
    return [d[k] for k in THU_TU.get(loai, ()) if d.get(k)]

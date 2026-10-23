"""Báo cáo HTML tự chứa của audit: tab «Theo ticket» (mỗi ticket vi phạm một khối: giá trị hiện tại, từng rule bị phạm,
sai ở đâu, cách sửa, link GitHub) · mục phát hiện không gắn một ticket · tab «Theo rule» · tab «Tiêu chí» (đủ 39, gồm
không áp dụng). Khung CSS/JS ở `templates/khung-bao-cao.html`; mọi chuỗi từ ảnh chụp đi qua html.escape."""
from collections import Counter
from html import escape as e
from pathlib import Path

KHUNG = Path(__file__).resolve().parents[1] / "templates" / "khung-bao-cao.html"
TEN_MUC = {"B": "Chặn", "W": "Lệch quy ước", "I": "Ghi nhận"}
THU_TU = {"B": 0, "W": 1, "I": 2}
HIEN = (("status", "Status"), ("owner", "Owner"), ("priority", "Priority"), ("sprint", "Sprint"), ("bat_dau", "Bắt đầu"),
        ("han", "Hạn"), ("xong", "Done Date"), ("point", "Story Point"), ("uoc", "Giờ ước"), ("da_lam", "Giờ đã làm"))


def _repo(nc) -> str | None:
    r = nc.anh.get("repo")
    return (r.get("ten") if isinstance(r, dict) else r) or nc.cfg.get("repo")


def _link(nc, so) -> str:
    r = _repo(nc)
    return f'<a href="https://github.com/{e(r)}/issues/{so}" target="_blank" rel="noopener">#{so}</a>' if r else f"#{so}"


def _url(u) -> str:
    """Link Project chỉ khi là http(s); khác thì in chữ (ảnh chụp là dữ liệu ngoài)."""
    u = str(u or "")
    return f'<a href="{e(u)}">{e(u)}</a>' if u.startswith(("https://", "http://")) else e(u)


def _chip(muc: str, chu: str) -> str:
    return f'<span class="chip {muc}">{e(chu)}</span>'


def _hien_tai(nc, it: dict) -> str:
    o = [f"<div><span>{nhan}:</span> {e(str(v))}</div>" for k, nhan in HIEN if (v := nc.f(it, k)) is not None]
    o.append(f"<div><span>Issue GitHub:</span> {e(str(it.get('state')).lower())}</div>")
    o.append(f"<div><span>Người phụ trách:</span> {e(', '.join(it.get('assignees') or []) or '—')}</div>")
    if it.get("cha") is not None:
        o.append(f"<div><span>Cha:</span> {_link(nc, it['cha'])}</div>")
    o.append(f"<div><span>Nhãn:</span> {e(', '.join(it.get('labels') or []) or '—')}</div>")
    return '<div class="hien">' + "".join(o) + "</div>"


def _vp(p: dict, t: dict) -> str:
    return (f'<div class="vp {p["muc"]}" data-ma="{e(p["ma"])}" data-muc="{p["muc"]}">'
            f'<p>{_chip(p["muc"], p["ma"] + " · " + TEN_MUC[p["muc"]])} <b>{e(t["ten"])}</b></p>'
            f'<p><span class="nhan-dong">Sai ở đâu</span> {e(p["ly_do"])}</p>'
            f'<p><span class="nhan-dong">Cách sửa</span> {e(t.get("cach_sua") or "")}</p>'
            f'<p class="mo"><span class="nhan-dong">Nguồn rule</span> {e(t["nguon"])} · đo: {e(t["cach_do"])}</p></div>')


def _ticket(nc, so: int, ps: list[dict], tc: dict) -> str:
    it = nc.theo_so[so]
    ps = sorted(ps, key=lambda p: (THU_TU[p["muc"]], p["ma"]))
    tim = f"#{so} {it.get('title') or ''}".lower()
    chips = "".join(_chip(m, f"{m} {n}") for m, n in sorted(Counter(p["muc"] for p in ps).items(), key=lambda x: THU_TU[x[0]]))
    return (f'<details class="ticket" id="t-{so}" data-tim="{e(tim)}">'
            f'<summary><span class="so">{_link(nc, so)}</span><span class="td">{e(it.get("title") or "")}</span>{chips}'
            f'<span class="mo">{e(", ".join(sorted({p["ma"] for p in ps})))}</span></summary>'
            f'<div class="than">{_hien_tai(nc, it)}{"".join(_vp(p, tc[p["ma"]]) for p in ps)}</div></details>')


def _doi_tuong(p: dict) -> str:
    return f'<a href="#t-{p["so"]}">#{p["so"]}</a>' if p["so"] is not None else e(str(p["khoa"]))


def _rule(nc, ma: str, ps: list[dict], t: dict) -> str:
    dong = "".join(f'<tr><td>{_doi_tuong(p)}</td><td>{e(p["title"][:70])}</td><td>{e(p["ly_do"])}</td></tr>' for p in ps)
    return (f'<details class="rule" id="r-{e(ma)}" data-ma="{e(ma)}" data-muc="{t["muc"]}"><summary>'
            f'{_chip(t["muc"], ma + " · " + TEN_MUC[t["muc"]])} <span class="td">{e(t["ten"])}</span><b>{len(ps)}</b></summary>'
            f'<div class="than"><p><span class="nhan-dong">Cách sửa</span> {e(t.get("cach_sua") or "")}</p>'
            f'<div class="bang"><table><tr><th>Issue</th><th>Tiêu đề</th><th>Sai ở đâu</th></tr>{dong}</table></div></div></details>')


def _tieu_chi(tc: dict, kq: dict, dem: Counter) -> str:
    dong = []
    for t in tc.values():
        kq_t = ("không áp dụng: " + t["ly_do"]) if not t["ap_dung"] else (
            "bỏ qua: thiếu nguồn" if t["ma"] in kq["bo_qua"] else f"{dem[t['ma']]} phát hiện")
        dong.append(f'<tr><td>{e(t["ma"])}</td><td>{e(t["chieu"])}</td><td>{e(t["ten"])}</td><td>{_chip(t["muc"], TEN_MUC[t["muc"]])}</td>'
                    f'<td>{e(kq_t)}</td><td>{e(t.get("cach_sua") or "")}</td></tr>')
    return ('<div class="bang"><table><tr><th>Mã</th><th>Chiều</th><th>Tiêu chí</th><th>Mức</th><th>Kết quả</th><th>Cách sửa</th></tr>'
            + "".join(dong) + "</table></div>")


def dung(nc, kq: dict) -> str:
    tc = {t["ma"]: t for t in nc.tc["tieu_chi"]}
    ph = kq["phat_hien"]
    dem, muc = Counter(p["ma"] for p in ph), Counter(p["muc"] for p in ph)
    theo_so = {}
    for p in ph:
        if p["so"] is not None and p["so"] in nc.theo_so:
            theo_so.setdefault(p["so"], []).append(p)
    rieng = [{**p, "khoa": p["khoa"] or f"#{p['so']}"} for p in ph if p["so"] is None or p["so"] not in nc.theo_so]
    thu_tu = sorted(theo_so, key=lambda s: (min(THU_TU[p["muc"]] for p in theo_so[s]), s))
    pj = nc.anh.get("project") or {}
    co = [m for m in tc if dem[m]]
    o = [f'<h1>Audit ticket — {e(pj.get("title") or "")}</h1>',
         f'<p class="mo">{_url(pj.get("url"))} · chụp {e(str(nc.anh.get("chup_luc")))} · '
         f'ngày xét quá hạn {e(nc.ngay_xet)} · {len(nc.items)} issue ({len(nc.song)} sống, {len(nc.thay)} bản thay thế)</p>',
         f'<p class="mo">Thước đo: {e(nc.tc.get("nguon_quy_uoc", ""))}.</p>',
         '<div class="kpi">' + "".join(f'<div class="{m}"><b>{muc[m]}</b>phát hiện {TEN_MUC[m].lower()}</div>' for m in "BWI")
         + f'<div><b>{len(theo_so)}</b>ticket vi phạm</div><div><b>{len(co)}/{sum(t["ap_dung"] for t in tc.values())}</b>rule có vi phạm</div>'
         + (f'<div><b>{len(kq["bo_qua"])}</b>bỏ qua: {e(", ".join(kq["bo_qua"]))}</div>' if kq["bo_qua"] else "") + "</div>",
         '<div class="dk"><button data-tab="tab-ticket">Theo ticket</button><button data-tab="tab-rule">Theo rule</button>'
         '<button data-tab="tab-tieu-chi">Tiêu chí</button>'
         + "".join(f'<label><input type="checkbox" class="loc-muc" value="{m}" checked> {TEN_MUC[m]}</label>' for m in "BWI")
         + '<select id="loc-rule"><option value="">Mọi rule</option>'
         + "".join(f'<option value="{e(m)}">{e(m)} ({dem[m]})</option>' for m in co)
         + '</select><input type="search" id="tim" placeholder="Tìm #số hoặc khoá"></div>',
         '<section class="tab" id="tab-ticket"><h2>Theo ticket</h2>'
         + ("".join(_ticket(nc, s, theo_so[s], tc) for s in thu_tu) or "<p>Không có ticket vi phạm.</p>")
         + '<section id="khong-gan-ticket"><h2>Phát hiện không gắn một ticket</h2>'
         + ('<div class="bang"><table><tr><th>Mã</th><th>Đối tượng</th><th>Sai ở đâu</th><th>Cách sửa</th></tr>'
            + "".join(f'<tr><td>{_chip(p["muc"], p["ma"])}</td><td>{e(str(p["khoa"]))}</td><td>{e(p["ly_do"])}</td>'
                      f'<td>{e(tc[p["ma"]].get("cach_sua") or "")}</td></tr>' for p in rieng) + "</table></div>" if rieng else "<p>Không có.</p>")
         + '</section></section><section class="tab" id="tab-rule"><h2>Theo rule</h2>'
         + ("".join(_rule(nc, m, [p for p in ph if p["ma"] == m], tc[m]) for m in co) or "<p>Không có vi phạm.</p>")
         + '</section><section class="tab" id="tab-tieu-chi"><h2>Tiêu chí</h2>' + _tieu_chi(tc, kq, dem) + "</section>"]
    return KHUNG.read_text(encoding="utf-8").replace("__TIEU_DE__", e(f"Audit ticket — {pj.get('title') or ''}"), 1) \
        .replace("__NOI_DUNG__", "\n".join(o), 1)

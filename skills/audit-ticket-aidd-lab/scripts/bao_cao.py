"""Báo cáo Markdown của audit: kết luận đếm theo mức → Chặn (B) → Lệch quy ước (W) → Ghi nhận (I) → Không áp dụng →
Phủ chiều (mọi tiêu chí áp dụng, in cả 0 và «bỏ qua: thiếu nguồn») → phụ lục đếm. Bảng tiêu chí cho docs."""
from collections import Counter

TEN_MUC = {"B": "Chặn (B)", "W": "Lệch quy ước (W)", "I": "Ghi nhận (I)"}
TOI_DA = 60   # dòng mỗi tiêu chí trong bảng chi tiết; đủ số issue nằm ở «Phụ lục: danh sách đủ»


def _o(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def _lien_ket(nc, p) -> str:
    if p["so"] is None:
        return f"`{_o(p['khoa'])}`"
    repo = nc.anh.get("repo")
    repo = (repo.get("ten") if isinstance(repo, dict) else repo) or nc.cfg.get("repo")   # snap-board lưu {ten, labels}
    return f"[#{p['so']}](https://github.com/{repo}/issues/{p['so']})" if repo else f"#{p['so']}"


def _dem_muc(kq: dict) -> Counter:
    return Counter(p["muc"] for p in kq["phat_hien"])


def dong_tom(kq: dict) -> str:
    d = _dem_muc(kq)
    return f"B {d['B']} · W {d['W']} · I {d['I']} · bỏ qua {len(kq['bo_qua'])}"


def dung(nc, kq: dict, toi_da: int = TOI_DA) -> str:
    ds = {t["ma"]: t for t in nc.tc["tieu_chi"]}
    theo_ma = Counter(p["ma"] for p in kq["phat_hien"])
    d = _dem_muc(kq)
    pj = nc.anh.get("project") or {}
    ra = [f"# Audit ticket — {_o(pj.get('title') or '')}", "",
          f"Project: {pj.get('url', '')} · ảnh chụp lúc {nc.anh.get('chup_luc')} · ngày xét quá hạn {nc.ngay_xet} · "
          f"{len(nc.items)} issue ({len(nc.song)} sống, {len(nc.thay)} bản thay thế).", "",
          f"Thước đo: {nc.tc.get('nguon_quy_uoc', '')} (bản mã hoá, ngày {nc.tc.get('ngay', '')}).", "",
          "## Kết luận", "",
          f"- Chặn (B): {d['B']} · Lệch quy ước (W): {d['W']} · Ghi nhận (I): {d['I']}.",
          f"- Tiêu chí áp dụng {sum(t['ap_dung'] for t in ds.values())}, có phát hiện {len(theo_ma)}, "
          f"bỏ qua vì thiếu nguồn {len(kq['bo_qua'])}{' (' + ', '.join(kq['bo_qua']) + ')' if kq['bo_qua'] else ''}, "
          f"không áp dụng {len(kq['khong_ap_dung'])}."]
    if sau := sum(1 for i in nc.song if (nc.f(i, "xong") or "") > nc.ngay_xet):
        ra.append(f"- Cảnh báo: {sau} Done Date sau ngày xét {nc.ngay_xet}. Board giả lập thì chạy lại với `--ngay-xet` "
                  "bằng ngày chụp giả lập (hoặc khoá `ngay_xet` trong config); G2, H1 đang đo theo ngày sai.")
    ra.append("")
    cat = []
    for m in ("B", "W", "I"):
        ra += [f"## {TEN_MUC[m]}", ""]
        nhom = [p for p in kq["phat_hien"] if p["muc"] == m]
        if not nhom:
            ra += ["Không có.", ""]
            continue
        ra += ["| Mã | Issue | Tiêu đề | Lý do |", "| --- | --- | --- | --- |"]
        for ma in [x for x in ds if theo_ma[x] and ds[x]["muc"] == m]:
            ps = [p for p in nhom if p["ma"] == ma]
            ra += [f"| {ma} | {_lien_ket(nc, p)} | {_o(p['title'][:60])} | {_o(p['ly_do'])} |" for p in ps[:toi_da]]
            if len(ps) > toi_da:
                cat.append(ma)
                ra.append(f"| {ma} | … | còn {len(ps) - toi_da} dòng | xem «Phụ lục: danh sách đủ» |")
        ra.append("")
    ra += ["## Không áp dụng", "", "| Mã | Tiêu chí | Lý do |", "| --- | --- | --- |"]
    ra += [f"| {t['ma']} | {_o(t['ten'])} | {_o(t['ly_do'])} |" for t in kq["khong_ap_dung"]] + [""]
    ra += ["## Phủ chiều", "", "| Mã | Chiều | Tiêu chí | Mức | Phát hiện | Ghi chú |", "| --- | --- | --- | --- | --- | --- |"]
    for t in (t for t in ds.values() if t["ap_dung"]):
        so = "bỏ qua: thiếu nguồn" if t["ma"] in kq["bo_qua"] else str(theo_ma[t["ma"]])
        ra.append(f"| {t['ma']} | {t['chieu']} | {_o(t['ten'])} | {t['muc']} | {so} | {_o(t.get('ghi_chu') or '')} |")
    ra += ["", "## Phụ lục: đếm theo tracker và Status (issue sống)", "", "| Tracker | Status | Số |", "| --- | --- | --- |"]
    dem = Counter((nc.tracker(i) or "?", nc.f(i, "status") or "—") for i in nc.song)
    ra += [f"| {t} | {s} | {n} |" for (t, s), n in sorted(dem.items())]
    if cat:
        ra += ["", "## Phụ lục: danh sách đủ", "", "Tiêu chí có nhiều hơn số dòng của bảng chi tiết; đủ số issue:", ""]
        ra += [f"- {ma}: " + ", ".join(f"#{p['so']}" if p["so"] is not None else str(p["khoa"])
                                     for p in kq["phat_hien"] if p["ma"] == ma) for ma in cat]
    return "\n".join(ra) + "\n"


def bang_tieu_chi(tc: dict) -> str:
    ra = ["# Tiêu chí audit", "", f"Thước đo: {tc.get('nguon_quy_uoc', '')}. Ngày: {tc.get('ngay', '')}.", "",
          "| Mã | Chiều | Tiêu chí | Nguồn | Cách đo | Mức | Áp dụng | Lý do / ghi chú |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for t in tc["tieu_chi"]:
        ra.append(f"| {t['ma']} | {t['chieu']} | {_o(t['ten'])} | {_o(t['nguon'])} | {_o(t['cach_do'])} | {t['muc']} | "
                  f"{'có' if t['ap_dung'] else 'không'} | {_o(t.get('ly_do') or t.get('ghi_chu') or '')} |")
    return "\n".join(ra) + "\n"

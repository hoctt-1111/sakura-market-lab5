"""Luật trạng thái và ngày (G, H): cha xong khi con chưa xong, Closed ↔ Done Date, Closed mà issue còn mở, phụ thuộc
giữa lá, quá hạn, trượt. Ngày xét = `--ngay-xet` (board giả lập: ngày chụp giả lập) hoặc ngày chụp ảnh."""
from audit_lib import hau_to, ph, story_cua_la


def G1(nc):
    x = nc.cfg["status_xong"]
    return [ph("G1", i, f"cha {x} mà còn con chưa xong: " + ", ".join(f"#{c['so']}" for c in con))
            for i in nc.song if nc.f(i, "status") == x
            and (con := [c for c in nc.con_song(i) if nc.f(c, "status") != x])]


def G2(nc):
    x, ra = nc.cfg["status_xong"], []
    for i in nc.song:
        s, d = nc.f(i, "status"), nc.f(i, "xong")
        if (s == x) != (d is not None):
            ra.append(ph("G2", i, f"Status {s} mà Done Date {d}"))
        elif d is not None and d > nc.ngay_xet:
            ra.append(ph("G2", i, f"Done Date {d} sau ngày xét {nc.ngay_xet}"))
        elif s in nc.cfg["status_chua_lam"] and nc.f(i, "da_lam") is not None:
            ra.append(ph("G2", i, f"Status {s} mà đã ghi giờ đã làm {nc.f(i, 'da_lam')}"))
    return ra


def G3(nc):
    x = nc.cfg["status_xong"]
    return [ph("G3", i, f"Status {x} trên board, issue GitHub còn mở") for i in nc.song
            if nc.f(i, "status") == x and str(i.get("state")).upper() == "OPEN"]


def _phu_thuoc(nc, i, theo_khoa) -> list[str]:
    pt, k = nc.pt, nc.khoa(i)
    h, st = hau_to(k), story_cua_la(k)
    if h is None:
        return []
    ds = [f"{st}/{x}" for x in (pt.get("cung_story") or {}).get(h, []) if f"{st}/{x}" in theo_khoa]
    mien = nc.epic_cua(i) in (pt.get("ngoai_le_epic") or []) or any(st.startswith(t) for t in pt.get("ngoai_le_tien_to") or [])
    moc = [] if mien else [x for x in (pt.get("moc") or {}).get(h, []) if x in theo_khoa]   # mốc không có trên board: bỏ qua
    return ds + moc


def G4(nc):
    """Lá Closed thì mọi phụ thuộc (cùng story, mốc) đã Closed với Done Date không sau Done Date của lá."""
    x, ra = nc.cfg["status_xong"], []
    theo_khoa = {nc.khoa(i): i for i in nc.song if nc.khoa(i)}
    for i in nc.song:
        if nc.f(i, "status") != x or nc.tracker(i) not in nc.cfg["tracker_la"]:
            continue
        loi = []
        for k in _phu_thuoc(nc, i, theo_khoa):
            d = theo_khoa.get(k)
            if d is None or nc.f(d, "status") != x or (nc.f(d, "xong") or "9") > (nc.f(i, "xong") or ""):
                loi.append(f"{k} ({'không có' if d is None else nc.f(d, 'status')}, Done {nc.f(d, 'xong') if d else None})")
        if loi:
            ra.append(ph("G4", i, f"Closed {nc.f(i, 'xong')} trước phụ thuộc: " + "; ".join(loi)))
    return ra


def H1(nc):
    x = nc.cfg["status_xong"]
    return [ph("H1", i, f"hạn {nc.f(i, 'han')} trước ngày xét {nc.ngay_xet}, Status {nc.f(i, 'status')}") for i in nc.song
            if nc.f(i, "han") is not None and nc.f(i, "status") != x and nc.f(i, "han") < nc.ngay_xet]


def H2(nc):
    return [ph("H2", i, f"Done Date {nc.f(i, 'xong')} sau hạn {nc.f(i, 'han')}") for i in nc.song
            if nc.f(i, "xong") is not None and nc.f(i, "han") is not None and nc.f(i, "xong") > nc.f(i, "han")]


LUAT = {"G1": G1, "G2": G2, "G3": G3, "G4": G4, "H1": H1, "H2": H2}

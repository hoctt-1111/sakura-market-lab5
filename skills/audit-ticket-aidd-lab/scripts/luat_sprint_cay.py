"""Luật sprint (B1–B4) và nhất quán cha–con (D1–D3); gộp vào `luat_field.LUAT`. B1 cần kế hoạch sprint (`nguon_ngoai`)."""
from audit_lib import ph


def B1(nc):
    """Có Sprint khi và chỉ khi khoá có trong kế hoạch; tên Sprint, ngày bắt đầu, hạn khớp kế hoạch."""
    ra, ten = [], nc.plan["sprint"]
    for i in nc.song:
        sp, m = nc.f(i, "sprint"), nc.plan["muc"].get(nc.khoa(i))
        if (sp is not None) != (m is not None):
            ra.append(ph("B1", i, "có Sprint mà ngoài kế hoạch" if sp else "trong kế hoạch mà chưa gán Sprint"))
        elif m and (sp, nc.f(i, "bat_dau"), nc.f(i, "han")) != (ten, m["start"], m["due"]):
            ra.append(ph("B1", i, f"{sp} {nc.f(i, 'bat_dau')}→{nc.f(i, 'han')}, kế hoạch {ten} {m['start']}→{m['due']}"))
    return ra


def B2(nc):
    return [ph("B2", i, f"{nc.tracker(i)} không nhận Sprint") for i in nc.song
            if nc.f(i, "sprint") is not None and nc.tracker(i) not in nc.cfg["tracker_sprint"]]


def B3(nc):
    ra = []
    for i in nc.song:
        if nc.f(i, "sprint") is None:
            continue
        bd, h = nc.f(i, "bat_dau"), nc.f(i, "han")
        if nc.f(i, "owner") is None or bd is None or h is None or bd > h:
            ra.append(ph("B3", i, f"Owner {nc.f(i, 'owner')}, bắt đầu {bd}, hạn {h}"))
    return ra


def B4(nc):
    tong = {}
    for i in nc.song:
        if (sp := nc.f(i, "sprint")) is not None:
            k = (nc.f(i, "owner"), sp)
            tong[k] = tong.get(k, 0) + (nc.f(i, "uoc") or 0)
    return [ph("B4", None, f"{g:g} giờ > trần {nc.tran(o):.1f}", khoa=f"{o}|{sp}")
            for (o, sp), g in sorted(tong.items(), key=str) if nc.tran(o) is not None and g > nc.tran(o) + 1e-9]


def D1(nc):
    """Story Point, Estimated time của cha bằng tổng con sống; Spent time bằng tổng khi có con đã ghi."""
    ra = []
    for i in nc.song:
        con = nc.con_song(i)
        if not con:
            continue
        lech = []
        for t in ("point", "uoc", "da_lam"):
            v = [nc.f(c, t) for c in con if nc.f(c, t) is not None]
            if t == "da_lam" and not v:
                continue
            if abs(sum(v) - (nc.f(i, t) or 0)) > 0.01:
                lech.append(f"{nc.cfg['field_map'][t]} {nc.f(i, t)} ≠ tổng con {sum(v):g}")
        if lech:
            ra.append(ph("D1", i, "; ".join(lech)))
    return ra


def _suy(nc, con: list[dict]) -> str:
    return "New" if all(nc.f(c, "status") in nc.cfg["status_chua_lam"] for c in con) else "In Progress"


def D2(nc):
    """Status epic, story = New khi mọi con chưa làm, ngược lại In Progress; không Closed khi chưa nghiệm thu."""
    return [ph("D2", i, f"Status {nc.f(i, 'status')}, suy từ con: {d}") for i in nc.song
            if nc.tracker(i) in ("epic", "story") and nc.f(i, "status") != (d := _suy(nc, nc.con_song(i)))]


def D3(nc):
    """Sub-issues progress của GitHub (đếm cả con đã đóng) khớp số con thật trong ảnh chụp."""
    return [ph("D3", i, f"GitHub ghi {(i.get('con') or {}).get('total', 0)} con, ảnh chụp có {len(nc.con_tat_ca.get(i['so'], []))}")
            for i in nc.song if (i.get("con") or {}).get("total", 0) != len(nc.con_tat_ca.get(i["so"], []))]


LUAT = {"B1": B1, "B2": B2, "B3": B3, "B4": B4, "D1": D1, "D2": D2, "D3": D3}

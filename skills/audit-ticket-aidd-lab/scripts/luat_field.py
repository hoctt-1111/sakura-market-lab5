"""Luật field và nhãn (C, D4, L1, L2) + gộp luật sprint và tổng cha (B, D1–D3) từ `luat_sprint_cay`.
Khuôn tiêu đề, nhãn type/team, Priority, luồng Status, Owner theo bộ phận/miền/ngoại lệ, trần một sprint, nhãn ràng buộc."""
import re

import luat_sprint_cay
from audit_lib import hau_to, ph, story_cua_la


def C1(nc):
    return [ph("C1", i, f"tiêu đề không theo khuôn [TRACKER] KHOÁ hoặc tracker lạ: «{i['title'][:40]}»")
            for i in nc.song if nc.tracker(i) is None or nc.khoa(i) is None]


def _khoa_dung(nc, t: str, k: str) -> bool:
    c = nc.cfg
    if t == "epic":
        return re.match(c["epic_re"], k) is not None
    if t in ("story", "investigation"):
        return re.match(c["story_re"], k) is not None
    h, st = hau_to(k), story_cua_la(k)
    return c["la_hau_to"].get(h) == t and st is not None and re.match(c["story_re"], st) is not None


def C2(nc):
    return [ph("C2", i, f"khoá {nc.khoa(i)} sai khuôn của {nc.tracker(i)}") for i in nc.song
            if nc.tracker(i) and nc.khoa(i) and not _khoa_dung(nc, nc.tracker(i), nc.khoa(i))]


def _nhan(i, tien_to: str) -> list[str]:
    return [n for n in i.get("labels") or [] if n.startswith(tien_to)]


def _team(i) -> list[str]:
    return _nhan(i, "team:")


def C3(nc):
    ra = []
    for i in nc.song:
        h = hau_to(nc.khoa(i))
        if nc.tracker(i) in nc.cfg["tracker_la"] and (can := nc.cfg["nhan_team"].get(h)) and _team(i) != [can]:
            ra.append(ph("C3", i, f"lá {h} cần đúng nhãn {can}, đang có {_team(i) or 'không'}"))
    return ra


def C3b(nc):
    return [ph("C3b", i, "lá kiểm thử không có nhãn team") for i in nc.song
            if nc.tracker(i) == "testdesign" and not _team(i)]


def C4(nc):
    ra = []
    for i in nc.song:
        t = nc.tracker(i)
        ty = _nhan(i, "type:")
        if t and ty != [nc.cfg["nhan_type"][t]]:
            ra.append(ph("C4", i, f"nhãn type {ty or 'không có'}, cần {nc.cfg['nhan_type'][t]}"))
    return ra


def C5(nc):
    ra = []
    for i in nc.song:
        thieu = [nc.cfg["field_map"][t] for t in ("status", "priority", "owner", "point", "uoc") if nc.f(i, t) is None]
        thieu += [] if i.get("assignees") else ["người phụ trách"]
        if thieu:
            ra.append(ph("C5", i, "thiếu " + ", ".join(thieu)))
    return ra


def C6(nc):
    c, ra = nc.cfg, []
    for i in nc.song:
        p = nc.f(i, "priority")
        if p is None:
            continue
        uu = nc.epic_cua(i) in c["epic_uu_tien"] or bool(_nhan(i, c["nhan_rang_buoc_tien_to"]))
        if p not in c["priority"]:
            ra.append(ph("C6", i, f"Priority {p} ngoài {c['priority']}"))
        elif uu and p not in c["priority_cao"]:
            ra.append(ph("C6", i, f"ràng buộc đặc thù hoặc epic ưu tiên mà Priority {p}"))
    return ra


def C7(nc):
    c, ra = nc.cfg, []
    for i in nc.song:
        s = nc.f(i, "status")
        if s is not None and s not in c["status_luong"]:
            ra.append(ph("C7", i, f"Status {s} ngoài luồng {c['status_luong']}"))
        elif s in c["status_chi_test"] and nc.tracker(i) != "testdesign":
            ra.append(ph("C7", i, f"Status {s} chỉ dành cho lá kiểm thử"))
    return ra


def _owner_dung(nc, i) -> list[str] | None:
    """Owner hợp lệ của item theo thứ tự luật sinh seed: ngoại lệ (khoá story đầy đủ rồi tiền tố) → luật chuỗi →
    danh sách chuyển cân tải → miền theo epic. None = không có luật (story, tracker lạ)."""
    o, t, k = nc.cfg["owner"], nc.tracker(i), nc.khoa(i)
    if t == "epic":
        return [o["epic"]]
    if t == "investigation":
        return list(o["investigation"])
    h, st = hau_to(k), story_cua_la(k)
    if t not in nc.cfg["tracker_la"] or h not in o["la"]:
        return None
    nl, v = o.get("ngoai_le") or {}, o["la"][h]
    if ngoai := (nl.get(st) or {}).get(h) or (nl.get(st.split("-")[0]) or {}).get(h):
        return [ngoai]
    if isinstance(v, str):
        return [v]
    if chuyen := next((c["sang"] for c in o.get("chuyen") or [] if c["story"] == st and h in c["loai"]), None):
        return [chuyen]
    return [v["giao_dich"] if nc.epic_cua(i) in o["mien"]["giao_dich"] else v["tai_chinh_nen"]]


def D4(nc):
    return [ph("D4", i, f"Owner {nc.f(i, 'owner')}, luật cho {d}") for i in nc.song
            if (d := _owner_dung(nc, i)) is not None and nc.f(i, "owner") is not None and nc.f(i, "owner") not in d]


def L1(nc):
    ra = []
    for i in nc.song:
        g, tr = nc.f(i, "uoc"), nc.tran(nc.f(i, "owner"))
        if nc.tracker(i) in nc.cfg["tracker_sprint"] and g is not None and tr is not None and g > tr + 1e-9:
            ra.append(ph("L1", i, f"giờ ước {g} > trần một sprint {tr:.1f} của {nc.f(i, 'owner')}"))
    return ra


def L2(nc):
    tt, ra = nc.cfg["nhan_rang_buoc_tien_to"], []
    for s in nc.song:
        if nc.tracker(s) != "story":
            continue
        rb = set(_nhan(s, tt))
        for c in nc.con_song(s):
            if thieu := rb - set(c.get("labels") or []):
                ra.append(ph("L2", c, f"thiếu nhãn ràng buộc của story: {sorted(thieu)}"))
    return ra


LUAT = {"C1": C1, "C2": C2, "C3": C3, "C3b": C3b, "C4": C4, "C5": C5, "C6": C6, "C7": C7, "D4": D4, "L1": L1, "L2": L2,
        **luat_sprint_cay.LUAT}

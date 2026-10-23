"""Luật cấu trúc (A, E, F, L3): đủ và đúng issue so seed, tầng cha–con, bản thay thế, trùng khoá, Project public.
Mỗi hàm nhận NguCanh, trả danh sách phát hiện; A1, E2 cần seed (`nguon_ngoai: seed`)."""
from audit_lib import ph


def A1(nc):
    """Khoá seed thiếu issue sống, hoặc issue sống có khoá không có trong seed (lạ)."""
    co = {nc.khoa(i) for i in nc.song}
    ra = [ph("A1", i, f"khoá {nc.khoa(i)} không có trong seed") for i in nc.song if nc.khoa(i) not in nc.seed]
    return ra + [ph("A1", None, "khoá seed không có issue sống trên board", khoa=k) for k in nc.seed if k not in co]


def A2(nc):
    """Epic không có story; story không có con; điều tra lại có con (chỉ đếm con sống)."""
    ra = []
    for i in nc.song:
        t, con = nc.tracker(i), nc.con_song(i)
        if t == "epic" and not any(nc.tracker(c) == "story" for c in con):
            ra.append(ph("A2", i, "epic không có story"))
        elif t == "story" and not con:
            ra.append(ph("A2", i, "story không có sub-issue"))
        elif t == "investigation" and con:
            ra.append(ph("A2", i, f"điều tra có {len(con)} con"))
    return ra


def A3(nc):
    """Bản thay thế: Status phải là trạng thái xong, không giữ Sprint, ngày bắt đầu, hạn, giờ đã làm, Done Date; nhãn thay thế mà còn mở."""
    ra, nhan = [], nc.cfg["nhan_thay_the"]
    for i in nc.thay:
        loi = [] if nc.f(i, "status") == nc.cfg["status_xong"] else [f"Status {nc.f(i, 'status')}"]
        loi += [nc.cfg["field_map"][t] for t in ("sprint", "bat_dau", "han", "da_lam", "xong") if nc.f(i, t) is not None]
        if loi:
            ra.append(ph("A3", i, "bản thay thế đã đóng còn giữ: " + ", ".join(loi)))
    return ra + [ph("A3", i, f"mang nhãn {nhan} nhưng issue còn mở") for i in nc.song if nhan in (i.get("labels") or [])]


def E1(nc):
    """Mọi item trừ epic có cha, cha đúng tầng theo `cha_hop_le`."""
    ra = []
    for i in nc.song:
        t = nc.tracker(i)
        if t in (None, "epic"):
            continue
        cha = nc.theo_so.get(i.get("cha"))
        if cha is None:
            ra.append(ph("E1", i, "không có cha (mồ côi)"))
        elif nc.tracker(cha) not in nc.cfg["cha_hop_le"].get(t, []):
            ra.append(ph("E1", i, f"cha #{cha['so']} là {nc.tracker(cha)}, {t} phải nằm dưới {nc.cfg['cha_hop_le'].get(t)}"))
    return ra


def E2(nc):
    """Item có trong seed nằm dưới epic khác epic của seed (đi theo chuỗi cha)."""
    ra = []
    for i in nc.song:
        k = nc.khoa(i)
        if nc.tracker(i) == "epic" or k not in nc.seed:
            continue
        ep = nc.epic_cua(i)
        if ep is not None and ep != nc.seed[k]:
            ra.append(ph("E2", i, f"nằm dưới epic {ep}, seed ghi {nc.seed[k]}"))
    return ra


def E3(nc):
    """Không cha nào quá 100 con (giới hạn sub-issue của GitHub, đếm cả con đã đóng)."""
    return [ph("E3", nc.theo_so[so], f"{len(c)} con > 100") for so, c in nc.con_tat_ca.items()
            if len(c) > 100 and so in nc.theo_so]


def F1(nc):
    """Hai issue sống cùng khoá: báo mọi issue trong nhóm."""
    nhom = {}
    for i in nc.song:
        if (k := nc.khoa(i)) is not None:
            nhom.setdefault(k, []).append(i)
    return [ph("F1", i, f"khoá {k} có {len(ds)} issue sống: " + ", ".join(f"#{x['so']}" for x in ds))
            for k, ds in nhom.items() if len(ds) > 1 for i in ds]


def L3(nc):
    """Project public; mọi field trong `field_map` có trên Project."""
    pj = nc.anh.get("project") or {}
    ra = [] if pj.get("public") is True else [ph("L3", None, "Project chưa public", khoa="project.public")]
    co = set(pj.get("fields") or [])
    return ra + [ph("L3", None, f"Project thiếu field «{t}»", khoa=f"field:{t}")
                 for t in nc.cfg["field_map"].values() if t not in co]


LUAT = {"A1": A1, "A2": A2, "A3": A3, "E1": E1, "E2": E2, "E3": E3, "F1": F1, "L3": L3}

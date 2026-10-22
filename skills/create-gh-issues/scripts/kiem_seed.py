"""`check --seed`: seed đúng tầng epic → story/điều tra → leaf trước khi đẩy; team.yaml khớp field và lựa chọn của Project.

Kiểm: tên file = key epic · key duy nhất · title khớp `^\\[[A-Z ]+\\] (\\S+) ` với key là từ thứ hai · `cha` tồn tại và đúng
tầng · ≤ 100 con mỗi cha (trần sub-issue của GitHub) · story không leaf = 0 · nhãn ⊆ labels.yaml · Owner/Priority có trong
team.yaml · (có field-list.json) tên field và lựa chọn Owner/Priority/Status có trên Project · `--so`: trường phi-văn so với
bản sao lưu (mọi trường trừ 5 trường văn, gap_refs, premise_refs).
"""
import re

from lib import LoiBoSinh
from seed_doc import LEAF_LOAI, LEAF_TRACKER, MANG_THEO, REF_GOC, TIEN_TO, TITLE_RE, cac_ban_ghi, tieu_de

EPIC_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
STORY_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
TRAN_CON = 100
TANG_STORY = ("story", "investigation")
TRUONG = ("key", "tracker", "title_vi", "spec_refs", "labels", "owner", "priority") + MANG_THEO


def _kiem_ban_ghi(f: str, it: dict, kq, nhan_hop_le, owner_hop_le, prio_hop_le) -> None:
    k, noi = it.get("key", "?"), f"backlog/{f}.yaml"
    if thieu := [t for t in TRUONG if t not in it]:
        kq.vi_pham(noi, None, f"{k}: thiếu trường {thieu}")
        return
    if it["tracker"] not in TIEN_TO:
        kq.vi_pham(noi, None, f"{k}: tracker lạ `{it['tracker']}`")
        return
    tv = str(it["title_vi"])
    m = TITLE_RE.match(tieu_de(it["tracker"], k, tv))
    if not tv.strip() or "\n" in tv or not m or m.group(1) != k:
        kq.vi_pham(noi, None, f"{k}: title không khớp `^\\[[A-Z ]+\\] (\\S+) ` hoặc key thứ hai ≠ key")
    if f"type:{it['tracker']}" not in it["labels"]:
        kq.vi_pham(noi, None, f"{k}: thiếu nhãn type:{it['tracker']}")
    if nhan_hop_le is not None and (la := sorted(set(it["labels"]) - nhan_hop_le)):
        kq.vi_pham(noi, None, f"{k}: nhãn không có trong labels.yaml {la}")
    if owner_hop_le is not None and it["owner"] not in owner_hop_le:
        kq.vi_pham(noi, None, f"{k}: owner `{it['owner']}` không có trong team.yaml")
    if prio_hop_le is not None and it["priority"] not in prio_hop_le:
        kq.vi_pham(noi, None, f"{k}: priority `{it['priority']}` không có trong team.yaml › priority_map")
    if not isinstance(it["spec_refs"], dict) or any(not isinstance(it["spec_refs"].get(r), list) for r in REF_GOC):
        kq.vi_pham(noi, None, f"{k}: spec_refs thiếu một trong {REF_GOC} (dạng danh sách)")


def gia_tri(d) -> set:
    return {x for v in d.values() for x in (gia_tri(v) if isinstance(v, dict) else {v})}


def kiem_seed(seed: dict, kq, nhan_hop_le=None, team=None) -> dict:
    """Kiểm cấu trúc; trả về số đếm {epic, story, inv, leaf, khong_leaf} cho dòng tóm tắt."""
    owner_hop_le = prio_hop_le = None
    if team is not None:
        owner_hop_le = gia_tri(team["owner_theo_tracker"]) | gia_tri(team["owner_theo_leaf"])
        prio_hop_le = set(team["priority_map"])
    dem, theo_key, con = {"epic": 0, "story": 0, "inv": 0, "leaf": 0, "khong_leaf": 0}, {}, {}
    for f, it in cac_ban_ghi(seed):
        k = it.get("key")
        if k in theo_key:
            kq.vi_pham(f"backlog/{f}.yaml", None, f"{k}: key trùng (đã có ở backlog/{theo_key[k][0]}.yaml)")
        theo_key.setdefault(k, (f, it))
        _kiem_ban_ghi(f, it, kq, nhan_hop_le, owner_hop_le, prio_hop_le)
    for f, d in seed.items():
        e = d.get("epic") or {}
        if e.get("key") != f or e.get("tracker") != "epic" or not EPIC_RE.match(f):
            kq.vi_pham(f"backlog/{f}.yaml", None, "tên file phải bằng key epic (chữ hoa, số, gạch nối) và epic.tracker = epic")
        dem["epic"] += 1
        for it in d.get("items") or []:
            _kiem_cha(f, it, theo_key, con, dem, kq)
    for cha, ds in con.items():
        if len(ds) > TRAN_CON:
            kq.vi_pham(f"backlog/{theo_key.get(cha, ('?',))[0]}.yaml", None, f"{cha}: {len(ds)} con > {TRAN_CON} (trần sub-issue)")
    for k, (f, it) in theo_key.items():
        if it.get("tracker") == "story" and not con.get(k):
            dem["khong_leaf"] += 1
            kq.vi_pham(f"backlog/{f}.yaml", None, f"{k}: story không có leaf")
    return dem


def _kiem_cha(f: str, it: dict, theo_key: dict, con: dict, dem: dict, kq) -> None:
    k, tr, cha, noi = it.get("key"), it.get("tracker"), it.get("cha"), f"backlog/{f}.yaml"
    if tr in TANG_STORY:
        dem["inv" if tr == "investigation" else "story"] += 1
        if cha != f or not STORY_RE.match(str(k)) or "/" in str(k):
            kq.vi_pham(noi, None, f"{k}: {tr} phải có cha = epic của file ({f}) và key dạng XXX-nn")
    elif tr in ("devtask", "testdesign"):
        dem["leaf"] += 1
        loai = str(k).rsplit("/", 1)[-1]
        goc = theo_key.get(cha, (None, {}))[1]
        if (goc.get("tracker") != "story" or theo_key[cha][0] != f or k != f"{cha}/{loai}"
                or loai not in LEAF_LOAI or LEAF_TRACKER[loai] != tr):
            kq.vi_pham(noi, None, f"{k}: leaf phải có cha là story cùng file, key `<story>/<FE|BE|DB|TEST|INFRA|PM|BRSE>`"
                                  f" và tracker khớp loại (cha hiện tại: {cha})")
    else:
        kq.vi_pham(noi, None, f"{k}: tracker `{tr}` không thuộc tầng story hay leaf")
        return
    con.setdefault(cha, []).append(k)


def kiem_team(team: dict, fl: dict, kq) -> None:
    """team.yaml khớp Project thật (field-list.json): tên field, lựa chọn Owner/Priority/Status."""
    try:
        fields = {x["name"]: x for x in fl["fields"]}
    except (KeyError, TypeError) as e:
        raise LoiBoSinh(f"field-list.json hỏng: {e}") from e

    def chon(ten):
        return {o["name"] for o in fields.get(team["field_map"].get(ten, ten), {}).get("options", [])}
    for logic, ten in team["field_map"].items():
        if ten not in fields:
            kq.vi_pham("team.yaml", None, f"field_map.{logic}: field `{ten}` không có trên Project")
    if thieu := sorted((gia_tri(team["owner_theo_tracker"]) | gia_tri(team["owner_theo_leaf"])) - chon("Owner")):
        kq.vi_pham("team.yaml", None, f"Owner {thieu} không là lựa chọn của field Owner")
    if la := sorted(set(team["priority_map"].values()) - chon("Priority")):
        kq.vi_pham("team.yaml", None, f"priority_map {la} không là lựa chọn của field Priority")
    if team["status_dau"] not in chon("Status"):
        kq.vi_pham("team.yaml", None, f"status_dau `{team['status_dau']}` không là lựa chọn của field Status")


def kiem_so(seed: dict, sao_luu: dict, kq) -> int:
    """So trường phi-văn (mọi trường trừ MANG_THEO) theo key với bản sao lưu; trả về số bản ghi đổi."""
    def phi_van(s):
        return {it.get("key"): (f, {t: v for t, v in it.items() if t not in MANG_THEO}) for f, it in cac_ban_ghi(s)}
    moi, cu, doi = phi_van(seed), phi_van(sao_luu), 0
    for k in sorted(set(moi) | set(cu)):
        if k not in cu or k not in moi:
            doi += 1
            kq.vi_pham(f"backlog/{(moi.get(k) or cu.get(k))[0]}.yaml", None, f"{k}: {'thêm' if k not in cu else 'mất'} so với bản sao lưu")
        elif moi[k][1] != cu[k][1]:
            doi += 1
            khac = sorted(t for t in set(moi[k][1]) | set(cu[k][1]) if moi[k][1].get(t) != cu[k][1].get(t))
            kq.vi_pham(f"backlog/{moi[k][0]}.yaml", None, f"{k}: trường phi-văn đổi {khac}")
    return doi

"""`check --snapshot`: ảnh chụp Project (lệnh snapshot) ↔ seed ↔ board-map. Không gọi mạng.

Kiểm: Project `public: true` (bỏ qua với `check --cho-phep-rieng`) · đủ field của `team.yaml › field_map` · nhãn repo ⊇
labels.yaml · số item theo tracker bằng seed · mọi khoá seed có trên board (thiếu gộp theo epic) · không item lạ, không key
trùng · từng khoá: title, nhãn, Owner, Priority (theo priority_map), người phụ trách, cha (= số của khoá cha trên board),
không mồ côi, map khớp số, băm thân trong map bằng thân dựng lại từ seed (và bằng băm thân trên board khi ảnh chụp có
`--body`). Bản thừa đã xử lý (đã đóng, nhãn `spec-gap`, cạnh issue khác cùng key) — loại khỏi so, in riêng.
"""
import re

from lib import LoiBoSinh
from ban_do import bam_than, chon_ban_chinh, khoa_tu_title
from seed_doc import TIEN_TO, tieu_de

TRACKER = {v: k for k, v in TIEN_TO.items()}
NGUON = "board-snapshot.json"


def tracker_tu_title(title: str) -> str | None:
    m = re.match(r"^(\[[A-Z ]+\])", title or "")
    return TRACKER.get(m.group(1)) if m else None


def _chung(anh: dict, team: dict, nhan_yaml: set, kq, can_public=True) -> None:
    if can_public and anh.get("project", {}).get("public") is not True:
        kq.vi_pham(NGUON, None, "Project chưa public (public ≠ true)")
    co = set(anh.get("project", {}).get("fields") or [])
    for logic, ten in team["field_map"].items():
        if ten not in co:
            kq.vi_pham(NGUON, None, f"Project thiếu field `{ten}` (field_map.{logic})")
    for ten in sorted(nhan_yaml - set(anh.get("repo", {}).get("labels") or [])):
        kq.vi_pham(NGUON, None, f"repo thiếu nhãn `{ten}` của labels.yaml")


def _gom_board(anh: dict, tat_ca: dict, kq, dem) -> dict[str, list[dict]]:
    theo_key: dict[str, list[dict]] = {}
    for x in anh.get("items") or []:
        k = khoa_tu_title(x.get("title") or "")
        if x.get("loai") != "ISSUE" or k is None or k not in tat_ca:
            dem["la"] += 1
            kq.vi_pham(NGUON, None, f"item lạ: {x.get('loai')} #{x.get('so')} «{x.get('title')}» — key không có trong seed")
            continue
        theo_key.setdefault(k, []).append(x)
    for k, ds in sorted(theo_key.items()):
        chinh, thua = chon_ban_chinh(ds)
        dem["loai_bo"] += len(thua)
        if chinh is None:
            dem["trung"] += 1
            kq.vi_pham(NGUON, None, f"{k}: key trùng trên board ({', '.join('#' + str(x['so']) for x in ds)})")
        else:
            theo_key[k] = [chinh]
    return theo_key


def _mot_khoa(k, f, it, x, so_board, team, m, than_fn, kq, dem) -> None:
    def loi(loai, chi_tiet):
        dem[loai] += 1
        kq.vi_pham(f"backlog/{f}.yaml", None, f"{k} (#{x['so']}): {chi_tiet}")
    if x["title"] != (dung := tieu_de(it["tracker"], k, it["title_vi"])):
        loi("title", f"title lệch: board «{x['title']}» ≠ seed «{dung}»")
    thieu, thua = sorted(set(it["labels"]) - set(x["labels"])), sorted(set(x["labels"]) - set(it["labels"]))
    if thieu or thua:
        loi("nhan", f"nhãn lệch: thiếu {thieu} thừa {thua}")
    fm, gt = team["field_map"], x.get("field") or {}
    if gt.get(fm["Owner"]) != it["owner"]:
        loi("owner", f"Owner lệch: board {gt.get(fm['Owner'])} ≠ seed {it['owner']}")
    if gt.get(fm["Priority"]) != (p := team["priority_map"].get(it["priority"])):
        loi("priority", f"Priority lệch: board {gt.get(fm['Priority'])} ≠ seed {p}")
    if team["assignee"] not in (x.get("assignees") or []):
        loi("nguoi", f"thiếu người phụ trách {team['assignee']}")
    cha = it.get("cha")
    if cha is None and x.get("cha") is not None:
        loi("cha", f"epic không được có cha (board: #{x['cha']})")
    elif cha is not None and x.get("cha") is None:
        loi("mo_coi", "mồ côi: chưa nối cha trên board")
    elif cha is not None and x["cha"] != so_board.get(cha):
        loi("cha", f"cha lệch: board #{x['cha']} ≠ seed {cha} ({'#' + str(so_board[cha]) if cha in so_board else 'chưa có trên board'})")
    e = m.get(k)
    if e is None or e.get("so") != x["so"]:
        loi("map", f"board-map.json {'thiếu khoá' if e is None else 'ghi #' + str(e.get('so'))} — board là #{x['so']}")
    try:
        ban = bam_than(than_fn(k))
    except LoiBoSinh as er:
        loi("than", f"không dựng được thân từ seed: {er}")
        return
    if e is not None and not e.get("bam_than"):
        loi("than", "băm thân chưa ghi trong map — thân trên board chưa đẩy từ seed (đẩy lại với --cap-nhat)")
    elif e is not None and e["bam_than"] != ban:
        loi("than", "thân lệch seed: băm lúc đẩy ≠ thân dựng lại (đẩy lại với --cap-nhat)")
    if x.get("bam_than") and x["bam_than"] != ban:
        loi("than", "thân trên board khác thân dựng từ seed (sửa tay trên web? sửa seed rồi --cap-nhat)")


def kiem_anh_chup(ban_ghi: list[tuple[str, dict]], anh: dict, team: dict, nhan_yaml: set, m: dict, than_fn, kq,
                  lo: set | None = None, can_public=True) -> dict:
    """`ban_ghi` = cac_ban_ghi(seed); `lo` giới hạn phép so vào các epic đó. Trả số đếm cho dòng tóm tắt."""
    dem = dict.fromkeys(("la", "trung", "thieu", "title", "nhan", "owner", "priority", "nguoi", "cha", "mo_coi", "map",
                         "than", "loai_bo"), 0)
    _chung(anh, team, nhan_yaml, kq, can_public)
    tat_ca = {it["key"]: (f, it) for f, it in ban_ghi}
    cac = {k: v for k, v in tat_ca.items() if lo is None or v[0] in lo}
    theo_key = _gom_board(anh, tat_ca, kq, dem)
    so_board = {k: ds[0]["so"] for k, ds in theo_key.items()}
    thieu: dict[str, list[str]] = {}
    for k, (f, it) in cac.items():
        if k not in theo_key:
            thieu.setdefault(f, []).append(k)
        else:
            _mot_khoa(k, f, it, theo_key[k][0], so_board, team, m, than_fn, kq, dem)
    for f, ds in thieu.items():
        dem["thieu"] += len(ds)
        tong = sum(1 for v in cac.values() if v[0] == f)
        kq.vi_pham(f"backlog/{f}.yaml", None, f"{len(ds)}/{tong} khoá seed chưa có trên board: {', '.join(ds[:5])}"
                                              + (f" … (+{len(ds) - 5})" if len(ds) > 5 else ""))
    theo_tracker = []
    for tr in TIEN_TO:
        s = sum(1 for _, it in cac.values() if it["tracker"] == tr)
        b = sum(1 for k in theo_key if k in cac and tracker_tu_title(theo_key[k][0]["title"]) == tr)
        theo_tracker.append(f"{tr} {b}/{s}")
        if b != s:
            kq.vi_pham(NGUON, None, f"số item tracker {tr}: board {b} ≠ seed {s}")
    dem.update(board=sum(len(ds) for k, ds in theo_key.items() if k in cac), seed=len(cac),
               theo_tracker=" · ".join(theo_tracker))
    return dem

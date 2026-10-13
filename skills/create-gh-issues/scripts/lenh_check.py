"""Lệnh `check`: kiểm offline, in `✓ … PASS` hoặc `✗ … FAIL (N vi phạm)`, thoát 0 (PASS) / 1 (FAIL) / 2 (lỗi dữ liệu).

  --seed [--van] [--so <thư mục>]   seed đúng tầng (kiem_seed.py); có field-list.json thì team.yaml phải khớp Project
  --snapshot [--lo E1,E2] [--cho-phep-rieng]   ảnh chụp ↔ seed ↔ board-map (kiem_anh_chup.py); cần chạy `snapshot` trước
Hai cờ dùng chung một lần chạy được. Không gọi mạng.
"""
from pathlib import Path

import kiem_seed as luat
import than_issue
from kiem_anh_chup import kiem_anh_chup
from kiem_van import kiem_van
from lib import KetQua, LoiBoSinh, doc_json, doc_yaml
from seed_doc import cac_ban_ghi, doc_seed


def kiem(cfg, van=False, so: Path | None = None, kq: KetQua | None = None) -> KetQua:
    kq = kq or KetQua("check-seed", "seed đúng tầng, cha, regex, leaf" + (", văn" if van else "") + (", phi-văn" if so else ""),
                      cfg.seed_dir)
    seed, team = doc_seed(cfg.backlog), doc_yaml(cfg.team)
    nhan = {x["ten"] for x in doc_yaml(cfg.labels)["nhan"]}
    dem = luat.kiem_seed(seed, kq, nhan, team)
    if cfg.evidence_dir and cfg.field_list_file.is_file():
        luat.kiem_team(team, doc_json(cfg.field_list_file), kq)
    else:
        kq.ghi_chu.append("check --seed: chưa có field-list.json — bỏ qua khớp team.yaml với Project (chạy push --dry-run một lần)")
    kq.ghi_chu.append(f"check --seed: {dem['epic']} epic · {dem['story']} story · {dem['inv']} điều tra · "
                      f"{dem['leaf']} leaf · story không leaf = {dem['khong_leaf']}")
    if so is not None:
        doi = luat.kiem_so(seed, doc_seed(so), kq)
        kq.ghi_chu.append(f"check --so {so}: {doi} bản ghi đổi trường phi-văn")
    if van:
        v = cfg.van or {}
        dat = kiem_van(seed, kq, team, int((cfg.than or {}).get("tran", 65536)), v.get("khoang"), v.get("can_chu"))
        kq.ghi_chu.append(f"check --van: {dat}/{len(cac_ban_ghi(seed))} bản ghi đủ văn")
    return kq


def kiem_snapshot(cfg, lo=None, kq: KetQua | None = None, than_fn=None, can_public=True) -> KetQua:
    """Ảnh chụp ↔ seed. `than_fn(key)` dựng thân; mặc định than_issue.than với ctx nạp một lần."""
    kq = kq or KetQua("check-snapshot", "ảnh chụp Project ↔ seed ↔ board-map", cfg.seed_dir)
    team, nhan = doc_yaml(cfg.team), {x["ten"] for x in doc_yaml(cfg.labels)["nhan"]}
    if not cfg.snap_file.is_file():
        raise LoiBoSinh(f"thiếu {cfg.snap_file} — chạy lệnh snapshot trước")
    anh = doc_json(cfg.snap_file)
    if than_fn is None:
        ctx = than_issue.nap_ctx(cfg)
        than_fn = lambda k: than_issue.than(k, ctx)  # noqa: E731
    dem = kiem_anh_chup(cac_ban_ghi(doc_seed(cfg.backlog)), anh, team, nhan, doc_json(cfg.map_file, {}), than_fn, kq,
                        set(lo) if lo else None, can_public)
    kq.ghi_chu.append(f"check --snapshot ({anh.get('chup_luc')}{', lô ' + ','.join(lo) if lo else ''}): board {dem['board']} item"
                      f" · seed {dem['seed']} khoá · thiếu {dem['thieu']} · lạ {dem['la']} · trùng {dem['trung']} · lệch title"
                      f" {dem['title']} · nhãn {dem['nhan']} · Owner {dem['owner']} · Priority {dem['priority']} · người phụ trách"
                      f" {dem['nguoi']} · cha {dem['cha']} · mồ côi {dem['mo_coi']} · map {dem['map']} · thân {dem['than']}"
                      + (f" · đã đóng loại khỏi so {dem['loai_bo']}" if dem["loai_bo"] else ""))
    kq.ghi_chu.append(f"check --snapshot theo tracker (board/seed): {dem['theo_tracker']}")
    return kq


def main(a, cfg) -> int:
    if not (a.seed or a.snapshot):
        raise LoiBoSinh("check cần --seed và/hoặc --snapshot")
    cfg.can("seed_dir")
    if a.so and not Path(a.so).is_dir():
        raise LoiBoSinh(f"--so: không có thư mục {a.so}")
    lo = [x.strip() for x in a.lo.split(",") if x.strip()] if a.lo else None
    kq = kiem(cfg, a.van, Path(a.so) if a.so else None) if a.seed else None
    if a.snapshot:
        cfg.can("evidence_dir")
        kq = kiem_snapshot(cfg, lo, kq, can_public=not a.cho_phep_rieng)
    return 0 if kq.in_ra() else 1

"""Lệnh `labels`: tạo (hoặc cập nhật màu, mô tả) nhãn repo từ `labels.yaml › nhan[]{ten, mau, mo_ta}`.

Mỗi nhãn một lệnh `gh label create <ten> --repo <repo> --color <mau> --description <mo_ta> --force` (`--force` = có rồi thì
cập nhật, không xoá nhãn nào). Không có `--create` thì chỉ in lệnh sẽ chạy. Nhịp: nghỉ 60/nhip_phut giây giữa hai lệnh.
"""
import subprocess
import time

from lib import LoiBoSinh, doc_yaml


def lenh_nhan(cfg) -> list[list[str]]:
    ds = (doc_yaml(cfg.labels) or {}).get("nhan") or []
    if bad := [x for x in ds if not x.get("ten") or not str(x.get("mau", "")).strip()]:
        raise LoiBoSinh(f"{cfg.labels}: nhãn thiếu `ten` hoặc `mau`: {bad[:3]}")
    return [["gh", "label", "create", str(x["ten"]), "--repo", cfg.repo, "--color", str(x["mau"]).lstrip("#"),
             "--description", str(x.get("mo_ta") or ""), "--force"] for x in ds]


def main(a, cfg, runner=subprocess.run, sleep=time.sleep) -> int:
    cfg.can("repo", "seed_dir")
    ds = lenh_nhan(cfg)
    if not a.create:
        for l in ds:
            print("  (chưa chạy) " + " ".join(l[:8]) + " --description … --force")
        print(f"labels: {len(ds)} nhãn — thêm --create để tạo thật trên {cfg.repo}")
        return 0
    loi = 0
    for i, l in enumerate(ds):
        if i:
            sleep(60 / max(1, cfg.nhip_phut))
        r = runner(l, capture_output=True, text=True)
        if r.returncode != 0:
            loi += 1
            print(f"✗ {l[3]}: {(r.stderr or r.stdout).strip().splitlines()[:1]}")
    print(f"labels: tạo/cập nhật {len(ds) - loi}/{len(ds)} nhãn trên {cfg.repo}" + (f" · lỗi {loi}" if loi else ""))
    return 1 if loi else 0

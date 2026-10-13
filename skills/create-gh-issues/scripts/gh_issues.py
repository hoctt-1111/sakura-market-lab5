#!/usr/bin/env python3
"""create-gh-issues: tạo issue GitHub từ seed YAML, nối sub-issue, đặt field Project v2; chụp và kiểm board.

Dùng: gh_issues.py <lệnh> [tham số chung] [tham số riêng]
  push      --lo E1[,E2…] [--dry-run] [--ghi-than] [--da-quet] [--lenh-quet "…"] [--cap-nhat] [--chi-field]
  snapshot  [--body] [--out <file>]
  check     --seed [--van] [--so <thư mục>] · --snapshot [--lo …] [--cho-phep-rieng]
  render    --key <key>
  labels    [--create]
Thoát: 0 xong/PASS · 1 lỗi GitHub, FAIL hoặc từ chối đăng · 2 lỗi dữ liệu/tham số · 3 cờ PUSH_RUNNING đang có.
"""
import argparse
import sys

import cau_hinh
import lenh_check
import lenh_labels
import lenh_push
import lenh_snapshot
from gh_api import LoiGh
from lib import LoiBoSinh
from than_issue import nap_ctx, than


def _chung() -> argparse.ArgumentParser:
    c = argparse.ArgumentParser(add_help=False)
    g = c.add_argument_group("tham số chung (đè khoá cùng tên trong --config)")
    g.add_argument("--config", help="file YAML chứa các khoá dưới đây (+ than, spec, van)")
    g.add_argument("--repo", help="owner/name của repo chứa issue")
    g.add_argument("--project-owner", help="login user hoặc org sở hữu Project v2")
    g.add_argument("--project-number", type=int, help="số Project (trong URL …/projects/<số>)")
    g.add_argument("--seed-dir", help="thư mục có backlog/*.yaml, team.yaml, labels.yaml (+ premise.yaml, gaps.yaml)")
    g.add_argument("--evidence-dir", help="thư mục board-map.json, field-list.json, snapshot, log, thân, cờ")
    g.add_argument("--khuon", help="khuôn issue Markdown (thứ tự mục thân); mặc định thứ tự của templates/khuon-issue.md")
    g.add_argument("--spec-registry", help="(tuỳ chọn) registry spec để in mã spec và khối «Dữ liệu từ spec»")
    g.add_argument("--than-dir", help="nơi ghi thân để quét (mặc định <evidence-dir>/bodies)")
    g.add_argument("--log-dir", help="nhật ký JSONL từng lệnh gh (mặc định <evidence-dir>/log)")
    g.add_argument("--co-chan", action="append", help="file cờ: còn tồn tại thì dừng (mặc định <evidence-dir>/BREAK_RUNNING)")
    g.add_argument("--nhip-phut", type=int, help="trần lệnh ghi mỗi phút (mặc định 40)")
    g.add_argument("--nhip-gio", type=int, help="trần lệnh ghi mỗi giờ (mặc định 450)")
    return c


def tao_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="gh_issues.py", description=__doc__.split("\n")[0])
    sub, c = ap.add_subparsers(dest="lenh", required=True), _chung()
    p = sub.add_parser("push", parents=[c], help="đẩy seed theo lô epic")
    p.add_argument("--lo", required=True, help="danh sách epic, ngăn bằng dấu phẩy (E15,FG-09)")
    for co, y in (("--dry-run", "không chạy lệnh ghi"), ("--cap-nhat", "PATCH issue có thân/nhãn lệch seed"),
                  ("--chi-field", "chỉ đặt lại field Project"), ("--ghi-than", "ghi thân để quét (cùng --dry-run)"),
                  ("--da-quet", "xác nhận thân đã qua gate quét của dự án"), ("--doc-lai-field", "đọc lại field-list")):
        p.add_argument(co, action="store_true", help=y)
    p.add_argument("--lenh-quet", action="append", help="lệnh gate chạy trước khi đăng, phải thoát 0 (lặp được)")
    p.add_argument("--field", default=",".join(cau_hinh.FIELD_DAT), help="field đặt khi đẩy (khoá logic team.yaml)")
    s = sub.add_parser("snapshot", parents=[c], help="chụp Project (chỉ đọc)")
    s.add_argument("--body", action="store_true", help="thêm băm thân issue")
    s.add_argument("--out", help="file ra (mặc định <evidence-dir>/board-snapshot.json)")
    s.add_argument("--doc-lai-field", action="store_true")
    k = sub.add_parser("check", parents=[c], help="kiểm seed / ảnh chụp, không gọi mạng")
    for co in ("--seed", "--van", "--snapshot", "--cho-phep-rieng"):
        k.add_argument(co, action="store_true")
    k.add_argument("--so", help="thư mục backlog sao lưu để so trường phi-văn")
    k.add_argument("--lo", help="chỉ so các epic này (cùng --snapshot)")
    r = sub.add_parser("render", parents=[c], help="in thân issue của một khoá")
    r.add_argument("--key", required=True)
    n = sub.add_parser("labels", parents=[c], help="tạo nhãn repo từ labels.yaml")
    n.add_argument("--create", action="store_true", help="chạy thật gh label create --force")
    return ap


def render(a, cfg) -> int:
    cfg.can("seed_dir")
    print(than(a.key, nap_ctx(cfg)))
    return 0


LENH = {"push": lenh_push.main, "snapshot": lenh_snapshot.main, "check": lenh_check.main, "render": render,
        "labels": lenh_labels.main}


def main(argv=None) -> int:
    a = tao_parser().parse_args(argv)
    try:
        return LENH[a.lenh](a, cau_hinh.tu_args(a))
    except LoiBoSinh as e:
        print(f"✗ lỗi dữ liệu: {e}")
        return 2
    except LoiGh as e:
        print(f"✗ GitHub: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

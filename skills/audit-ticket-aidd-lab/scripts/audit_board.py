"""audit-ticket-aidd-lab — audit ticket trên GitHub Project v2 theo bảng tiêu chí YAML. Chỉ đọc, không sửa board.
Lệnh: snapshot (chụp Project bằng `gh api graphql`) · audit (ảnh chụp → báo cáo HTML, hoặc Markdown khi --out *.md;
không mạng) · tieu-chi (in bảng).
Dùng: audit_board.py snapshot --config c.yaml --out anh.json
      audit_board.py audit --snapshot anh.json --config c.yaml --tieu-chi t.yaml [--seed-dir d] [--sprint-plan f]
                     [--phu-thuoc f] [--ngay-xet YYYY-MM-DD] [--out bao-cao-audit.html]
      audit_board.py tieu-chi --tieu-chi t.yaml [--out tieu-chi.md]"""
import argparse
import sys
from pathlib import Path

import bao_cao
import bao_cao_html
import luat_cau_truc
import luat_field
import luat_trang_thai
from audit_lib import LoiBoSinh, doc_yaml, ghi_text
from ngu_canh import NguCanh

GOC = Path(__file__).resolve().parents[1]
LUAT = {**luat_cau_truc.LUAT, **luat_field.LUAT, **luat_trang_thai.LUAT}
NGUON = {"seed": "seed", "sprint_plan": "plan", "phu_thuoc": "pt"}


def chay(nc: NguCanh) -> dict:
    """{phat_hien, bo_qua, khong_ap_dung}; mức lấy từ YAML (YAML thắng mã); mã áp dụng thiếu hàm → LoiBoSinh."""
    ds = nc.tc["tieu_chi"]
    if thieu := [t["ma"] for t in ds if t["ap_dung"] and t["ma"] not in LUAT]:
        raise LoiBoSinh(f"tiêu chí áp dụng chưa có hàm luật: {thieu}")
    ph, bo_qua = [], []
    for t in (t for t in ds if t["ap_dung"]):
        ngoai = t.get("nguon_ngoai")
        if ngoai and getattr(nc, NGUON[ngoai]) is None:
            bo_qua.append(t["ma"])
            continue
        ph += [{**p, "muc": t["muc"]} for p in LUAT[t["ma"]](nc)]
    return {"phat_hien": ph, "bo_qua": bo_qua, "khong_ap_dung": [t for t in ds if not t["ap_dung"]]}


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="audit_board.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="lenh", required=True)
    s = sub.add_parser("snapshot", help="chụp Project (chỉ đọc, cần gh đã đăng nhập)")
    s.add_argument("--config", default=str(GOC / "config" / "lab5.yaml"))
    s.add_argument("--out", required=True)
    a = sub.add_parser("audit", help="ảnh chụp → báo cáo HTML (mặc định) hoặc Markdown (--out *.md)")
    a.add_argument("--snapshot", required=True)
    a.add_argument("--config", default=str(GOC / "config" / "lab5.yaml"))
    a.add_argument("--tieu-chi", default=str(GOC / "tieu-chi.yaml"))
    for k in ("--seed-dir", "--sprint-plan", "--phu-thuoc", "--ngay-xet"):
        a.add_argument(k)
    a.add_argument("--out", default="bao-cao-audit.html", help="đuôi .md → Markdown, khác → HTML")
    t = sub.add_parser("tieu-chi", help="in bảng tiêu chí Markdown")
    t.add_argument("--tieu-chi", default=str(GOC / "tieu-chi.yaml"))
    t.add_argument("--out")
    return ap


def main(argv=None) -> int:
    a = _parser().parse_args(argv)
    try:
        if a.lenh == "snapshot":
            import chup
            anh = chup.chup(doc_yaml(a.config))
            ghi_text(a.out, chup.json_dep(anh))
            print(f"đã chụp {len(anh['items'])} item → {a.out}")
            return 0
        if a.lenh == "tieu-chi":
            md = bao_cao.bang_tieu_chi(doc_yaml(a.tieu_chi))
        else:
            nc = NguCanh.tao(a.snapshot, a.config, a.tieu_chi, a.seed_dir, a.sprint_plan, a.phu_thuoc, a.ngay_xet)
            kq = chay(nc)
            md = bao_cao.dung(nc, kq) if a.out.lower().endswith(".md") else bao_cao_html.dung(nc, kq)
            print(bao_cao.dong_tom(kq) + f" → {a.out}")
        if a.out:
            ghi_text(a.out, md)
        else:
            print(md)
        return 0
    except LoiBoSinh as e:
        print(f"LỖI: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

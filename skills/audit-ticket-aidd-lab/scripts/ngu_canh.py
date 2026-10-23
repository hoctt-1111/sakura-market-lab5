"""Ngữ cảnh audit: ảnh chụp Project + cấu hình + tiêu chí (+ seed, kế hoạch sprint, phụ thuộc nếu có). Không gọi mạng.
Item sống = mọi issue trừ bản thay thế (đóng + nhãn thay thế); luật so khoá, tổng cha, cây chỉ nhìn item sống, trừ khi
ghi khác (A3 soi bản thay thế, D3/E3 đếm mọi con như GitHub)."""
from pathlib import Path

from audit_lib import LoiBoSinh, doc_json, doc_yaml, khoa_tu_title, la_ban_thua, tracker_tu_title


class NguCanh:
    def __init__(self, anh: dict, cfg: dict, tieu_chi: dict, seed=None, plan=None, pt=None, ngay_xet=None):
        self.anh, self.cfg, self.tc = anh, cfg, tieu_chi
        self.seed, self.plan, self.pt = seed, plan, pt
        self.ngay_xet = ngay_xet or cfg.get("ngay_xet") or str(anh.get("chup_luc") or "")[:10]
        self.items = [i for i in anh.get("items") or [] if i.get("loai", "ISSUE") == "ISSUE"]
        self.theo_so = {i["so"]: i for i in self.items}
        self.thay = [i for i in self.items if la_ban_thua(i, cfg)]
        self.song = [i for i in self.items if not la_ban_thua(i, cfg)]
        self.con, self.con_tat_ca = {}, {}
        for i in self.items:
            if i.get("cha") is not None:
                self.con_tat_ca.setdefault(i["cha"], []).append(i)
                if not la_ban_thua(i, cfg):
                    self.con.setdefault(i["cha"], []).append(i)

    @classmethod
    def tao(cls, anh, cfg_path, tc_path, seed_dir=None, sprint_plan=None, phu_thuoc=None, ngay_xet=None):
        anh = anh if isinstance(anh, dict) else doc_json(anh)
        return cls(anh, doc_yaml(cfg_path), doc_yaml(tc_path), doc_seed(seed_dir) if seed_dir else None,
                   doc_plan(sprint_plan) if sprint_plan else None, doc_yaml(phu_thuoc) if phu_thuoc else None, ngay_xet)

    def f(self, item: dict, ten: str):
        return (item.get("field") or {}).get(self.cfg["field_map"][ten])

    def khoa(self, item: dict) -> str | None:
        return khoa_tu_title(item.get("title"), self.cfg)

    def tracker(self, item: dict) -> str | None:
        return tracker_tu_title(item.get("title"), self.cfg)

    def con_song(self, item: dict) -> list[dict]:
        return self.con.get(item["so"], [])

    def epic_cua(self, item: dict) -> str | None:
        """Khoá epic theo chuỗi cha (epic thì chính nó); đứt chuỗi hoặc vòng → None."""
        da, x = set(), item
        while x is not None and x["so"] not in da:
            if self.tracker(x) == "epic":
                return self.khoa(x)
            da.add(x["so"])
            x = self.theo_so.get(x.get("cha"))
        return None

    def tran(self, owner: str | None) -> float | None:
        """Trần giờ một sprint của vị trí Owner = tran × giờ × số người (BrSE dùng brse_inv)."""
        nl = self.cfg["nang_luc_sprint"]
        if owner is None:
            return None
        gio = nl["brse_inv"] if owner == "BrSE" else nl["gio"]
        return nl["tran"] * gio * (nl.get("so_nguoi") or {}).get(owner, 1)


def doc_seed(thu_muc) -> dict[str, str]:
    """{khoá: khoá epic} từ thư mục seed (mỗi tệp `<EPIC>.yaml` có `epic` và `items`)."""
    thu_muc = Path(thu_muc)
    if not thu_muc.is_dir():
        raise LoiBoSinh(f"thiếu thư mục seed: {thu_muc}")
    ra = {}
    for p in sorted(thu_muc.glob("*.yaml")):
        d = doc_yaml(p)
        ep = (d.get("epic") or {}).get("key")
        for it in [d.get("epic") or {}] + list(d.get("items") or []):
            if it.get("key"):
                ra[it["key"]] = ep
    if not ra:
        raise LoiBoSinh(f"{thu_muc}: không có tệp <EPIC>.yaml nào có khối `epic` — --seed-dir phải trỏ đúng thư mục chứa tệp epic")
    return ra


def doc_plan(p) -> dict:
    d = doc_json(p)
    return {"sprint": d["sprint"], "muc": {m["key"]: m for m in d.get("muc") or []}}

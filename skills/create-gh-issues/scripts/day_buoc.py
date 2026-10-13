"""Máy trạng thái đẩy MỘT khoá seed lên GitHub: tao (REST tạo issue) → them (addProjectV2ItemById) → field
(updateProjectV2ItemFieldValue, gộp các field trong một lệnh bằng bí danh) → cha (REST sub_issues). Ghi map sau MỖI bước.

Chạy lại bắt đầu từ bước chưa xong (`buoc`). Lệnh tạo không rõ kết quả (KHONG_RO) → chờ, hoà map bằng danh sách issue rồi mới
tạo lại, tối đa 3 lần. Nối cha trả 422 → hỏi GraphQL `issue{parent{number}}`: đúng cha của seed thì `cha_ok`, khác thì dừng
(không dùng `replace_parent`). Khoá đã có: so `bam` (title, thân, nhãn); khác thì PATCH khi bật `cap_nhat`, không thì đếm lệch.
"""
from dataclasses import dataclass, field

from gh_api import KHONG_RO, LoiGh
from lib import LoiBoSinh
from ban_do import bam, bam_than, da_xong, hoa_map, liet_ke_issue

Q_THEM = "mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}"
Q_CHA = "query($o:String!,$n:String!,$k:Int!){repository(owner:$o,name:$n){issue(number:$k){parent{number}}}}"
LAN_TAO = 3


def q_field(n: int) -> str:
    """Một mutation, n bí danh f0…f(n-1): mỗi bí danh đặt một field single-select của cùng item."""
    bien = "".join(f",$f{i}:ID!,$o{i}:String!" for i in range(n))
    than = " ".join(f"f{i}:updateProjectV2ItemFieldValue(input:{{projectId:$p,itemId:$i,fieldId:$f{i},"
                    f"value:{{singleSelectOptionId:$o{i}}}}}){{projectV2Item{{id}}}}" for i in range(n))
    return f"mutation($p:ID!,$i:ID!{bien}){{{than}}}"


@dataclass
class Viec:
    """Một khoá cần đẩy: bản ghi seed, title, thân, nhãn, [(id field, id lựa chọn)]."""
    key: str
    cha: str | None
    title: str
    body: str
    labels: list
    field: list


@dataclass
class Dem:
    tao_moi: int = 0
    nhan_lai: int = 0
    loi: int = 0
    cap_nhat: int = 0
    lech: int = 0
    loi_ghi: list = field(default_factory=list)


class Day:
    def __init__(self, client, repo: str, project_id: str, assignee: str, m: dict, luu, seed_cha: dict, cap_nhat=False):
        self.c, self.repo, self.pid, self.assignee = client, repo, project_id, assignee
        self.m, self.luu, self.seed_cha, self.cap_nhat = m, luu, seed_cha, cap_nhat
        self.dem = Dem()

    def day(self, v: Viec) -> None:
        e = self.m.get(v.key)
        if e is None:
            e = self._tao(v)
        else:
            self.dem.nhan_lai += 1
        if not da_xong(e["buoc"], "them"):
            self._them(v.key, e)
        if not da_xong(e["buoc"], "field"):
            self._field(v, e)
        if v.cha is None:
            e["cha_ok"] = True
        elif not (da_xong(e["buoc"], "cha") and e.get("cha_ok")):
            self._cha(v, e)
        self._doi_chieu(v, e)

    def chi_field(self, v: Viec) -> None:
        e = self.m.get(v.key)
        if e is None or not e.get("item_id"):
            raise LoiBoSinh(f"{v.key}: chưa có item trên Project — đẩy thường trước rồi mới --chi-field")
        self._field(v, e)

    # ---------- bước ----------
    def _tao(self, v: Viec) -> dict:
        than = {"title": v.title, "body": v.body, "labels": v.labels, "assignees": [self.assignee]}
        for _ in range(LAN_TAO):
            r = self.c.rest("POST", f"repos/{self.repo}/issues", than, tao=True, op="tao-issue")
            if r is KHONG_RO:
                self.c.sleep(10)
                hoa_map(self.m, liet_ke_issue(self.c, self.repo), self.seed_cha)  # hoà trước, không tạo mù
                if v.key not in self.m:
                    continue
                e = self.m[v.key]
            else:
                j = r.json
                e = {"so": j["number"], "url": j.get("html_url"), "id": j["id"], "node_id": j["node_id"], "item_id": None,
                     "buoc": "tao", "cha": v.cha, "cha_ok": v.cha is None}
                self.m[v.key] = e
            e.update(bam=bam(v.title, v.body, v.labels), bam_than=bam_than(v.body))
            self.dem.tao_moi += 1
            self.luu()
            return e
        raise LoiBoSinh(f"{v.key}: lệnh tạo không rõ kết quả {LAN_TAO} lần, hoà map vẫn không thấy — dừng, xem <log-dir>")

    def _them(self, key: str, e: dict) -> None:
        d = self.c.graphql(Q_THEM, {"p": self.pid, "c": e["node_id"]}, op="addProjectV2ItemById", ghi=True)
        e["item_id"] = d["addProjectV2ItemById"]["item"]["id"]
        e["buoc"] = "them"
        self.luu()

    def _field(self, v: Viec, e: dict) -> None:
        bien = {"p": self.pid, "i": e["item_id"]}
        for i, (fid, oid) in enumerate(v.field):
            bien.update({f"f{i}": fid, f"o{i}": oid})
        if v.field:
            self.c.graphql(q_field(len(v.field)), bien, op="updateProjectV2ItemFieldValue", ghi=True)
        if not da_xong(e["buoc"], "field"):
            e["buoc"] = "field"
        self.luu()

    def _cha(self, v: Viec, e: dict) -> None:
        goc = self.m.get(v.cha)
        if not goc or not goc.get("so"):
            raise LoiBoSinh(f"{v.key}: cha {v.cha} chưa có trên GitHub — đẩy cha trước (cha trước con)")
        try:
            self.c.rest("POST", f"repos/{self.repo}/issues/{goc['so']}/sub_issues", {"sub_issue_id": e["id"]}, op="sub_issues")
        except LoiGh as x:
            if x.status != 422:
                raise
            co = self._cha_that(e["so"])
            if co != goc["so"]:
                raise LoiBoSinh(f"{v.key}: nối cha #{goc['so']} bị 422 «{x.thong_diep}», cha hiện tại "
                                f"{'#' + str(co) if co else 'không có'} — không dùng replace_parent, dừng và báo") from x
        e.update(buoc="cha", cha=v.cha, cha_ok=True)
        self.luu()

    def _cha_that(self, so: int) -> int | None:
        chu, ten = self.repo.split("/")
        d = self.c.graphql(Q_CHA, {"o": chu, "n": ten, "k": so}, op="issue.parent")
        return (((d.get("repository") or {}).get("issue") or {}).get("parent") or {}).get("number")

    def _doi_chieu(self, v: Viec, e: dict) -> None:
        moi = bam(v.title, v.body, v.labels)
        if e.get("bam") == moi:
            return
        if not self.cap_nhat:
            self.dem.lech += 1
            return
        self.c.rest("PATCH", f"repos/{self.repo}/issues/{e['so']}", {"title": v.title, "body": v.body, "labels": v.labels},
                    op="sua-issue")
        e.update(bam=moi, bam_than=bam_than(v.body))
        self.dem.cap_nhat += 1
        self.luu()


def xong(e: dict | None) -> bool:
    """Khoá đã đủ bước: epic tới `field`, còn lại tới `cha` và `cha_ok`."""
    if not e:
        return False
    return da_xong(e.get("buoc"), "field") if e.get("cha") is None else (e.get("buoc") == "cha" and bool(e.get("cha_ok")))

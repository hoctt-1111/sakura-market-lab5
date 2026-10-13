"""Cấu hình của skill: gộp file `--config` (YAML) với tham số dòng lệnh (dòng lệnh thắng), dựng đường dẫn trong thư mục seed
và thư mục bằng chứng, đọc id Project / field / lựa chọn qua GraphQL (chỉ đọc) rồi đệm vào `<evidence-dir>/field-list.json`.

Đường dẫn tương đối trong file cấu hình tính từ thư mục chứa file đó; trên dòng lệnh tính từ thư mục đang đứng.
Lệnh đẩy chỉ đặt 3 field single-select: Status (`team.yaml › status_dau`), Owner (`owner` của bản ghi), Priority
(`team.yaml › priority_map[priority]`); tên field thật trên Project lấy qua `team.yaml › field_map`.
"""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from lib import LoiBoSinh, doc_json, doc_yaml, ghi_json_nguyen_tu

FIELD_DAT = ("Status", "Owner", "Priority")  # khoá logic trong team.yaml › field_map
DUONG = ("seed_dir", "evidence_dir", "khuon", "spec_registry", "than_dir", "log_dir")
KHOA = ("repo", "project_owner", "project_number", "nhip_phut", "nhip_gio") + DUONG
Q_PROJECT = ("query($o:String!,$n:Int!){repositoryOwner(login:$o){__typename ... on User{projectV2(number:$n){...P}}"
             " ... on Organization{projectV2(number:$n){...P}}}} fragment P on ProjectV2{id number title url public"
             " fields(first:100){nodes{__typename ... on ProjectV2FieldCommon{id name dataType}"
             " ... on ProjectV2SingleSelectField{options{id name}}}}}")


@dataclass
class CauHinh:
    repo: str | None = None
    project_owner: str | None = None
    project_number: int | None = None
    seed_dir: Path | None = None
    evidence_dir: Path | None = None
    khuon: Path | None = None
    spec_registry: Path | None = None
    than_dir: Path | None = None
    log_dir: Path | None = None
    co_chan: list = field(default_factory=list)
    nhip_phut: int = 40
    nhip_gio: int = 450
    than: dict = field(default_factory=dict)  # tuỳ chọn dựng thân (docs/seed-schema.md, mục Cấu hình)
    spec: dict = field(default_factory=dict)  # bảng diễn giải giá trị registry spec
    van: dict = field(default_factory=dict)   # luật độ dài của check --van

    def can(self, *ten) -> None:
        if thieu := [t for t in ten if getattr(self, t) in (None, "")]:
            raise LoiBoSinh("thiếu " + ", ".join(f"--{t.replace('_', '-')}" for t in thieu) + " (hoặc khoá cùng tên trong --config)")

    backlog = property(lambda s: s.seed_dir / "backlog")
    team = property(lambda s: s.seed_dir / "team.yaml")
    labels = property(lambda s: s.seed_dir / "labels.yaml")
    map_file = property(lambda s: s.evidence_dir / "board-map.json")
    snap_file = property(lambda s: s.evidence_dir / "board-snapshot.json")
    field_list_file = property(lambda s: s.evidence_dir / "field-list.json")
    co_push = property(lambda s: s.evidence_dir / "PUSH_RUNNING")


def tu_args(a) -> CauHinh:
    """CauHinh từ argparse.Namespace: khoá trong `--config` trước, tham số dòng lệnh đè lên."""
    gt: dict = {}
    if getattr(a, "config", None):
        goc = Path(a.config).resolve().parent
        d = doc_yaml(a.config) or {}
        if la := sorted(set(d) - set(KHOA) - {"co_chan", "than", "spec", "van"}):
            raise LoiBoSinh(f"{a.config}: khoá lạ {la}")
        gt = {k: (goc / v if k in DUONG and v else v) for k, v in d.items()}
        gt["co_chan"] = [goc / x for x in d.get("co_chan") or []]
    for k in KHOA:
        if (v := getattr(a, k, None)) not in (None, ""):
            gt[k] = Path(v) if k in DUONG else v
    gt["co_chan"] = list(gt.get("co_chan") or []) + [Path(x) for x in getattr(a, "co_chan", None) or []]
    c = CauHinh(**gt)
    if c.project_number is not None:
        c.project_number = int(c.project_number)
    if c.evidence_dir is not None:
        c.than_dir = c.than_dir or c.evidence_dir / "bodies"
        c.log_dir = c.log_dir or c.evidence_dir / "log"
        c.co_chan = c.co_chan or [c.evidence_dir / "BREAK_RUNNING"]
    return c


def doc_field_list(cfg: CauHinh, client, lam_moi=False) -> dict:
    """Danh sách field của Project: đọc đệm nếu đúng owner + số Project, không thì hỏi GraphQL (chỉ đọc) rồi ghi đệm."""
    cfg.can("evidence_dir", "project_owner", "project_number")
    p = cfg.field_list_file
    if p.is_file() and not lam_moi:
        fl = doc_json(p)
        pr = fl.get("project") or {}
        if pr.get("owner") == cfg.project_owner and pr.get("number") == cfg.project_number:
            return fl
    d = client.graphql(Q_PROJECT, {"o": cfg.project_owner, "n": cfg.project_number}, op="doc-field-list")
    chu = d.get("repositoryOwner") or {}
    pv = chu.get("projectV2")
    if not pv:
        raise LoiBoSinh(f"không thấy Project số {cfg.project_number} của {cfg.project_owner} (gh cần scope project)")
    fl = {"doc_luc": datetime.now().isoformat(timespec="seconds"),
          "project": {"id": pv["id"], "number": pv["number"], "title": pv.get("title"), "url": pv.get("url"),
                      "public": pv.get("public"), "owner": cfg.project_owner, "loai_chu": chu.get("__typename")},
          "fields": [{k: n[k] for k in ("id", "name", "dataType", "options") if k in n}
                     for n in (pv.get("fields") or {}).get("nodes") or [] if n.get("name")]}
    ghi_json_nguyen_tu(p, fl)
    return fl


def project_id(fl: dict) -> str:
    return fl["project"]["id"]


def field_ids(fl: dict) -> dict[str, tuple[str, dict[str, str]]]:
    """{tên field: (id field, {tên lựa chọn: id lựa chọn})} cho field single-select của Project."""
    return {n["name"]: (n["id"], {o["name"]: o["id"] for o in n["options"]}) for n in fl.get("fields") or [] if "options" in n}


def gia_tri_field(it: dict, team: dict, chon=FIELD_DAT) -> dict[str, str]:
    """{tên field trên Project: tên lựa chọn} của một bản ghi seed theo luật team.yaml."""
    logic = {"Status": team["status_dau"], "Owner": it["owner"], "Priority": team["priority_map"][it["priority"]]}
    if la := [k for k in chon if k not in logic]:
        raise LoiBoSinh(f"--field {la}: skill chỉ đặt {list(logic)} (field khác đặt tay hoặc bằng công cụ riêng)")
    return {team["field_map"][k]: logic[k] for k in chon}


def lenh_field(it: dict, team: dict, ids: dict, chon=FIELD_DAT) -> list[tuple[str, str]]:
    """[(id field, id lựa chọn)] — thiếu field hay lựa chọn trên Project thì dừng trước mọi lệnh mạng."""
    ra = []
    for ten, chon_ten in gia_tri_field(it, team, chon).items():
        if ten not in ids or chon_ten not in ids[ten][1]:
            raise LoiBoSinh(f"{it['key']}: field `{ten}` không có lựa chọn `{chon_ten}` trên Project (field-list.json)")
        ra.append((ids[ten][0], ids[ten][1][chon_ten]))
    return ra


def ten_file_than(key: str) -> str:
    """Tên file thân issue đã ghi để quét: `SC-031/BE` → `SC-031-BE.md`."""
    return key.replace("/", "-") + ".md"

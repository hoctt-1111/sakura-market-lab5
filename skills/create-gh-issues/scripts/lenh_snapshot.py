"""Lệnh `snapshot`: chụp GitHub Project (chỉ đọc) → <evidence-dir>/board-snapshot.json cho `check --snapshot`.

Đọc: mọi item của Project (GraphQL, trang 100) với số, title, nhãn, người phụ trách, trạng thái, cha, tổng sub-issue và giá
trị các field trong `team.yaml › field_map`; Project `public`, tên mọi field; nhãn của repo (REST). Thứ tự cố định để so
được hai lần chụp. `--body`: thêm `bam_than` (sha256 thân issue, như ban_do.bam_than) — không lưu thân.
"""
import re
from datetime import datetime
from pathlib import Path

import cau_hinh as ch
from ban_do import bam_than
from gh_api import GhClient
from lib import LoiBoSinh, chan_khi_co, doc_yaml, ghi_json_nguyen_tu

Q_ITEM = """query($id:ID!,$after:String){node(id:$id){... on ProjectV2{title number url public
 fields(first:50){nodes{... on ProjectV2FieldCommon{name}}}
 items(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{id type
  content{__typename ... on Issue{number title state BODY labels(first:30){nodes{name}} assignees(first:10){nodes{login}}
   parent{number} subIssuesSummary{total completed}} ... on PullRequest{number title state} ... on DraftIssue{title}}
  fieldValues(first:30){nodes{__typename
   ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldNumberValue{number field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldIterationValue{title field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}}}}}}}}"""
GIA_TRI = ("name", "number", "title", "date", "text")


def gia_tri_o(nodes: list, ten_can: list[str]) -> dict:
    ra = {t: None for t in ten_can}
    for n in nodes or []:
        ten = ((n or {}).get("field") or {}).get("name")
        if ten in ra:
            ra[ten] = next((n[k] for k in GIA_TRI if k in n), None)
    return ra


def item(n: dict, ten_can: list[str], co_than: bool) -> dict:
    c = n.get("content") or {}
    ra = {"item_id": n["id"], "loai": n.get("type"), "so": c.get("number"), "title": c.get("title"), "state": c.get("state"),
          "labels": sorted(x["name"] for x in (c.get("labels") or {}).get("nodes") or []),
          "assignees": sorted(x["login"] for x in (c.get("assignees") or {}).get("nodes") or []),
          "cha": (c.get("parent") or {}).get("number"), "con": c.get("subIssuesSummary"),
          "field": gia_tri_o((n.get("fieldValues") or {}).get("nodes"), ten_can)}
    if co_than and c.get("__typename") == "Issue":
        ra["bam_than"] = bam_than(c.get("body") or "")
    return ra


def chup(client, project_id: str, repo: str, ten_can: list[str], co_than=False) -> dict:
    q = Q_ITEM.replace("BODY", "body" if co_than else "")
    ds, sau, p = [], None, {}
    while True:
        p = client.graphql(q, {"id": project_id, "after": sau}, op="snap-items").get("node") or {}
        if not p:
            raise LoiBoSinh(f"không đọc được Project {project_id}")
        trang = p["items"]
        ds += [item(n, ten_can, co_than) for n in trang["nodes"]]
        if not trang["pageInfo"]["hasNextPage"]:
            break
        sau = trang["pageInfo"]["endCursor"]
    nhan, path = [], f"repos/{repo}/labels?per_page=100"
    while path:
        r = client.rest("GET", path, op="snap-labels")
        nhan += [x["name"] for x in r.json or []]
        m = re.search(r'<https://api\.github\.com/([^>]+)>;\s*rel="next"', r.headers.get("link", ""))
        path = m.group(1) if m else None
    ds.sort(key=lambda x: (x["loai"] != "ISSUE", x["so"] or 0, x["title"] or ""))
    return {"chup_luc": datetime.now().isoformat(timespec="seconds"), "co_bam_than": co_than,
            "project": {"id": project_id, "number": p.get("number"), "title": p.get("title"), "url": p.get("url"),
                        "public": p.get("public"), "fields": sorted(f["name"] for f in p["fields"]["nodes"] if f.get("name"))},
            "repo": {"ten": repo, "labels": sorted(nhan)}, "items": ds}


def main(a, cfg, client=None) -> int:
    cfg.can("repo", "seed_dir", "evidence_dir", "project_owner", "project_number")
    chan_khi_co(cfg.co_chan)
    team = doc_yaml(cfg.team)
    client = client or GhClient(log_path=cfg.log_dir / "snapshot.jsonl", kiem_diem_moi=0)
    fl = ch.doc_field_list(cfg, client, getattr(a, "doc_lai_field", False))
    anh = chup(client, ch.project_id(fl), cfg.repo, list(team["field_map"].values()), a.body)
    out = Path(a.out) if a.out else cfg.snap_file
    ghi_json_nguyen_tu(out, anh)
    loai = {}
    for x in anh["items"]:
        loai[x["loai"]] = loai.get(x["loai"], 0) + 1
    print(f"ảnh chụp: {len(anh['items'])} item ({', '.join(f'{k} {v}' for k, v in sorted(loai.items())) or 'trống'}) · "
          f"public {anh['project']['public']} · {len(anh['project']['fields'])} field · {len(anh['repo']['labels'])} nhãn repo"
          f"{' · có băm thân' if a.body else ''} → {out}")
    return 0

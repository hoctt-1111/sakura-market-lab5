"""Lệnh snapshot: chụp GitHub Project v2 (chỉ đọc) qua `gh api graphql` → dict cùng khuôn ảnh chụp mà lệnh audit đọc.
Đọc mọi item (trang 100): số, tiêu đề, trạng thái issue, nhãn, người phụ trách, cha, tổng sub-issue, giá trị field trong
`field_map`; Project public và tên mọi field. Không đọc thân issue, không in token (gh tự giữ)."""
import json
import subprocess
from datetime import datetime

from audit_lib import LoiBoSinh

Q_ID = """query($o:String!,$n:Int!){user(login:$o){projectV2(number:$n){id}} organization(login:$o){projectV2(number:$n){id}}}"""
Q_ITEM = """query($id:ID!,$after:String){node(id:$id){... on ProjectV2{title number url public
 fields(first:50){nodes{... on ProjectV2FieldCommon{name}}}
 items(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{id type
  content{__typename ... on Issue{number title state labels(first:30){nodes{name}} assignees(first:10){nodes{login}}
   parent{number} subIssuesSummary{total completed}}}
  fieldValues(first:30){nodes{__typename
   ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldNumberValue{number field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldIterationValue{title field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}}
   ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}}}}}}}}"""
GIA_TRI = ("name", "number", "title", "date", "text")


def _gh(query: str, **bien) -> dict:
    lenh = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in bien.items():
        if v is not None:
            lenh += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    try:
        r = subprocess.run(lenh, capture_output=True, text=True, timeout=120)
        d = json.loads(r.stdout) if r.stdout.strip().startswith("{") else {}
    except (OSError, subprocess.TimeoutExpired) as e:
        raise LoiBoSinh(f"không chạy được gh (đã cài và `gh auth login` chưa?): {e}") from e
    except json.JSONDecodeError as e:
        raise LoiBoSinh(f"gh trả về không phải JSON: {r.stdout[:200]}") from e
    if r.returncode != 0 and not d.get("data"):
        raise LoiBoSinh(f"gh api graphql lỗi: {(r.stderr or r.stdout).strip()[:300]}")
    return d.get("data") or {}


def _field(nodes, ten: list[str]) -> dict:
    ra = dict.fromkeys(ten)
    for n in nodes or []:
        t = ((n or {}).get("field") or {}).get("name")
        if t in ra:
            ra[t] = next((n[k] for k in GIA_TRI if k in n), None)
    return ra


def chup(cfg: dict) -> dict:
    d = _gh(Q_ID, o=cfg["project_owner"], n=int(cfg["project_number"]))
    pid = ((d.get("user") or {}).get("projectV2") or (d.get("organization") or {}).get("projectV2") or {}).get("id")
    if not pid:
        raise LoiBoSinh(f"không tìm thấy Project {cfg['project_owner']} #{cfg['project_number']}")
    ten, items, sau, pj = list(cfg["field_map"].values()), [], None, {}
    while True:
        n = _gh(Q_ITEM, id=pid, after=sau).get("node")
        if not n:
            raise LoiBoSinh(f"gh không trả node Project {pid} (thiếu quyền `project`?)")
        pj = {"id": pid, "number": n["number"], "title": n["title"], "url": n["url"], "public": n["public"],
              "fields": sorted(x["name"] for x in n["fields"]["nodes"] if x)}
        for x in n["items"]["nodes"]:
            c = x.get("content") or {}
            if c.get("__typename") != "Issue":
                continue
            items.append({"item_id": x["id"], "loai": "ISSUE", "so": c["number"], "title": c["title"], "state": c["state"],
                          "labels": sorted(l["name"] for l in c["labels"]["nodes"]),
                          "assignees": sorted(a["login"] for a in c["assignees"]["nodes"]),
                          "cha": (c.get("parent") or {}).get("number"), "con": c.get("subIssuesSummary") or {"total": 0, "completed": 0},
                          "field": _field(x["fieldValues"]["nodes"], ten)})
        if not n["items"]["pageInfo"]["hasNextPage"]:
            break
        sau = n["items"]["pageInfo"]["endCursor"]
    return {"chup_luc": datetime.now().isoformat(timespec="seconds"), "co_bam_than": False, "project": pj,
            "repo": cfg.get("repo"), "items": sorted(items, key=lambda i: i["so"])}


def json_dep(anh: dict) -> str:
    return json.dumps(anh, ensure_ascii=False, indent=1) + "\n"

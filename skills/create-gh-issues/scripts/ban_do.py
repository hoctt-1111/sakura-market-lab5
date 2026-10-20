"""Map khoá seed ↔ issue GitHub (`<evidence-dir>/board-map.json`): đọc, ghi nguyên tử, băm, hoà với danh sách issue thật.

Bản ghi: {so, url, id, node_id, item_id, buoc: tao|them|field|cha, cha, cha_ok, bam, bam_than}. `bam_than` = sha256 thân đã
đăng (check --snapshot so với thân dựng lại từ seed); `bam` = sha256 của (title, bam_than, nhãn đã sắp) — `--cap-nhat` so
để PATCH. Bản thừa đã xử lý = issue ĐÃ ĐÓNG mang nhãn thừa `NHAN_THUA` nằm cạnh một issue khác cùng key; issue mang nhãn
thừa duy nhất của một key (kể cả đã đóng) vẫn là issue của key đó. Nhãn thừa tách khỏi `spec-gap` (= chỗ hở của spec).
"""
import hashlib
import json
import re
from pathlib import Path

from lib import LoiBoSinh, doc_json, ghi_json_nguyen_tu
from seed_doc import khoa_tu_title  # noqa: F401 (tái xuất)

BUOC = ("tao", "them", "field", "cha")
NHAN_THUA = "da-thay-the"


def da_xong(buoc: str | None, moc: str) -> bool:
    return buoc in BUOC and BUOC.index(buoc) >= BUOC.index(moc)


def bam_than(body: str) -> str:
    return hashlib.sha256(body.replace("\r\n", "\n").strip().encode("utf-8")).hexdigest()


def bam(title: str, body: str, labels) -> str:
    return hashlib.sha256(json.dumps([title, bam_than(body), sorted(labels)], ensure_ascii=False).encode("utf-8")).hexdigest()


def doc_map(p: Path) -> dict:
    return doc_json(p, {}) if Path(p).is_file() else {}


def ghi_map(p: Path, m: dict) -> None:
    ghi_json_nguyen_tu(p, m)


def la_ban_thua(issue: dict) -> bool:
    return str(issue.get("state")).lower() == "closed" and any(
        (l.get("name") if isinstance(l, dict) else l) == NHAN_THUA for l in issue.get("labels") or [])


def chon_ban_chinh(ds: list[dict]) -> tuple[dict | None, list[dict]]:
    """(issue chính, bản thừa đã xử lý) của một key. Không chọn được đúng một issue chính → (None, [])."""
    if len(ds) == 1:
        return ds[0], []
    song = [i for i in ds if not la_ban_thua(i)]
    return (song[0], [i for i in ds if la_ban_thua(i)]) if len(song) == 1 else (None, [])


def liet_ke_issue(client, repo: str) -> list[dict]:
    """Mọi issue (mở và đóng, bỏ pull request) của repo, đi theo header Link rel=next."""
    ra, path = [], f"repos/{repo}/issues?state=all&per_page=100"
    while path:
        r = client.rest("GET", path, op="liet-ke-issue")
        ra += [i for i in (r.json or []) if "pull_request" not in i]
        m = re.search(r'<https://api\.github\.com/([^>]+)>;\s*rel="next"', r.headers.get("link", ""))
        path = m.group(1) if m else None
    return ra


def hoa_map(m: dict, issues: list[dict] | None, seed_cha: dict) -> int:
    """Điền vào map các khoá seed đã có issue trên GitHub mà map chưa ghi; trả số khoá vừa nhận. Trùng key, map lệch
    số, map trỏ issue không còn → LoiBoSinh (dừng, không đoán). `issues=None` (dry-run) → chỉ dùng map."""
    if issues is None:
        return 0
    theo_key: dict[str, list[dict]] = {}
    for i in issues:
        if k := khoa_tu_title(i.get("title", "")):
            theo_key.setdefault(k, []).append(i)
    chinh = {}
    for k, ds in sorted(theo_key.items()):
        chinh[k], _ = chon_ban_chinh(ds)
        if chinh[k] is None:
            raise LoiBoSinh(f"{k}: {len(ds)} issue trùng key trên GitHub ({', '.join('#' + str(i['number']) for i in ds)})"
                            f" — đóng bản thừa với nhãn {NHAN_THUA} rồi chạy lại")
    so_github = {i["number"] for i in chinh.values()}
    for k, e in m.items():
        if e.get("so") not in so_github and k in seed_cha:
            raise LoiBoSinh(f"{k}: map ghi #{e.get('so')} nhưng GitHub không có issue nào khớp key — kiểm tay trước khi đẩy")
    moi = 0
    for k, i in chinh.items():
        if k in m:
            if m[k].get("so") != i["number"]:
                raise LoiBoSinh(f"{k}: map ghi #{m[k].get('so')} nhưng GitHub có #{i['number']}")
            continue
        if k not in seed_cha:
            continue  # item lạ: check --snapshot báo, push không nhận
        m[k] = {"so": i["number"], "url": i.get("html_url"), "id": i["id"], "node_id": i["node_id"], "item_id": None,
                "buoc": "tao", "cha": seed_cha[k], "cha_ok": seed_cha[k] is None}
        moi += 1
    return moi

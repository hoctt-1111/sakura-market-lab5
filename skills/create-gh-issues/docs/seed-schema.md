# Schema đầu vào của create-gh-issues

Mọi lệnh đọc một thư mục seed (`--seed-dir`) và ghi vào một thư mục bằng chứng (`--evidence-dir`). Seed là nguồn duy nhất: sửa seed rồi đẩy lại, không sửa tay issue trên web.

## 1. Cây thư mục seed

```
<seed-dir>/
  backlog/<EPIC>.yaml   một file một epic, tên file = key epic (bắt buộc)
  team.yaml             luật Owner, Priority, Status, người phụ trách, mẫu định nghĩa xong (bắt buộc)
  labels.yaml           nhãn của repo (bắt buộc)
  premise.yaml          giả định P-xx, hiện ở mục «Tiền đề» và issue điều tra (tuỳ chọn)
  gaps.yaml, gaps/*.yaml  chỗ hở G-xx, hiện ở mục «Chỗ hở» (tuỳ chọn; trùng mã thì file đọc trước thắng)
```

File khác trong thư mục (vd. dữ liệu riêng của bộ sinh seed) không được đọc.

## 2. Key và title

- Bốn tầng: `epic` → `story` hoặc `investigation` → leaf `devtask` / `testdesign`. Story và điều tra là con trực tiếp của epic; leaf là con của story cùng file.
- Key duy nhất toàn backlog, không đổi sau lần đẩy đầu. Epic và story: chữ hoa, số, gạch nối (`FG-04`, `SC-031`, `INV-Q-SD4`). Leaf: `<story>/<FE|BE|DB|TEST|INFRA>`; `TEST` là `testdesign`, còn lại là `devtask`.
- Title dựng từ seed: `[EPIC] <key> <title_vi>`, `[STORY] …`, `[INVESTIGATION] …`, `[DEV TASK] …`, `[TEST DESIGN] …`. Key là từ thứ hai, khớp `^\[[A-Z ]+\] (\S+) `. Mọi lệnh tìm issue theo key này, nên đừng sửa title trên web.
- Mỗi cha tối đa 100 con (trần sub-issue của GitHub); story phải có ít nhất một leaf.

## 3. `backlog/<EPIC>.yaml`

```yaml
epic: {key: E1, tracker: epic, title_vi: "Nền tảng", feature: "tuỳ chọn", spec_refs: {...}, labels: [type:epic],
       owner: PM, priority: 3, premise_refs: [], gap_refs: [], mo_ta: "…", pham_vi: "", luong_chinh: [],
       tieu_chi_nghiem_thu: ["…"], dinh_nghia_xong: []}
items:
  - key: S-1
    cha: E1                      # bắt buộc trừ epic
    tracker: story               # story | investigation | devtask | testdesign
    title_vi: "Khung repo"       # một dòng, không rỗng
    spec_refs: {sc: [], api: [API-201], tech: [], bang: [orders], fr: [], adr: [], nfr: []}
    labels: [type:story]         # phải có type:<tracker>; mọi nhãn phải có trong labels.yaml
    owner: PM                    # một giá trị của team.yaml › owner_theo_tracker / owner_theo_leaf
    priority: 3                  # khoá của team.yaml › priority_map
    premise_refs: [P-01]         # mã trong premise.yaml
    gap_refs: [G-02]             # mã trong gaps
    mo_ta: "2–4 câu"             # 5 trường văn do người (hoặc agent) viết
    pham_vi: "…"
    luong_chinh: ["Ai làm gì", "…"]
    tieu_chi_nghiem_thu: ["Khi … thì …"]
    dinh_nghia_xong: []          # chỉ phần thêm ngoài mẫu trong team.yaml
    nguoi_tra_loi: "Khách"       # chỉ issue điều tra
    han: "2026-10-31"            # chỉ issue điều tra
```

- `spec_refs` luôn có 7 khoá `sc, api, tech, bang, fr, adr, nfr` (danh sách, có thể rỗng); thêm tuỳ chọn `khuon, ac, sd, hoi`. Leaf DB ghi bảng nó tạo ở `bang` — bảng đó được ghi «chủ migration» ở các leaf khác.
- Trong một trường văn, dòng bắt đầu `Ràng buộc đặc thù:` được tách ra thành mục «Ràng buộc đặc thù» của thân.
- Nhãn bắt đầu `constraint:` là nhãn ràng buộc đặc thù: thân issue in câu giải thích lấy từ `team.yaml › rang_buoc`.

## 4. `team.yaml`

```yaml
assignee: <login GitHub>          # gán cho mọi issue
status_dau: New                   # lựa chọn Status lúc tạo
priority_map: {1: Urgent, 2: High, 3: Normal}   # priority trong seed → lựa chọn của field Priority
owner_theo_tracker: {epic: PM, story: PM, investigation: {khach: BrSE, tech_lead: BE-1}}
owner_theo_leaf: {FE: FE-1, BE: {le: BE-1, chan: BE-2, xuyen_suot: BE-1}, DB: BE-1, TEST: QA, INFRA: Infra}
field_map: {Status: Status, Priority: Priority, Owner: Owner}   # khoá logic → tên field đúng như trên Project
dinh_nghia_xong_mau: {epic: ["…"], story: ["…"], investigation: ["…"], FE: ["…"], BE: ["…"], DB: ["…"], TEST: ["…"], INFRA: ["…"]}
rang_buoc: [{nhan: "constraint:hitl", ten: "Người quyết, máy ghi nhận", vi_sao: "…"}]
```

Mọi giá trị Owner (kể cả lồng trong dict) phải là lựa chọn của field Owner; `check --seed` so với `field-list.json` khi đã có.

## 5. `labels.yaml`, `premise.yaml`, `gaps.yaml`

```yaml
nhan: [{ten: "type:epic", mau: "5319e7", mo_ta: "Epic"}]          # labels.yaml — lệnh labels tạo đúng danh sách này
p: [{ma: P-01, spec: "tên ngắn", sau: "giả định đang dùng", chot: "…", cho_de_ngo: "…", inv: INV-1, anh_huong: [S-1, S-1/BE]}]
g: [{ma: G-01, mo_ta: "chỗ hở", xu_ly: "premise:P-01"}]           # gaps.yaml và gaps/*.yaml
```

## 6. Thư mục bằng chứng

| File | Ai ghi | Nội dung |
| --- | --- | --- |
| `board-map.json` | push | `{key: {so, url, id, node_id, item_id, buoc: tao\|them\|field\|cha, cha, cha_ok, bam, bam_than}}` — ghi sau mỗi bước, chạy lại đi tiếp từ `buoc` |
| `field-list.json` | push, snapshot | id Project, id field, id lựa chọn đọc qua GraphQL; đúng owner + số Project thì dùng lại, `--doc-lai-field` để đọc lại |
| `board-snapshot.json` | snapshot | item, nhãn, người phụ trách, cha, giá trị field; `--body` thêm băm thân |
| `bodies/<key>.md` | push --dry-run --ghi-than | thân sắp đăng, để gate của dự án quét (`/` trong key đổi thành `-`) |
| `log/<epic>.jsonl` | push, snapshot | mỗi lệnh `gh`: giờ, thao tác, mã HTTP, điểm còn lại — không thân, không token |
| `PUSH_RUNNING` | push | đặt khi bắt đầu, gỡ khi xong; còn cờ thì lượt push khác từ chối (exit 3) |
| `BREAK_RUNNING` (`--co-chan`) | dự án | cờ chặn: còn cờ thì push và snapshot dừng |

`bam_than` = sha256 thân đã chuẩn hoá xuống dòng; `bam` = sha256 của (title, bam_than, nhãn đã sắp). `--cap-nhat` PATCH khi `bam` khác seed.

## 7. File cấu hình (`--config`, tuỳ chọn)

```yaml
repo: acme/shop
project_owner: acme
project_number: 5
seed_dir: seed                 # đường dẫn tương đối tính từ thư mục chứa file cấu hình
evidence_dir: evidence
khuon: khuon-issue.md          # thứ tự mục thân; mẫu ở templates/
spec_registry: spec/registry   # tuỳ chọn, xem mục 8
nhip_phut: 40
nhip_gio: 450
co_chan: [../khac/BREAK_RUNNING]
than: {tran: 2500, cho_trong: "_(chưa viết)_", cjk_toi_da: 11, dinh_nghia_xong_story_theo_nhan: {"constraint:hitl": ["…"]}}
van: {khoang: {story: {luong_chinh: [3, 7]}}, can_chu: {story: [mo_ta, pham_vi]}}
spec: {loai_man: {一覧: "一覧 (danh sách)"}, tang: {}, thiet_bi: {office: "văn phòng"}, ngoai_bang: [giao-dien],
       ghi_chu_validation: "", trien_khai: {tieu_de: "Thiết kế hệ thống mục 10", ten: {thu_tu: "thứ tự triển khai"}}}
```

Tham số dòng lệnh cùng tên đè khoá trong file. Mặc định thân: trần 65.536 ký tự (trần GitHub), không kiểm chữ Nhật liền.

## 8. Registry spec (`--spec-registry`, tuỳ chọn)

Có registry thì «Spec nguồn» in mã spec của màn và API, và thân story/leaf có mục «Dữ liệu từ spec» (số item, số điều kiện validation — chỉ đếm, không chép —, FR chi phối, API phục vụ, bảng, story cha, epic). Bố cục registry theo Spec Standard:

- `spec-standard.yaml › screens[]{sc}` theo thứ tự gán mã, `id_ranges.{screen, khuon_bao_cao, api, detail}.{prefix, start}`
- `screens-design.yaml › man[]{sc, ten_vi, items[]{tu, ghi}, validation[], fr_chi_phoi, tang_dac_quyen, thiet_bi, thuc_the_chinh, loai}`
- `api-design.yaml › apis[]{api_id, method, route}` theo thứ tự, ứng với `API-<start + i>`

Không có registry: mục «Dữ liệu từ spec» bị bỏ hẳn, «Spec nguồn» chỉ liệt mã trong `spec_refs` theo nhóm (Màn, Khuôn, API, Luồng kỹ thuật, Bảng, FR, ADR, NFR, Mã khác).

## 9. Khuôn issue (`--khuon`)

Mỗi tiêu đề `### …` mở một loại issue: `Epic`, `Story`, `Investigation`, hoặc `(leaf FE / BE / DB / INFRA)`, `(leaf TEST)`. Bảng ngay dưới có cột đầu là tên mục, từ trên xuống là thứ tự trong thân. Được đổi chỗ hoặc bỏ mục; tên mục phải nằm trong `scripts/khuon.py › MAC_DINH`. Mẫu: `templates/khuon-issue.md`.

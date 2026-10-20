---
name: create-gh-issues
description: Tạo issue từ seed YAML và đẩy backlog lên GitHub Project v2 theo tầng epic → story → sub-issue, đặt field Status/Owner/Priority, chạy lại không tạo trùng — dùng khi người dùng nói «tạo issue từ seed», «đẩy backlog lên GitHub Project», «nối sub-issue» hoặc gọi «create-gh-issues».
---

# create-gh-issues

Một lệnh Python (`scripts/gh_issues.py`) đọc thư mục seed YAML, dựng thân issue theo khuôn, rồi tạo issue, thêm vào Project v2, đặt field và nối cha–con bằng sub-issue của GitHub. Mọi bước ghi lại vào `board-map.json`, nên chạy lại chỉ làm phần còn thiếu.

## Khi nào dùng

- Đã có backlog dạng YAML (epic → story/điều tra → leaf FE, BE, DB, TEST, INFRA) và cần đưa lên GitHub Project để cả đội theo dõi.
- Cần đẩy theo lô epic, dừng giữa chừng được, chạy lại không sinh issue trùng.
- Cần kiểm board có khớp seed không (thiếu, lạ, trùng, lệch nhãn, lệch Owner/Priority, mồ côi, thân bị sửa tay).

Không dùng để: tạo hay sửa field của Project, xoá issue, quản lý sprint, Story Point, giờ công.

## Điều kiện

- `gh` đã đăng nhập (`gh auth status`) với scope `repo` và `project`. Skill chỉ gọi `gh api`, không đọc, không in, không lưu token.
- Project v2 (của user hoặc org) đã có field single-select **Status, Owner, Priority** với đủ lựa chọn mà `team.yaml` dùng. Skill không tạo field.
- Repo đã có các nhãn trong `labels.yaml` (chạy lệnh `labels --create` nếu chưa).
- Python 3.10 trở lên, có PyYAML.

## Đầu vào

- `--seed-dir`: `backlog/<EPIC>.yaml` (một file một epic), `team.yaml` (Owner, Priority, Status, người phụ trách, mẫu định nghĩa xong), `labels.yaml`; tuỳ chọn `premise.yaml`, `gaps.yaml`.
- `--repo owner/name`, `--project-owner <login>`, `--project-number <số>`: id Project, field, lựa chọn đọc bằng GraphQL lúc chạy, đệm vào `<evidence-dir>/field-list.json`.
- `--evidence-dir`: nơi ghi `board-map.json`, `board-snapshot.json`, `bodies/`, `log/`, cờ.
- Tuỳ chọn: `--khuon` (thứ tự mục thân, mẫu `templates/khuon-issue.md`), `--spec-registry` (registry spec: in mã spec và mục «Dữ liệu từ spec»; không có thì mục này bị bỏ), `--config` (file YAML gom mọi tham số trên).
- Key là từ thứ hai của title: `[STORY] SC-031 Danh sách giao dịch`. Đừng sửa title trên web.

Schema đầy đủ, bảng file bằng chứng và khoá cấu hình: [docs/seed-schema.md](docs/seed-schema.md).

## Các lệnh

Đặt biến cho gọn (đường dẫn ví dụ):

```bash
S=skills/create-gh-issues/scripts
CHUNG="--repo acme/shop --project-owner acme --project-number 5 --seed-dir seed --evidence-dir bang-chung --khuon skills/create-gh-issues/templates/khuon-issue.md"
```

1. Kiểm seed trước (không gọi mạng):
   `python3 $S/gh_issues.py check --seed --van $CHUNG`
2. Xem thử thân một issue:
   `python3 $S/gh_issues.py render --key SC-031 $CHUNG`
3. Tạo nhãn repo — chạy không `--create` để xem lệnh trước:
   `python3 $S/gh_issues.py labels $CHUNG` rồi `python3 $S/gh_issues.py labels --create $CHUNG`
4. Chạy thử lô đầu, ghi thân ra `bang-chung/bodies/` để quét:
   `python3 $S/gh_issues.py push --lo E15 --dry-run --ghi-than $CHUNG`
   Kết quả thật ở LAB-5 khi chạy lệnh này kèm `--cap-nhat` (map đã có sẵn 3 khoá của lô):
   `E15: tạo mới 8 · nhận lại 3 · lỗi 0 · bước dở 0 · cập nhật 3`
   `dry-run E15: 11 khoá · addProjectV2ItemById 8 · sua-issue 3 · sub_issues 8 · tao-issue 8 · updateProjectV2ItemFieldValue 8 · 35 lệnh ghi ≈ 0.9 phút …`
5. Quét `bang-chung/bodies/` bằng gate của dự án (RFP, bí mật, tên người…). Đạt rồi mới đẩy thật:
   `python3 $S/gh_issues.py push --lo E15 --da-quet --lenh-quet "python3 tools/quet-than.py bang-chung/bodies" $CHUNG` (lệnh quét là của dự án bạn)
6. Đẩy các lô còn lại (trong mỗi lô: epic → story/điều tra → leaf, cha luôn trước con):
   `python3 $S/gh_issues.py push --lo FG-01,FG-02 --da-quet $CHUNG`
   Thân trong seed đã đổi sau khi đẩy: thêm `--cap-nhat`. Chỉ đặt lại field: `--chi-field`.
7. Chụp board rồi kiểm khớp seed:
   `python3 $S/gh_issues.py snapshot --body $CHUNG` rồi `python3 $S/gh_issues.py check --snapshot $CHUNG`
   (Project để riêng tư thì thêm `--cho-phep-rieng`.)

Mã thoát: 0 xong hoặc PASS · 1 lỗi GitHub, FAIL hoặc từ chối đăng · 2 lỗi dữ liệu hoặc tham số · 3 cờ `PUSH_RUNNING` đang có.

## Luật an toàn

- **Thân phải qua gate của dự án trước khi đăng.** Lượt thật từ chối khi thiếu `--da-quet`, khi thân sắp đăng khác bản ở `bodies/`, hoặc khi một `--lenh-quet` không thoát 0. `--ghi-than` chỉ đi với `--dry-run`. Skill không kèm gate quét nội dung — mỗi dự án tự mang gate của mình.
- Nhịp: ≤ 40 lệnh ghi mỗi phút, ≤ 450 mỗi giờ (`--nhip-phut`, `--nhip-gio`). Cứ 50 lệnh đọc `rate_limit` một lần, điểm còn dưới 200 thì chờ tới giờ đặt lại. Bị chặn 403/429 thì chờ theo `retry-after`, nhân đôi mỗi lần; bị chặn quá 3 lần trong một giờ thì dừng cả loạt.
- Chạy lại không trùng: trước mỗi lượt thật, liệt kê issue của repo và nhận các key đã có. Lệnh tạo không rõ kết quả (hết giờ, 5xx) thì liệt kê lại rồi mới quyết tạo lại. Nối cha bị 422 thì hỏi cha hiện tại: đúng thì nhận, khác thì dừng (không dùng `replace_parent`).
- Cờ `PUSH_RUNNING` trong thư mục bằng chứng: đặt khi chạy, gỡ khi xong; còn cờ thì lượt khác từ chối. Cờ chặn ngoài (`--co-chan`, mặc định `BREAK_RUNNING`) làm push và snapshot dừng.
- Không ghi token ở đâu cả; log JSONL chỉ có giờ, thao tác, mã HTTP, điểm còn lại.
- Không xoá gì. Issue trùng thì đóng tay bản thừa và gắn nhãn `da-thay-the` (tách khỏi `spec-gap` = chỗ hở); lần chạy sau tự bỏ qua bản đó.

## Giới hạn

- Chỉ Project v2 của user hoặc org mà tài khoản `gh` có quyền ghi.
- Chỉ đặt Status, Owner, Priority (single-select). Không tạo field hay lựa chọn; Sprint, Story Point, giờ công làm bằng công cụ khác.
- Không xoá, không đổi cha của issue đã có cha.
- Tối đa 100 sub-issue mỗi cha (trần GitHub); `check --seed` báo trước.
- GraphQL tính điểm: đọc field 1 lần mỗi Project (có đệm), snapshot khoảng 1 điểm mỗi trang 100 item; lượt đẩy dùng chủ yếu REST và mutation, mỗi khoá 3–5 lệnh ghi (epic không có bước nối cha; `--cap-nhat` thêm một lệnh sửa).
- Thân issue tối đa 65.536 ký tự (trần GitHub); trần thấp hơn đặt ở `than.tran` của file cấu hình.

## Cách dùng với Agent

Giao cho agent theo đúng thứ tự, mỗi bước dừng lại báo kết quả:

```text
Dùng skill create-gh-issues với file cấu hình gh-issues.yaml.
1. check --seed --van: phải PASS, báo dòng đếm epic/story/leaf.
2. push --lo <lô thử> --dry-run --ghi-than: báo số khoá, số lệnh ghi theo loại, giờ ước.
3. Chạy gate quét thân của dự án trên bang-chung/bodies/; đỏ thì dừng, báo file và dòng.
4. Chờ tôi duyệt, rồi push --lo <lô thử> --da-quet; báo dòng «tạo mới · nhận lại · lỗi · bước dở».
5. snapshot --body rồi check --snapshot --lo <lô thử>: phải PASS.
6. Đẩy các lô còn lại từng lô một, sau mỗi lô lặp bước 5. Gặp DỪNG thì không thử lại mù: đọc bang-chung/log/, báo tôi.
Không xoá gì, không sửa title trên web, không chạy hai lượt push cùng lúc.
```

Agent không được tự thêm `--da-quet` khi chưa có kết quả quét thân của dự án.

## Nguồn gốc

Xây cho LAB-5 (dự án mẫu Sakura Market, chương trình AIDD for Leaders của Sun*): đẩy backlog 19 epic, 496 khoá từ seed YAML lên GitHub Project, mỗi khoá một issue có sub-issue, Owner, Priority. Bản này tách khỏi công cụ của bài lab: mọi tên repo, số Project, id field và đường dẫn đều đến từ tham số; bộ dựng thân cho ra đúng từng byte thân issue của bài lab khi dùng cùng seed, registry spec và cấu hình.

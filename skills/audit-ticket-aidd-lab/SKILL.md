---
name: audit-ticket-aidd-lab
description: Audit ticket trên GitHub Project v2 theo bảng tiêu chí YAML (quy ước vận hành Project của công ty, bản mã hoá, cộng quy ước tự khai của dự án) — chụp Project chỉ đọc, chạy luật trên ảnh chụp, xuất báo cáo HTML liệt kê từng ticket vi phạm, rule bị phạm, sai ở đâu và cách sửa, theo mức Chặn / Lệch quy ước / Ghi nhận. Dùng khi người dùng nói «audit ticket», «kiểm board theo quy ước», «ticket có đúng quy định không», «/audit-ticket-aidd-lab».
---

# audit-ticket-aidd-lab

Kiểm từng issue trên GitHub Project v2 có được vận hành đúng quy ước không: tiêu đề, nhãn, field bắt buộc, cha–con, trùng, Sprint, tổng cha, trạng thái, phụ thuộc giữa việc lá, quá hạn. Tiêu chí là dữ liệu (`tieu-chi.yaml`) để người duyệt sửa mức hay tắt một tiêu chí mà không đụng mã. Skill **chỉ đọc**: không sửa issue, field hay nhãn; sửa là việc riêng sau khi người đọc báo cáo.

## Khi nào dùng

- Trước buổi lập kế hoạch sprint, sau một lượt ghi hàng loạt lên Project, trước khi nộp hoặc bàn giao board.
- Cần một bảng «tiêu chí nào đang dùng, cái nào không áp dụng và vì sao» để người khác duyệt.

Không dùng để: sửa board, đọc thân issue (skill chỉ đọc field và cấu trúc), chấm điểm hay ước giờ.

## Điều kiện

- Python 3.10 trở lên, có PyYAML.
- Lệnh `snapshot` cần `gh` đã đăng nhập (`gh auth status`) với scope `read:project` và `repo`. Skill chỉ gọi query GraphQL, không mutation, không đọc hay in token.

## Tệp

| Tệp | Vai trò |
| --- | --- |
| `tieu-chi.yaml` | 39 tiêu chí theo chiều A–L: mã, tên, nguồn, cách đo, mức (B/W/I), áp dụng hay không và lý do |
| `config/lab5.yaml` | Cấu hình board mẫu (LAB-5): repo, số Project, field, luồng Status, tiền tố tracker, hậu tố việc lá, nhãn, Priority, năng lực sprint, luật Owner, ngày xét |
| `scripts/audit_board.py` | Ba lệnh `snapshot`, `audit`, `tieu-chi` |
| `scripts/luat_*.py` | Một hàm cho mỗi tiêu chí áp dụng, đăng ký theo mã |
| `docs/tieu-chi.md` | Bảng tiêu chí sinh từ `tieu-chi.yaml` (lệnh `tieu-chi`) |
| `templates/khung-bao-cao.html` | Khung HTML của báo cáo (CSS, JS lọc và tìm nội tuyến) |
| `vi-du/` | Ảnh chụp mẫu 26 issue, seed, kế hoạch sprint, phụ thuộc mẫu; khoá `mong_doi` trong ảnh ghi tập issue mỗi tiêu chí phải bắt |

## Các lệnh

```bash
# chạy từ gốc repo, bằng python có PyYAML (pip install pyyaml)
S=skills/audit-ticket-aidd-lab/scripts
# 0. Chạy thử không cần mạng trên ảnh chụp mẫu đi kèm (26 issue, mỗi tiêu chí có vi phạm cài sẵn)
V=skills/audit-ticket-aidd-lab/vi-du
python3 $S/audit_board.py audit --snapshot $V/anh-chup-mau.json --seed-dir $V/seed-mau \
  --sprint-plan $V/sprint-plan-mau.json --phu-thuoc $V/phu-thuoc-mau.yaml --out bao-cao-mau.html
# 1. Chụp Project (chỉ đọc) → ảnh chụp JSON
python3 $S/audit_board.py snapshot --config skills/audit-ticket-aidd-lab/config/lab5.yaml --out bang-chung/anh-chup.json
# 2. Audit trên ảnh chụp (không gọi mạng); ba nguồn ngoài là tuỳ chọn, tệp của dự án bạn.
#    Repo này: seed epic ở backlog/backlog/ (backlog/ ngoài cùng là tệp đội, nhãn, tiền đề — không phải seed)
python3 $S/audit_board.py audit --snapshot bang-chung/anh-chup.json \
  --seed-dir backlog/backlog --sprint-plan sprint-plan.json --phu-thuoc phu-thuoc-la.yaml \
  --out bao-cao-audit.html        # bỏ --out cũng ra tệp này; --out *.md ra Markdown
# 3. In bảng tiêu chí
python3 $S/audit_board.py tieu-chi --out skills/audit-ticket-aidd-lab/docs/tieu-chi.md
```

`--config` và `--tieu-chi` mặc định là hai tệp trong thư mục skill. Lỗi đầu vào (thiếu tệp, YAML hỏng, `gh` chưa đăng nhập) in một dòng `LỖI:` và trả mã 2.

Nguồn ngoài, thiếu thì tiêu chí in «bỏ qua: thiếu nguồn», không báo vi phạm:

| Cờ | Tiêu chí | Khuôn |
| --- | --- | --- |
| `--seed-dir` | A1 (đủ và không lạ), E2 (đúng epic) | thư mục chứa trực tiếp các tệp `<EPIC>.yaml`; mỗi tệp có khối `epic` và danh sách `items`, mỗi mục mang trường `key`; không có tệp epic nào thì dừng với `LỖI:` |
| `--sprint-plan` | B1 (Sprint khớp kế hoạch) | JSON `{sprint, muc: [{key, start, due}]}` |
| `--phu-thuoc` | G4 (việc lá đóng không trái phụ thuộc) | YAML `cung_story`, `moc`, `ngoai_le_epic`, `ngoai_le_tien_to` |

## Đầu ra

Mặc định là **một tệp HTML tự chứa** (không tải gì từ mạng, mở thẳng bằng trình duyệt, sáng/tối theo máy, đọc được trên điện thoại):

- Đầu trang: Project, giờ chụp, ngày xét, số issue; ô đếm Chặn / Lệch quy ước / Ghi nhận, số ticket vi phạm, số rule có vi phạm, mã bị bỏ qua vì thiếu nguồn.
- Thanh lọc: tab **Theo ticket** · **Theo rule** · **Tiêu chí**, bật tắt từng mức, chọn một rule, ô tìm theo `#số` hoặc khoá.
- **Theo ticket** (mặc định): mỗi ticket vi phạm một dòng, xếp mức nặng nhất trước; mở ra thấy giá trị hiện tại của ticket (Status, Owner, Priority, Sprint, ngày, Story Point, giờ, trạng thái issue GitHub, cha, nhãn) và từng rule nó phạm: mã, mức, rule nói gì, **sai ở đâu** (lý do do luật sinh, có giá trị cụ thể), **cách sửa** (khoá `cach_sua` của `tieu-chi.yaml`), nguồn rule. Số issue là link mở GitHub; thêm `#t-<số>` vào URL để mở thẳng ticket đó.
- **Phát hiện không gắn một ticket**: khoá seed thiếu issue, tải vượt trần theo Owner × Sprint, Project chưa public hay thiếu field.
- **Theo rule**: mỗi rule có vi phạm một mục, liệt kê ticket kèm lý do. **Tiêu chí**: đủ 39 tiêu chí với kết quả (số phát hiện, bỏ qua, không áp dụng kèm lý do) và cách sửa.

`--out <tệp>.md` ra báo cáo Markdown cùng nội dung theo rule (dùng để so bằng diff): Kết luận → Chặn / Lệch quy ước / Ghi nhận → Không áp dụng → Phủ chiều (in cả số 0) → phụ lục, danh sách đủ khi bảng bị cắt (60 dòng mỗi tiêu chí).

## Dùng cho board khác

1. Chép `config/lab5.yaml` thành tệp mới, sửa `repo`, `project_owner`, `project_number`, `field_map` (tên field trên Project), `status_luong`, `tracker_tien_to`, `la_hau_to`, nhãn, `nang_luc_sprint`, `owner`.
2. Bỏ khoá `ngay_xet` nếu board chạy thật. Khoá này cố định ngày xét quá hạn cho board **giả lập** (LAB-5: ngày chụp giả lập Sprint 1); để nguyên trên board thật thì H1 (quá hạn) và G2 đo theo ngày sai. Báo cáo chỉ cảnh báo chiều ngược lại (có Done Date sau ngày xét).
3. `owner.chuyen` là danh sách việc lá được chuyển giữa hai vị trí cùng bộ phận để cân tải; ở LAB-5 nó chép từ `owner-chuyen.yaml` của dự án và có test đồng bộ. Board khác phải tự giữ danh sách này, nếu không D4 báo các lá đã chuyển là sai Owner.
4. Sửa `tieu-chi.yaml`: đổi `muc`, hoặc `ap_dung: false` kèm `ly_do` cho tiêu chí không hợp với board. Mã áp dụng mà chưa có hàm luật thì lệnh `audit` dừng với lỗi.

## Giới hạn

- Thước đo là bản mã hoá của quy ước công ty (tracker, khuôn tiêu đề, field bắt buộc, nhãn, cha–con, trùng, trạng thái, quá hạn, bug), không phải nguyên văn quy định. Báo cáo ghi rõ điều này ở đầu.
- Không đọc thân issue: các tiêu chí cần thân (khớp phạm vi story, Sprint ghi trong thân) để «không áp dụng».
- Cột `nguon` và `gate` của `tieu-chi.yaml` trỏ tới tệp và gate của bộ công cụ LAB-5 nằm ngoài repo nộp, chỉ để truy vết; skill không gọi chúng.
- Test của skill nằm ở bộ công cụ LAB-5 (`lab-05/tools/tests/test_skill_audit_*.py`), không đi kèm repo nộp; test đọc chính ảnh chụp mẫu ở `vi-du/` và so tập phát hiện với `mong_doi`.

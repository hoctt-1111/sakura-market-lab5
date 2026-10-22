# Khuôn issue — LAB-5 Sakura Market (bản để user duyệt, U11)

> Bản chép khuôn đã duyệt (U11) để dùng lại với skill create-gh-issues. Chỉ đổi những chỗ gắn với kho làm việc của LAB-5: đường dẫn seed, tên công cụ, tài khoản phụ trách, nơi để issue mẫu. `gh_issues.py --khuon <file này>` đọc thứ tự mục ở các bảng mục 2; sửa bảng để đổi chỗ hoặc bỏ bớt mục (tên mục phải là tên bộ dựng biết, xem `scripts/khuon.py`).

Mọi issue trên Project sinh từ seed `<seed-dir>/backlog/<epic>.yaml` qua `scripts/than_issue.py`. Khuôn này chốt: tiêu đề, thứ tự và tên mục trong thân, mục nào máy sinh từ seed, mục nào agent viết, độ dài, nhãn và field. Thân dựng theo đúng thứ tự mục dưới đây; `gh_issues.py check --seed --van` kiểm độ dài văn.

## 1. Quy ước chung

- Tiêu đề: `[TRACKER] <key> <tên tiếng Việt>`; key là từ thứ hai, không đổi sau khi tạo. Tracker: `EPIC` · `STORY` · `DEV TASK` · `TEST DESIGN` · `INVESTIGATION`.
- Ngôn ngữ: tiếng Việt tự viết; thuật ngữ Nhật ghi kèm nghĩa một lần trong mỗi issue, ví dụ `相対取引 (giao dịch thỏa thuận)`. Không chép câu từ spec hay RFP; không đoạn chữ Nhật dài.
- Số: mọi con số trong thân phải có trong spec LAB-4 hoặc PREMISE; không bịa ngưỡng.
- Mã trỏ nguồn: spec LAB-4 ghi bằng mã (`SPEC-SKM-118`, `SKM_AITAI_TRADE_CREATE`, bảng `transactions`, `FR-AITAI-02`, `ADR-003`) kèm tóm tắt tiếng Việt; không dẫn đường dẫn kho làm việc.
- Nhãn: một nhãn `type:*` theo tracker; leaf FE/BE/DB thêm `team:frontend|backend`, leaf INFRA thêm `team:infrastructure`; nhãn `constraint:*` kế thừa từ story; `spec-gap` khi issue có mục «Chỗ hở».
- Field trên Project: Status = New lúc tạo · Owner theo vai (`team.yaml`) · Priority theo `priority_map` · Assignee = tài khoản ở `team.yaml › assignee`. Sprint, Story Point, Estimated time, Spent time để trống ở đầu việc 1–2, điền ở đầu việc 3–4.
- Cha–con: epic ← story ← leaf bằng sub-issue của GitHub; issue điều tra là con trực tiếp của epic.

## 2. Thân theo tracker (thứ tự mục cố định)

### 2.1 Epic — `[EPIC] FG-04 Giao dịch thỏa thuận 相対取引`
| Mục | Ai viết | Độ dài |
| --- | --- | --- |
| Mục tiêu | agent (`mo_ta`) | 2–3 câu: nhóm chức năng này giải quyết việc gì của chợ |
| Phạm vi | máy từ seed | danh sách story con (key — tên) |
| Tiêu chí hoàn thành epic | agent (`tieu_chi_nghiem_thu`) | 2–4 mục, mục đầu luôn «mọi story con đóng» |
| Ràng buộc đặc thù | agent, chỉ khi epic có nhãn `constraint:*` | 1–2 câu: ràng buộc tác động gì tới epic |
| Spec nguồn | máy từ `spec_refs` | mã FG, SPEC-SKM, ADR, NFR |

### 2.2 Story — `[STORY] SC-031 Danh sách giao dịch 相対`
| Mục | Ai viết | Độ dài |
| --- | --- | --- |
| Mô tả | agent (`mo_ta`) | 2–4 câu: ai dùng, làm gì, vì sao cần |
| Phạm vi | agent (`pham_vi`) | màn, API, bảng liên quan bằng mã + tên tiếng Việt |
| Luồng chính | agent (`luong_chinh`) | 3–7 bước, mỗi bước «ai làm gì» |
| Tiêu chí nghiệm thu | agent (`tieu_chi_nghiem_thu`) | 2–6 mục dạng «Khi … thì …»; bước người xác nhận phải nêu ai xác nhận và hệ thống ghi gì |
| Định nghĩa xong | máy (mẫu story trong `team.yaml`) + agent (`dinh_nghia_xong`, chỉ phần thêm) | mẫu: mọi sub-issue đóng, tiêu chí đã chạy qua; thêm nếu có |
| Ràng buộc đặc thù | agent, chỉ khi có nhãn `constraint:*` | 1–2 câu |
| Dữ liệu từ spec | máy từ seed | số item, số validation, FR chi phối, tầng đặc quyền, thiết bị, thực thể chính, API phục vụ |
| Tiền đề | máy từ `premise_refs` | P-xx — tóm tắt một dòng |
| Chỗ hở | máy từ `gap_refs` | G-xx — tóm tắt một dòng |
| Spec nguồn | máy từ `spec_refs` | mã SPEC-SKM, API, bảng, FR, ADR |

### 2.3 Dev Task (leaf FE / BE / DB / INFRA / PM / BRSE) — `[DEV TASK] SC-031/BE API danh sách giao dịch`
| Mục | Ai viết | Độ dài |
| --- | --- | --- |
| Mô tả | agent (`mo_ta`) | 1–2 câu: phần việc của bộ phận này trong story |
| Tiêu chí nghiệm thu | agent (`tieu_chi_nghiem_thu`) | 1–3 mục kiểm được riêng cho bộ phận |
| Định nghĩa xong | máy (mẫu theo loại leaf trong `team.yaml`) | FE: màn dựng đúng wireframe, validation phía giao diện, kiểm thử giao diện · BE: API theo spec, validation phía máy chủ, kiểm thử đơn vị · DB: migration + rollback, ràng buộc, dữ liệu mẫu · INFRA: môi trường/pipeline chạy xanh, tài liệu vận hành |
| Dữ liệu từ spec | máy từ seed | route API, bảng và vai trò (chủ migration hay chỉ đọc), item ghi/đọc, validation, nhãn ràng buộc, story cha, epic |
| Ràng buộc đặc thù | agent, chỉ khi có nhãn `constraint:*` | 1 câu |
| Spec nguồn | máy | mã |

Lá PM (quản lý sprint, `team:pm`) và BRSE (cầu nối khách, `team:brse`) dùng cùng khuôn này; mẫu «Định nghĩa xong» lấy theo loại leaf trong `team.yaml`.

### 2.4 Test (leaf TEST) — `[TEST DESIGN] SC-031/TEST Kiểm thử danh sách giao dịch`
| Mục | Ai viết | Độ dài |
| --- | --- | --- |
| Mô tả | agent (`mo_ta`) | 1–2 câu: phạm vi kiểm thử của story |
| Ca kiểm thử bắt buộc | agent (`tieu_chi_nghiem_thu`) | 1–3 mục; story có người xác nhận phải có ca chứng minh kết quả luôn đi qua người xác nhận |
| Định nghĩa xong | máy (mẫu TEST) | ca thiết kế xong, chạy trên staging, kết quả ghi vào story |
| Dữ liệu từ spec | máy | số validation, FR chi phối, API, tầng đặc quyền |
| Spec nguồn | máy | mã |

### 2.5 Investigation — `[INVESTIGATION] INV-Q-SD4 Vai nội bộ của 照合事務 và 取引運用`
| Mục | Ai viết | Độ dài |
| --- | --- | --- |
| Câu hỏi | máy từ seed (`mo_ta` = câu hỏi gốc viết lại bằng tiếng Việt) | 1–3 câu |
| Giả định đang dùng | máy từ `premise_refs` (dòng P-xx) | 1 dòng |
| Người trả lời · Mốc | máy từ seed (owner, hạn) | 1 dòng |
| Issue bị ảnh hưởng | máy từ `anh_huong` của P-xx | danh sách key |
| Định nghĩa xong | máy (mẫu INV) | có câu trả lời ghi trong issue, PREMISE cập nhật, issue ảnh hưởng được sửa hoặc xác nhận giữ |
| Nguồn | máy từ seed (`nguon`) | chỗ trong tài liệu nguồn đặt ra câu hỏi, mỗi chỗ một dòng; tên tệp bỏ đuôi, khoá registry viết lại thành câu (`than.nguon_doi`) |

## 3. Giới hạn kỹ thuật
- Thân ≤ 2.500 ký tự; mục trống thì bỏ cả tiêu đề mục (trừ mục bắt buộc của tracker).
- Thứ tự mục đúng bảng trên (bộ dựng đọc chính các bảng này qua `--khuon`); `check --seed --van` đo độ dài văn.
- Khối «Dữ liệu từ spec» và «Định nghĩa xong» máy sinh, agent không sửa.

## 4. Bốn issue mẫu
Dựng thật từ seed bằng `gh_issues.py render --key <key>`, ví dụ E15, SC-031, SC-031/BE, INV-Q-SD4.

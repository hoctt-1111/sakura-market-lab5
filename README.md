# Sakura Market — hệ quản lý chợ thủy sản Vịnh Sakura (LAB-5: backlog và GitHub Project)

<!-- gen:readme-dau:start -->
Học viên: Trần Thái Học · mã học viên HocTT · lớp CEVC4, nhóm 3 · Đề: Product A — 産地市場 (chợ bán buôn thủy sản ngay cảng cá, mua thẳng từ tàu).
<!-- gen:readme-dau:end -->

## Tổng quan

Repo này giữ phần chia việc của LAB-5 cho hệ quản lý chợ thủy sản Vịnh Sakura. Backlog epic → issue → sub-issue nằm trên GitHub Project; các file Markdown ở gốc repo giải thích backlog lấy từ bản LAB-4 nào, khác bản đó ở đâu và vì sao. Mọi con số dưới đây do chương trình đếm tự động từ bộ dữ liệu nguồn của backlog (các file YAML trong `backlog/`) và ảnh chụp Project, không gõ tay.

<!-- gen:readme-tong-quan:start -->
- Mốc chia việc: bản LAB-4 đã nộp — repo `hoctt-1111/sakura-market-lab4-spec`, nhánh `main`, commit `3ab06e6`, nộp ngày 12/10/2026.
- `PREMISE.md`: có thay đổi so với LAB-4 — 10 dòng spec thêm, bỏ hoặc sửa · 28 giả định bổ sung · 4 hướng đã chốt.
- Backlog: 19 epic (14 nhóm chức năng FG-01…FG-14, 5 epic xuyên suốt E15…E19) · 119 story · 29 issue điều tra · 329 sub-issue lá (Dev Task, Test Design) — tổng 496 issue.
- Trên Project (ảnh chụp 2026-10-13): 496 issue.
- Sprint giả lập: chưa chạy — cập nhật ở đầu việc 4.
<!-- gen:readme-tong-quan:end -->

## Link

Repo và Project đều công khai: người ngoài mở được bằng trình duyệt mà không cần đăng nhập. Project có ba chế độ xem: «Bảng theo trạng thái», «Bảng nhóm theo issue cha» (cây epic → issue → sub-issue) và «Lộ trình theo Sprint». Cột Assignees (người được giao) của mọi issue là cùng một tài khoản, tài khoản của học viên; người phụ trách giả định nằm ở field «Owner» và ghi theo vai (PM, BrSE, FE-1, FE-2, BE-1, BE-2, QA, Infra), không phải tên người thật.

<!-- gen:readme-link:start -->
- Repo: https://github.com/hoctt-1111/sakura-market-lab5
- GitHub Project: https://github.com/users/hoctt-1111/projects/3
- Báo cáo HTML của skill chấm SWP: `reports/` — thêm ở đầu việc 3
- Kiểm công khai: đã mở thử repo và Project bằng cửa sổ ẩn danh lúc 13:39 ngày 13/10/2026.
<!-- gen:readme-link:end -->

## Cấu trúc repo

Bảng liệt kê mọi mục ở gốc repo. Bộ sinh đọc cây thật lúc chạy, nên mục nào thêm hoặc bớt thì bảng đổi theo; mục chưa có nội dung ghi rõ đầu việc sẽ điền.

<!-- gen:readme-cau-truc:start -->
| File/thư mục | Nội dung |
| --- | --- |
| `README.md` | Trang đầu: tổng quan, link repo và Project, cấu trúc repo, bảng spec LAB-4 → epic trên Project |
| `PREMISE.md` | Tiền đề: backlog khác bản LAB-4 đã nộp ở đâu — spec thêm, bỏ, sửa; giả định bổ sung; hướng đã chốt |
| `task-breakdown.md` | Nguyên tắc chia task, bảng spec → issue, hạng mục chịu ràng buộc đặc thù, chỗ hở của spec LAB-4 |
| `estimate.md` | SWP đã review và giờ ước lượng cho từng issue — điền ở đầu việc 3 |
| `progress-report.md` | Báo cáo tiến độ của sprint giả lập — điền ở đầu việc 4 |
| `AI-report.md` | Cách dùng AI cho break task, chấm SWP, quy giờ, báo cáo tiến độ — điền ở plan sau |
| `reports/` | Báo cáo HTML của skill chấm SWP — thêm ở đầu việc 3 |
| `skills/` | Skill tự viết: `create-gh-issues` |
| `backlog/` | Seed YAML sinh issue trên Project, cùng một nguồn với Project (23 file: epic, đội, nhãn, PREMISE, chỗ hở) |
| `.gitignore` | Bỏ khỏi git file tạm của máy, file PDF và file `.env*` |
<!-- gen:readme-cau-truc:end -->

## Spec → epic

Mỗi dòng nối một phần spec LAB-4 (nhóm chức năng, màn, API, luồng kỹ thuật, ADR, yêu cầu phi chức năng) hoặc một dòng PREMISE với epic trên Project. Cột Ghi chú nêu ràng buộc đặc thù của Product A mà issue trong epic mang nhãn, để người đọc thấy ngay các hạng mục như 完納奨励金 (thưởng thanh toán đủ hạn), 相対取引 (giao dịch thỏa thuận) và hai tầng đặc quyền 許可 / 承認 được tách thành issue riêng, không gộp vào việc chung.

<!-- gen:readme-spec-epic:start -->
| Spec (mã/file LAB-4 hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
| --- | --- | --- |
| `FG-01` `account-access`<br>SC-001, SC-002, SC-003, SC-004, SC-005, SC-006<br>API-201, API-202, API-203<br>ADR-011<br>NFR-SEC-03<br>Q-SD3, Q-SD4<br>dòng PREMISE P-01, P-03, P-04, P-05, P-06, P-12, P-15, P-28 | [#35](https://github.com/hoctt-1111/sakura-market-lab5/issues/35) — Tài khoản và quyền nội bộ | Ràng buộc đặc thù 許可 / 承認 (hai tầng đặc quyền): 1 issue |
| `FG-02` `participant-qualification`<br>SC-010, SC-011, SC-012, SC-013, SC-014<br>API-204<br>dòng PREMISE P-01, P-03, P-04, P-05, P-06, P-26, P-29, P-09, P-24 | [#71](https://github.com/hoctt-1111/sakura-market-lab5/issues/71) — Tư cách người tham gia 許可・承認 | Ràng buộc đặc thù 許可 / 承認 (hai tầng đặc quyền): 24 issue |
| `FG-03` `lot-intake`<br>SC-020, SC-021, SC-022, SC-023, SC-024, SC-025<br>API-205, API-206<br>dòng PREMISE P-01, P-03, P-04, P-05, P-06, P-26, P-24 | [#96](https://github.com/hoctt-1111/sakura-market-lab5/issues/96) — Tiếp nhận lô và thẩm định 目利き | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 5 issue |
| `FG-04` `negotiated-trade`<br>SC-030, SC-031, SC-032, SC-033, SC-034<br>API-207, API-208, API-209, API-210, API-221, API-222, API-223<br>TECH-301<br>ADR-003<br>Q-11, Q-21<br>dòng PREMISE P-03, P-04, P-05, P-06, P-07, P-26, P-30, P-08, P-12, P-18, P-20, P-21, P-31, P-24, P-25 | [#128](https://github.com/hoctt-1111/sakura-market-lab5/issues/128) — Giao dịch thỏa thuận 相対取引 | Ràng buộc đặc thù 相対取引 (giao dịch thỏa thuận): 44 issue<br>Ràng buộc đặc thù 許可 / 承認 (hai tầng đặc quyền): 12 issue |
| `FG-05` `auction-result`<br>SC-040, SC-041<br>API-208, API-211, API-212<br>TECH-302<br>dòng PREMISE P-01, P-04, P-05, P-32 | [#172](https://github.com/hoctt-1111/sakura-market-lab5/issues/172) — Kết quả đấu giá せり | Ràng buộc đặc thù 相対取引 (giao dịch thỏa thuận): 3 issue<br>Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 9 issue<br>Ràng buộc đặc thù 許可 / 承認 (hai tầng đặc quyền): 5 issue |
| `FG-06` `correction`<br>SC-050, SC-051, SC-052, SC-053<br>Q-02<br>system-design: A10<br>dòng PREMISE P-01, P-03, P-06, P-16 | [#189](https://github.com/hoctt-1111/sakura-market-lab5/issues/189) — Sửa sau xác nhận và bút toán đảo 赤伝 | — |
| `FG-07` `delivery`<br>SC-060, SC-061, SC-062, SC-063, SC-064<br>Q-SD1<br>system-design: A8<br>dòng PREMISE P-01, P-03, P-06, P-26, P-13, P-33 | [#210](https://github.com/hoctt-1111/sakura-market-lab5/issues/210) — Giao hàng và ngoại lệ giao hàng | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 6 issue |
| `FG-08` `daily-reconciliation`<br>SC-070, SC-071, SC-072, SC-073<br>API-213, API-214<br>Q-SD2<br>system-design: A7, EV3<br>dòng PREMISE P-01, P-03, P-04, P-05, P-06, P-26, P-08, P-14, P-34 | [#235](https://github.com/hoctt-1111/sakura-market-lab5/issues/235) — Đối soát ngày và khoá ngày nghiệp vụ | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 10 issue |
| `FG-09` `full-payment-incentive`<br>SC-080, SC-081, SC-082<br>API-215, API-216<br>TECH-304<br>TECH-304-Q1<br>dòng PREMISE P-01, P-04, P-05, P-26, P-10, P-22, P-35 | [#12](https://github.com/hoctt-1111/sakura-market-lab5/issues/12) — Thưởng thanh toán đủ hạn 完納奨励金 | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 9 issue<br>Ràng buộc đặc thù 完納奨励金 (thưởng thanh toán đủ hạn): 23 issue |
| `FG-10` `rules-and-rates`<br>SC-090, SC-091, SC-092, SC-093<br>API-217, API-218, API-219<br>TECH-303<br>ADR-004<br>Q-09<br>dòng PREMISE P-01, P-03, P-04, P-05, P-06, P-10, P-36 | [#264](https://github.com/hoctt-1111/sakura-market-lab5/issues/264) — Quy chế và biểu suất theo phiên bản | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 5 issue<br>Ràng buộc đặc thù 完納奨励金 (thưởng thanh toán đủ hạn): 5 issue |
| `FG-11` `reporting`<br>SC-100, SC-101, SC-102, SC-103, SC-104, SC-105, SC-106, SC-107, SC-108, SC-109, SC-110, SC-111, SC-112, SC-113, SC-114<br>KH-181, KH-182<br>ADR-014<br>Q-04, Q-17, Q-18<br>system-design: EV1<br>dòng PREMISE P-01, P-03, P-06, P-09, P-11, P-17, P-37, P-38, P-23 | [#286](https://github.com/hoctt-1111/sakura-market-lab5/issues/286) — Báo cáo và xuất sang hệ kế toán | Ràng buộc đặc thù 許可 / 承認 (hai tầng đặc quyền): 4 issue |
| `FG-12` `notification`<br>SC-120, SC-121, SC-122<br>ADR-013<br>system-design: EV2<br>dòng PREMISE P-01, P-03, P-06, P-12, P-14, P-39 | [#361](https://github.com/hoctt-1111/sakura-market-lab5/issues/361) — Thông báo và cảnh báo vận hành | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 4 issue |
| `FG-13` `audit-privacy`<br>SC-130, SC-131, SC-132, SC-133<br>ADR-003<br>dòng PREMISE P-01, P-03, P-04, P-06, P-12, P-40 | [#379](https://github.com/hoctt-1111/sakura-market-lab5/issues/379) — Vết kiểm toán và dữ liệu cá nhân | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 5 issue |
| `FG-14` `data-quality`<br>SC-140, SC-141, SC-142, SC-143, SC-150, SC-151<br>Q-19<br>dòng PREMISE P-01, P-03, P-06, P-12, P-19 | [#401](https://github.com/hoctt-1111/sakura-market-lab5/issues/401) — Chất lượng dữ liệu, chứng từ và ảnh | Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 8 issue |
| `E15`<br>API-220<br>ADR-003, ADR-008, ADR-009, ADR-012, ADR-015<br>NFR-OPS-01<br>dòng PREMISE P-02, P-04, P-19 | [#1](https://github.com/hoctt-1111/sakura-market-lab5/issues/1) — Nền tảng và hạ tầng | — |
| `E16`<br>ADR-016<br>Q-01<br>dòng PREMISE P-26, P-41 | [#431](https://github.com/hoctt-1111/sakura-market-lab5/issues/431) — Di trú dữ liệu | — |
| `E17`<br>AC1, AC2, AC3, AC4, AC5, AC6, AC7<br>system-design: A1, A10, A2, A3, A4, A5, A6, A7, A9, EV2<br>dòng PREMISE P-39, P-27 | [#445](https://github.com/hoctt-1111/sakura-market-lab5/issues/445) — Kiểm thử tích hợp và nghiệm thu | Ràng buộc đặc thù 相対取引 (giao dịch thỏa thuận): 2 issue<br>Ràng buộc đặc thù Người quyết, máy chỉ ghi nhận: 4 issue<br>Ràng buộc đặc thù 完納奨励金 (thưởng thanh toán đủ hạn): 2 issue<br>Ràng buộc đặc thù 許可 / 承認 (hai tầng đặc quyền): 4 issue |
| `E18`<br>SC-113<br>ADR-010, ADR-012<br>DR-RET-01, NFR-AVL-01, NFR-AVL-02, NFR-AVL-03, NFR-COMP-01, NFR-OPS-01, NFR-OPS-02, NFR-PERF-01, NFR-PERF-02, NFR-SEC-01, NFR-SEC-03, NFR-SEC-04, NFR-USE-01, SEC-IAM-02<br>Q-12<br>dòng PREMISE P-11, P-14, P-15, P-42 | [#460](https://github.com/hoctt-1111/sakura-market-lab5/issues/460) — Phi chức năng và bảo mật | — |
| `E19`<br>system-design: trien_khai.cach_biet_hong, trien_khai.d, trien_khai.hoan_nguyen, trien_khai.thu_tu | [#484](https://github.com/hoctt-1111/sakura-market-lab5/issues/484) — Phát hành production | — |
<!-- gen:readme-spec-epic:end -->

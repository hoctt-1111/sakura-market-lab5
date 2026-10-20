# Ước lượng — SWP đã review và giờ cho từng issue

<!-- gen:estimate-html:start -->
Báo cáo HTML của skill chấm SWP: [`reports/estimate-swp-github-hoctt-1111-projects-3-20261019-224426.html`](reports/estimate-swp-github-hoctt-1111-projects-3-20261019-224426.html)
<!-- gen:estimate-html:end -->

Skill chấm từng issue của chính Project theo Scope × Complexity, issue cha lấy tổng của issue con, rồi xuất báo cáo HTML ở trên. Trường point của Project chỉ mang SWP đã review; giờ nằm ở trường Estimated time.

## Issue mẫu skill chọn để kiểm

Mẫu gồm các issue skill tự chọn cộng một issue mỗi epic. Bản nộp này mới duyệt xong các mẫu skill chọn: mỗi mẫu đọc lại với thân issue và ô rubric của skill, chọn mức khó rồi điểm cụ thể, ghi lý do giữ ở cột cuối. Các mẫu theo epic đã có câu trả lời nháp nhưng chờ review đồng loạt, nên tạm giữ điểm skill và cột Lý do ghi rõ «chờ review đồng loạt»; số mẫu đã duyệt và còn chờ nằm ở dòng tổng dưới bảng. Điều chỉnh nào áp được cho các issue cùng tầng, cùng loại leaf và cùng cặp Scope × Complexity thì lan sang các issue đó theo luật, không sửa tay từng cái.

<!-- gen:estimate-mau:start -->
| Issue | Nguồn mẫu | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
| --- | --- | --- | --- | --- |
| [#3](https://github.com/hoctt-1111/sakura-market-lab5/issues/3) | skill chọn | 5 × 1 → 6 | 6 | Giữ 6 (vừa): khung dự án nhiều module, CI bốn cửa chặn gộp, công cụ migration chạy lại được — Scope 5, Complexity 1 vì đều là công cụ có sẵn với quyết định có giới hạn; người chấm thứ hai cho 8 (Complexity 2), không theo vì không thấy ràng buộc chéo khó trong thân issue. Mẫu chọn vì hai người chấm lệch nhau. |
| [#7](https://github.com/hoctt-1111/sakura-market-lab5/issues/7) | skill chọn | 5 × 3 → 10 | 10 | Giữ 10 (vừa): dựng hai môi trường từ tài khoản trống theo một bộ cấu hình, CSDL dự phòng như production, script che dữ liệu chạy lại ra cùng kết quả — Scope 5, Complexity 3; lô thử sáng 19/10 chấm 8, bản toàn bộ chấm 10, giữ 10 vì có cả yêu cầu khôi phục theo thời điểm. Mẫu chọn vì lệch xa trung vị. |
| [#8](https://github.com/hoctt-1111/sakura-market-lab5/issues/8) | một mẫu mỗi epic | 3 × 3 → 6 | 6 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#10](https://github.com/hoctt-1111/sakura-market-lab5/issues/10) | skill chọn | 1 × 1 → 1 | 1 | Giữ 1 (rất dễ): một route GET /api/health, một truy vấn nhẹ tới CSDL, hai nhánh 200/500, không kiểm phiên — đúng ô Scope 1 «một đường thay đổi cục bộ», Complexity thấp; hai người chấm cùng 1. Mẫu chọn vì nhỏ nhất. |
| [#436](https://github.com/hoctt-1111/sakura-market-lab5/issues/436) | một mẫu mỗi epic | 3 × 2 → 5 | 5 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#453](https://github.com/hoctt-1111/sakura-market-lab5/issues/453) | một mẫu mỗi epic | 3 × 2 → 5 | 5 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#471](https://github.com/hoctt-1111/sakura-market-lab5/issues/471) | skill chọn | 5 × 3 → 10 | 10 | Giữ 10 (vừa): đồng hồ khả dụng, sao lưu, bản dự phòng đồng bộ và diễn tập khôi phục đo RTO/RPO thật — Scope 5 «trọn một phân hệ», Complexity 3 «suy luận vận hành, khôi phục»; không lên mức khó vì không có dấu hiệu rủi ro cao cụ thể. Mẫu chọn vì lớn nhất. |
| [#476](https://github.com/hoctt-1111/sakura-market-lab5/issues/476) | một mẫu mỗi epic | 3 × 1 → 4 | 4 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#494](https://github.com/hoctt-1111/sakura-market-lab5/issues/494) | một mẫu mỗi epic | 3 × 2 → 5 | 5 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#69](https://github.com/hoctt-1111/sakura-market-lab5/issues/69) | một mẫu mỗi epic | 3 × 3 → 6 | 6 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#84](https://github.com/hoctt-1111/sakura-market-lab5/issues/84) | một mẫu mỗi epic | 2 × 2 → 3 | 3 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#104](https://github.com/hoctt-1111/sakura-market-lab5/issues/104) | một mẫu mỗi epic | 3 × 3 → 6 | 6 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#159](https://github.com/hoctt-1111/sakura-market-lab5/issues/159) | một mẫu mỗi epic | 3 × 2 → 5 | 5 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#186](https://github.com/hoctt-1111/sakura-market-lab5/issues/186) | một mẫu mỗi epic | 2 × 2 → 3 | 3 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#201](https://github.com/hoctt-1111/sakura-market-lab5/issues/201) | một mẫu mỗi epic | 2 × 0 → 2 | 2 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#231](https://github.com/hoctt-1111/sakura-market-lab5/issues/231) | một mẫu mỗi epic | 3 × 2 → 5 | 5 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#262](https://github.com/hoctt-1111/sakura-market-lab5/issues/262) | một mẫu mỗi epic | 3 × 2 → 5 | 5 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#22](https://github.com/hoctt-1111/sakura-market-lab5/issues/22) | một mẫu mỗi epic | 5 × 2 → 8 | 8 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#276](https://github.com/hoctt-1111/sakura-market-lab5/issues/276) | một mẫu mỗi epic | 2 × 3 → 4 | 4 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#333](https://github.com/hoctt-1111/sakura-market-lab5/issues/333) | skill chọn | 2 × 2 → 3 | 3 | Giữ 3 (dễ): spec và một truy vấn đọc so giờ ghi điều chỉnh với giờ khoá ngày — Scope 2 «vài thay đổi liên quan trong một lớp», Complexity 2 vì có nhánh ngày chưa khoá và nguồn dòng đảo; người chấm thứ hai cũng 3. Mẫu chọn vì trung vị. |
| [#357](https://github.com/hoctt-1111/sakura-market-lab5/issues/357) | một mẫu mỗi epic | 5 × 3 → 10 | 10 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#372](https://github.com/hoctt-1111/sakura-market-lab5/issues/372) | một mẫu mỗi epic | 5 × 2 → 8 | 8 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#391](https://github.com/hoctt-1111/sakura-market-lab5/issues/391) | một mẫu mỗi epic | 1 × 2 → 2 | 2 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |
| [#420](https://github.com/hoctt-1111/sakura-market-lab5/issues/420) | một mẫu mỗi epic | 3 × 1 → 4 | 4 | Chờ review đồng loạt (bản nháp 19/10): tạm giữ điểm skill. |

24 mẫu: giữ 24 · sửa 0 · đã duyệt 5 · chờ review đồng loạt 19. Điều chỉnh lan theo luật sang 0 issue cùng tầng; 0 INV chấm theo luật cố định vì skill không chấm điều tra. Tổng 371 mục chấm trực tiếp.
<!-- gen:estimate-mau:end -->

## Cách quy ra giờ

Chọn quy ước đổi SWP ra giờ thay vì ước trực tiếp từng issue. Lý do: backlog có vài trăm mục chấm, ước tay từng issue vừa lâu vừa khó giữ nhất quán, còn SWP đã qua review nên là thước đo chung. Mỗi nhóm leaf có một hệ số k riêng, lấy từ dữ liệu LAB-1 chứ không tự đặt: nhóm dev hồi quy qua gốc trên các màn của LAB-1, nhóm test lấy theo tỷ lệ vai QA so với Dev của LAB-1, điều tra (INV) có giờ cố định theo người trả lời. Không ép tổng giờ bằng LAB-1, nên bảng so sánh ở cuối có chênh thật để giải thích. Độ tin cậy cần nói rõ: SWP giải thích rất ít độ lệch giờ giữa các màn của LAB-1 (R² so trung bình ở bảng dưới gần bằng không), nên k chỉ đúng như một mức giờ trung bình cho mỗi SWP trên cả tập. Tổng giờ theo epic và toàn backlog dùng được để lập kế hoạch; giờ của từng issue là ước thô, cần chỉnh khi đội ước lại lúc vào sprint.

Áp dụng như nhau cho mọi issue: giờ = SWP chốt × k của nhóm, làm tròn từng issue; issue cha lấy tổng con. Chỉ issue mang nhãn ràng buộc đặc thù được chỉnh tay, có trần và phải ghi lý do.

<!-- gen:estimate-k:start -->
| Nhóm | Cách | k (giờ/SWP) | R² | Nguồn | Số issue áp |
| --- | --- | --- | --- | --- | --- |
| dev | hồi quy qua gốc trên 72 màn LAB-1: giờ_i = man_day_i × 0.80 × 8 (chi_tiet_man); SWP_i = ΣSWP leaf nhóm dev của story SC-i; k = Σ(giờ_i·SWP_i) / Σ(SWP_i²) — Σ(giờ·SWP) = 18856.77, Σ(SWP²) = 5268.00, 72 màn | 3,579 | 0,05 | effort-computed.yaml:45<br>effort-rates.yaml:20<br>quy-uoc-gio.yaml:6<br>swp-final.json | 212 |
| test | giờ test = giờ dev (k_dev × ΣSWP nhóm dev toàn backlog) × QA/Dev của LAB-1 (340.2 / 643.5); chia ΣSWP leaf nhóm test — giờ dev 2931.60 × 340.2/643.5 = 1549.86; ΣSWP test = 438 | 3,538 | — | effort-computed.yaml:12<br>effort-computed.yaml:9<br>swp-final.json | 120 |

Giờ từng issue = SWP chốt × k của nhóm, làm tròn 0,5 giờ; issue cha = tổng con. Tổng sau làm tròn: dev 2.911,5 giờ · test 1.533 giờ · inv 109 giờ. Chỉnh tay theo nhãn `constraint:*` (tối đa 20%): không issue nào.
<!-- gen:estimate-k:end -->

## Tổng theo epic

Số đếm và tổng sinh từ registry ước lượng, khớp với trường point và Estimated time trên Project (gate field kiểm «cha = tổng con»).

<!-- gen:estimate-epic:start -->
| Epic | Số issue | Tổng SWP | Tổng giờ | Ghi chú |
| --- | --- | --- | --- | --- |
| [#1](https://github.com/hoctt-1111/sakura-market-lab5/issues/1) Nền tảng và hạ tầng | 10 | 29 | 104 | — |
| [#431](https://github.com/hoctt-1111/sakura-market-lab5/issues/431) Di trú dữ liệu | 13 | 50 | 171 | — |
| [#445](https://github.com/hoctt-1111/sakura-market-lab5/issues/445) Kiểm thử tích hợp và nghiệm thu | 24 | 49 | 171,5 | `constraint:incentive` 28 giờ · `constraint:two-tier` 35 giờ · `constraint:aitai` 14 giờ · `constraint:hitl` 73,5 giờ · `constraint:jst` 28 giờ |
| [#460](https://github.com/hoctt-1111/sakura-market-lab5/issues/460) Phi chức năng và bảo mật | 23 | 76 | 261,5 | — |
| [#484](https://github.com/hoctt-1111/sakura-market-lab5/issues/484) Phát hành production | 12 | 45 | 159,5 | — |
| [#35](https://github.com/hoctt-1111/sakura-market-lab5/issues/35) Tài khoản và quyền nội bộ | 35 | 99 | 341 | `constraint:two-tier` 3 giờ |
| [#71](https://github.com/hoctt-1111/sakura-market-lab5/issues/71) Tư cách người tham gia 許可・承認 | 24 | 67 | 221 | `constraint:two-tier` 218 giờ |
| [#96](https://github.com/hoctt-1111/sakura-market-lab5/issues/96) Tiếp nhận lô và thẩm định 目利き | 32 | 84 | 295 | `constraint:hitl` 46 giờ · `constraint:jst` 67,5 giờ |
| [#128](https://github.com/hoctt-1111/sakura-market-lab5/issues/128) Giao dịch thỏa thuận 相対取引 | 44 | 99 | 324,5 | `constraint:two-tier` 123,5 giờ · `constraint:aitai` 324,5 giờ · `constraint:jst` 124 giờ |
| [#172](https://github.com/hoctt-1111/sakura-market-lab5/issues/172) Kết quả đấu giá せり | 14 | 42 | 149 | `constraint:two-tier` 67,5 giờ · `constraint:aitai` 28,5 giờ · `constraint:hitl` 117,5 giờ · `constraint:jst` 50 giờ |
| [#189](https://github.com/hoctt-1111/sakura-market-lab5/issues/189) Sửa sau xác nhận và bút toán đảo 赤伝 | 22 | 56 | 180 | `constraint:two-tier` 2 giờ |
| [#210](https://github.com/hoctt-1111/sakura-market-lab5/issues/210) Giao hàng và ngoại lệ giao hàng | 24 | 62 | 212,5 | `constraint:hitl` 51 giờ · `constraint:jst` 110 giờ |
| [#235](https://github.com/hoctt-1111/sakura-market-lab5/issues/235) Đối soát ngày và khoá ngày nghiệp vụ | 29 | 74 | 250,5 | `constraint:aitai` 49,5 giờ · `constraint:hitl` 86,5 giờ · `constraint:jst` 166 giờ |
| [#12](https://github.com/hoctt-1111/sakura-market-lab5/issues/12) Thưởng thanh toán đủ hạn 完納奨励金 | 24 | 69 | 225 | `constraint:incentive` 225 giờ · `constraint:hitl` 155 giờ · `constraint:jst` 152 giờ |
| [#264](https://github.com/hoctt-1111/sakura-market-lab5/issues/264) Quy chế và biểu suất theo phiên bản | 22 | 58 | 197 | `constraint:incentive` 46 giờ · `constraint:hitl` 45,5 giờ · `constraint:jst` 46 giờ |
| [#286](https://github.com/hoctt-1111/sakura-market-lab5/issues/286) Báo cáo và xuất sang hệ kế toán | 75 | 176 | 618,5 | `constraint:two-tier` 31,5 giờ · `constraint:jst` 160,5 giờ |
| [#361](https://github.com/hoctt-1111/sakura-market-lab5/issues/361) Thông báo và cảnh báo vận hành | 17 | 44 | 154,5 | `constraint:hitl` 39 giờ · `constraint:jst` 56,5 giờ |
| [#379](https://github.com/hoctt-1111/sakura-market-lab5/issues/379) Vết kiểm toán và dữ liệu cá nhân | 21 | 56 | 198 | `constraint:hitl` 46 giờ · `constraint:jst` 50 giờ |
| [#401](https://github.com/hoctt-1111/sakura-market-lab5/issues/401) Chất lượng dữ liệu, chứng từ và ảnh | 29 | 90 | 319,5 | `constraint:hitl` 103,5 giờ · `constraint:jst` 46,5 giờ |
| Tổng | 494 | 1.325 | 4.553,5 | số issue không tính chính epic |

Một issue có thể mang nhiều nhãn `constraint:*`, nên giờ theo nhãn ở cột Ghi chú cộng chéo, không cộng thành tổng epic.
<!-- gen:estimate-epic:end -->

## So với estimate LAB-1

So theo phần, quy man-day của LAB-1 ra giờ. Chỗ chênh do thay đổi ở PREMISE.md thì trỏ đúng dòng P-xx.

<!-- gen:estimate-lab1:start -->
| Phần | LAB-1 (giờ) | LAB-5 (giờ) | Chênh | Vì sao |
| --- | --- | --- | --- | --- |
| Màn hình (dev) | 2.199,7 | 2.069 | -130,7 (-6%) | Sai số của cách tính, không phải phát hiện: k_dev hồi quy qua gốc trên chính 72 màn LAB-1 (bình phương nhỏ nhất qua gốc không ép tổng bằng nhau) cộng làm tròn 0,5 giờ trên 167 leaf. R² so trung bình chỉ 0,05 nên từng màn lệch nhiều (SC-106: LAB-1 44,8 giờ, LAB-5 17,9 giờ); tổng dùng được, giờ từng màn là ước thô |
| Dev ngoài màn | 2.948,3 | 609 | -2.339,3 (-79%) | LAB-1 gán 368,5 man-day Dev cho hạng mục ngoài màn (EF-05…EF-11 nền tảng quy tắc, chỉ-thêm, vết kiểm toán, thông báo, xuất kế toán, APPI; EF-17…EF-19 di trú). LAB-5 dòng này gồm E15–E19 222,5 · DATA 111 · KH 97 · API 96 · TECH 82,5 giờ. Một phần nền tảng nằm trong story màn (SC-091 quy tắc, SC-121 thông báo) nhưng dòng Màn hình chỉ lệch 6%, nên phần lớn chênh là LAB-5 ước thấp hơn cho việc ngoài màn — mở để xem lại khi review, không có dữ liệu cho thấy đây là gom nhóm có chủ ý |
| QA | 2.721,6 | 1.533 | -1.188,6 (-44%) | Hệ quả của dòng dev, không phải phát hiện riêng: giờ test = giờ dev LAB-5 × tỷ lệ QA/Dev của LAB-1 (340,2/643,5 = 0,529). Giờ dev LAB-5 2.931,6 thấp hơn Dev LAB-1 5.148 giờ 43%; thêm làm tròn từng issue (1.549,9 → 1.533) thành -44% |
| Infra | 651,2 | 233,5 | -417,7 (-64%) | LAB-1 Infra 81,4 man-day gồm kiến trúc và dựng 3 môi trường (EF-04, 40 md), lưu trữ hai tầng và khôi phục (EF-12, 18 md) và các mục Infra khác. LAB-5 chỉ có 10 leaf INFRA, cùng nằm trong E15–E19, giờ = SWP × k_dev vì không có k riêng cho Infra, nên dòng này đi theo mức thấp của k_dev |
| PM · BrSE · Tech Lead · Designer | 4.437,6 | 0 | -4.437,6 (-100%) | LAB-5 không ước giờ cho quản lý dự án, cầu nối khách, thiết kế cơ bản và UX (EF-01…EF-03, EF-33, EF-20): các vai này có tên làm Owner (INV giao BrSE) nhưng việc của họ không break thành leaf có giờ (task-breakdown.md, nguyên tắc chia task). Dòng này là 34% LAB-1, nên tổng LAB-5 không so thẳng với tổng LAB-1 |
| E15–E19 (xuyên suốt) | không có | 867,5 | — | LAB-1 không tách dòng này (nằm trong Dev/Infra phi màn); LAB-5 tách 5 epic nền tảng, di trú, nghiệm thu, NFR, phát hành để thấy riêng phần không gắn màn nào |
| INV (điều tra) | không có | 109 | — | LAB-1 không có: 39 issue làm rõ (câu hỏi khách qua BrSE, quyết định Tech Lead) phát sinh khi break LAB-4; giờ cố định theo người trả lời (3 giờ khách, 2 giờ Tech Lead) trong quy-uoc-gio.yaml |
| 完納奨励金 (FG-09) | 124 | 225 | 101 (81%) | Ba màn SC-080…SC-082 ra 99 giờ dev + 38,5 giờ test = 137,5 giờ, gần LAB-1 99,2 giờ (Dev 0,8) + 24,8 giờ (QA 0,2) = 124 giờ. Phần LAB-1 không có dòng riêng: dịch vụ tính TECH-304 và bảng DATA-FG09 (dev 46,5 · test 28 giờ) và 5 INV làm rõ kỳ tính, chênh lệch, ghi đè (13 giờ) |

LAB-1 đổi man-day ra giờ theo 8 giờ một man-day; LAB-5 cộng giờ chốt của issue chấm trực tiếp. Các dòng lọc theo epic hoặc theo nhóm chồng nhau (một leaf của E15–E19 hay FG-09 cũng nằm trong dòng theo vai), nên cộng cột không ra tổng. Tổng LAB-1 12.958,4 giờ · tổng LAB-5 4.553,5 giờ (35% LAB-1).
<!-- gen:estimate-lab1:end -->

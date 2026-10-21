# Báo cáo tiến độ — sprint giả lập trên GitHub Project

<!-- gen:progress-dau:start -->
Iteration trên Project: «Sprint 1» (field Iteration «Sprint»), 09/11/2026 – 22/11/2026. Báo cáo là ảnh chụp ngày làm việc 9/10 của Sprint 1 (19/11/2026), số liệu giả lập: Status, Spent time, Done Date do kịch bản giả lập ghi, không phải kết quả một sprint chạy thật.
<!-- gen:progress-dau:end -->

Đây là báo cáo của một Sprint giả lập: issue được xếp vào Iteration thật trên Project, còn Status, Spent time và Done Date do kịch bản giả lập ghi lên như sau một Sprint chạy thật. Giả lập không đóng issue trên GitHub: issue xong chỉ mang Status Closed trên board và ngày ở trường Done Date, còn trạng thái của issue trên GitHub vẫn là mở. Các issue thật sự đóng trên GitHub là issue thay thế, không thuộc Sprint và không tính trong các bảng dưới.

## Tóm tắt

<!-- gen:pr-tom-tat:start -->
- Ảnh chụp ngày 19/11/2026, ngày làm việc 9/10 của Sprint 1 (09/11/2026 – 22/11/2026). Số liệu giả lập, không phải kết quả một sprint chạy thật.
- Hoàn thành 98/135 SWP (73%) của Sprint 1.
- Nguyên nhân trượt chính: chờ câu trả lời cho các câu hỏi gửi quý khách — 15 việc, 27 SWP trên 37 SWP chưa xong vì trượt; chờ quyết định kỹ thuật nội bộ (Tech Lead) — 3 việc, 10 SWP. Việc nội bộ chính: [#513](https://github.com/hoctt-1111/sakura-market-lab5/issues/513) — Tech Lead chưa chốt nơi giữ dòng đảo và khung nhìn chuẩn: hai phương án đụng nhau ở bảng nào giữ dòng đảo, cần rà cùng BE-2 trước khi chốt (chi tiết ở mục Burndown).
- Cần quý khách trả lời 30 câu; hạn gần nhất 09/11/2026 (hạn bên làm đề xuất trước buổi khởi động dự án), 9 câu đã quá hạn ở ngày chụp; thêm 2 câu có hạn gốc trước ngày bắt đầu dự án 09/11/2026, vẫn chưa có trả lời ở ngày chụp (bảng ở cuối báo cáo).
- Dự báo theo tốc độ thực tế của Sprint 1 (cả đội 98 SWP/sprint, backlog còn 1.282 SWP): vai nghẽn BE-2 còn 209 SWP, làm 12 SWP mỗi sprint nên cần thêm 18 sprint, tổng 19 sprint so với kế hoạch 19 sprint (một sprint dữ liệu — dự báo thô, con số sẽ đổi khi có thêm sprint thật). Số sprint ở cuối mục Rủi ro trễ tính theo năng lực giờ theo kế hoạch của từng vai, không theo tốc độ này, nên hai số khác nhau.
- Vai chưa có việc xong trong Sprint 1 nên chưa dự báo riêng: BrSE.

| Vai | SWP toàn backlog | Xong Sprint 1 | Còn lại | Sprint cần thêm |
| --- | --- | --- | --- | --- |
| BE-1 | 331 | 25 | 306 | 13 |
| BE-2 | 221 | 12 | 209 | 18 |
| BrSE | 57 | 0 | 57 | chưa đo được |
| FE-1 | 133 | 12 | 121 | 11 |
| FE-2 | 104 | 13 | 91 | 7 |
| Infra | 68 | 6 | 62 | 11 |
| PM | 2 | 2 | 0 | 0 |
| QA | 464 | 28 | 436 | 16 |
<!-- gen:pr-tom-tat:end -->

<!-- gen:pr-tom-tat-ja:start -->
**進捗サマリー**（2026年11月19日時点・シミュレーション値）

- Sprint 1 の完了率は73%（135 SWP 中 98 SWP）でございます。
- 主な遅延要因は、お客様へのご確認事項のご回答待ち（15件、27 SWP）でございます。このほか、社内の技術判断（テックリード）の確定待ち（3件、10 SWP）がございます。社内の案件（主に[#513](https://github.com/hoctt-1111/sakura-market-lab5/issues/513)）につきましては、弊社にて早急に対応いたします。詳細は本報告書のバーンダウン欄に記載しております。
- ご回答をお願いしたい事項は30件で、最も早い期限は2026年11月9日（キックオフ前に弊社よりご提案した期限）でございます（うち9件は期限を経過しております）。お手数をおかけいたしますが、お早めにご回答いただけますと幸いです。このほか、キックオフ（2026年11月9日）以前を当初の期限としておりました事項のうち、本報告時点でご回答をいただいていないものが2件ございます。
- Sprint 1 の実績速度に基づきますと、最も時間を要する担当（BE-2）は残り209 SWP、1スプリントあたり12 SWP のため、完了までにあと約18スプリント（計画19スプリント）を要する見込みでございます。
- ※1スプリント分のデータに基づく概算のため、今後のスプリント実績により見直してまいります。
<!-- gen:pr-tom-tat-ja:end -->

## Trạng thái

Đếm từ chính Project ở ảnh chụp cuối kỳ báo cáo.

<!-- gen:progress-trang-thai:start -->
| Trạng thái | Số issue | Tổng SWP | Trong Sprint | Ghi chú |
| --- | --- | --- | --- | --- |
| New | 437 | 1.245 | 0 | việc lá/INV 325 · story/epic 112 |
| In Progress | 31 | 0 | 0 | story/epic 31 |
| Pending | 18 | 37 | 18 | việc lá/INV 18 |
| Closed | 31 | 98 | 31 | việc lá/INV 31 |

Tổng SWP chỉ cộng việc lá và INV (story, epic là tổng con nên không cộng lại).

Bảng không tính 4 issue đã đóng vì được thay thế: [#176](https://github.com/hoctt-1111/sakura-market-lab5/issues/176), [#187](https://github.com/hoctt-1111/sakura-market-lab5/issues/187), [#188](https://github.com/hoctt-1111/sakura-market-lab5/issues/188), [#230](https://github.com/hoctt-1111/sakura-market-lab5/issues/230).
<!-- gen:progress-trang-thai:end -->

## Burndown hoặc tương đương

Ảnh và bảng burndown theo SWP: đường kế hoạch giảm đều mỗi ngày làm việc, đường thực tế giảm theo Done Date của việc lá và điều tra trong Sprint, không cộng issue cha. Ảnh vẽ từ đúng các số trong bảng.

<!-- gen:progress-burndown:start -->
![Burndown Sprint 1: SWP còn lại theo ngày làm việc, kế hoạch và thực tế](reports/burndown-sprint-1.svg)

| Ngày làm việc | Kế hoạch còn lại | Thực tế còn lại | Xong trong ngày | Ghi chú |
| --- | --- | --- | --- | --- |
| 0 (đầu sprint) | 135 | 135 | — | — |
| 1 (09/11/2026) | 121,5 | 121 | 14 | — |
| 2 (10/11/2026) | 108 | 116 | 5 | — |
| 3 (11/11/2026) | 94,5 | 99 | 17 | — |
| 4 (12/11/2026) | 81 | 95 | 4 | — |
| 5 (13/11/2026) | 67,5 | 65 | 30 | — |
| 6 (16/11/2026) | 54 | 56 | 9 | — |
| 7 (17/11/2026) | 40,5 | 42 | 14 | — |
| 8 (18/11/2026) | 27 | 37 | 5 | — |
| 9 (19/11/2026) | 13,5 | 37 | 0 | ảnh chụp |
| 10 (20/11/2026) | 0 | — | — | chưa tới |

Scope = 135 SWP của 49 việc lá và INV trong Sprint; đơn vị SWP; giả lập.
<!-- gen:progress-burndown:end -->

Thực tế lệch kế hoạch ở các issue dưới đây; dòng cuối gộp SWP trượt theo nguyên nhân. Việc phụ thuộc phải chờ câu trả lời hoặc quyết định, trong khi đội vẫn làm được phần không bị chặn.

<!-- gen:progress-truot:start -->
| Issue | Status ở ảnh chụp | Lý do lệch kế hoạch |
| --- | --- | --- |
| [#143](https://github.com/hoctt-1111/sakura-market-lab5/issues/143), [#78](https://github.com/hoctt-1111/sakura-market-lab5/issues/78), [#144](https://github.com/hoctt-1111/sakura-market-lab5/issues/144), [#20](https://github.com/hoctt-1111/sakura-market-lab5/issues/20), [#270](https://github.com/hoctt-1111/sakura-market-lab5/issues/270), [#306](https://github.com/hoctt-1111/sakura-market-lab5/issues/306), [#366](https://github.com/hoctt-1111/sakura-market-lab5/issues/366), [#385](https://github.com/hoctt-1111/sakura-market-lab5/issues/385), [#435](https://github.com/hoctt-1111/sakura-market-lab5/issues/435), [#468](https://github.com/hoctt-1111/sakura-market-lab5/issues/468), [#77](https://github.com/hoctt-1111/sakura-market-lab5/issues/77), [#140](https://github.com/hoctt-1111/sakura-market-lab5/issues/140), [#141](https://github.com/hoctt-1111/sakura-market-lab5/issues/141), [#142](https://github.com/hoctt-1111/sakura-market-lab5/issues/142), [#177](https://github.com/hoctt-1111/sakura-market-lab5/issues/177) (15 việc) | Pending | khách chưa trả lời, chưa đóng được trong giả lập |
| [#513](https://github.com/hoctt-1111/sakura-market-lab5/issues/513) | Pending | Tech Lead chưa chốt nơi giữ dòng đảo và khung nhìn chuẩn: hai phương án đụng nhau ở bảng nào giữ dòng đảo, cần rà cùng BE-2 trước khi chốt |
| [#19](https://github.com/hoctt-1111/sakura-market-lab5/issues/19) | Pending | Câu hỏi P-22 (lưu kết quả chờ của bước tính thưởng thất bại thì trả lỗi hay bỏ qua) quá hạn từ 08/10, Tech Lead chưa trả lời trong sprint |
| [#8](https://github.com/hoctt-1111/sakura-market-lab5/issues/8) | Pending | Thư viện ghi chỉ-thêm chờ INV-FG06-DONG-DAO: chưa biết bảng nào giữ dòng đảo thì chưa chốt được hàm ghi đảo; BE-1 làm xong hàm ghi gốc và ghi sửa, phần đảo để lại |

Xong 98/135 SWP (73%) ở ảnh chụp.

SWP trượt gộp theo nguyên nhân: chờ câu trả lời cho các câu hỏi gửi quý khách — 15 việc, 27 SWP · chờ quyết định kỹ thuật nội bộ (Tech Lead) — 3 việc, 10 SWP.
<!-- gen:progress-truot:end -->

## Spent so với Estimated

Giờ thực tế (Spent time) so với giờ ước lượng (Estimated time) của các issue đã xong, gộp theo nhóm việc. Hệ số k là số giờ cho một SWP: so k thực tế với k dùng khi ước lượng cho biết cách quy giờ còn đúng hay cần chỉnh trước sprint sau.

<!-- gen:pr-spent:start -->
| Nhóm | Số issue xong | Estimated (giờ) | Spent (giờ) | Chênh | k quy ước (giờ/SWP) | k thực tế (giờ/SWP) |
| --- | --- | --- | --- | --- | --- | --- |
| dev | 18 | 200,5 | 212 | +6% | 3,37 | 3,53 |
| inv | 6 | 13 | 15 | +15% | — | 1,5 |
| test | 7 | 89,5 | 112,5 | +26% | 3,24 | 4,02 |
| Tổng | 31 | 303 | 339,5 | +12% | — | 3,46 |

Chỉ tính việc lá và điều tra đã xong ở ảnh chụp, có Spent time (giả lập). k thực tế = Spent chia SWP của chính các issue đó; lệch xa k quy ước thì xem lại hệ số quy giờ trước khi xếp sprint sau.

<details><summary>Từng issue (31)</summary>

| Issue | Estimated (giờ) | Spent (giờ) | Chênh |
| --- | --- | --- | --- |
| [#243](https://github.com/hoctt-1111/sakura-market-lab5/issues/243) | 2 | 2 | 0% |
| [#510](https://github.com/hoctt-1111/sakura-market-lab5/issues/510) | 2 | 2,5 | +25% |
| [#514](https://github.com/hoctt-1111/sakura-market-lab5/issues/514) | 2 | 2,5 | +25% |
| [#515](https://github.com/hoctt-1111/sakura-market-lab5/issues/515) | 2 | 2 | 0% |
| [#498](https://github.com/hoctt-1111/sakura-market-lab5/issues/498) | 2 | 2,5 | +25% |
| [#519](https://github.com/hoctt-1111/sakura-market-lab5/issues/519) | 3 | 3,5 | +17% |
| [#3](https://github.com/hoctt-1111/sakura-market-lab5/issues/3) | 20 | 19 | −5% |
| [#10](https://github.com/hoctt-1111/sakura-market-lab5/issues/10) | 3,5 | 5 | +43% |
| [#11](https://github.com/hoctt-1111/sakura-market-lab5/issues/11) | 3 | 3 | 0% |
| [#46](https://github.com/hoctt-1111/sakura-market-lab5/issues/46) | 10 | 10 | 0% |
| [#47](https://github.com/hoctt-1111/sakura-market-lab5/issues/47) | 20 | 16,5 | −18% |
| [#48](https://github.com/hoctt-1111/sakura-market-lab5/issues/48) | 3,5 | 4,5 | +29% |
| [#49](https://github.com/hoctt-1111/sakura-market-lab5/issues/49) | 16 | 19,5 | +22% |
| [#50](https://github.com/hoctt-1111/sakura-market-lab5/issues/50) | 10 | 14 | +40% |
| [#51](https://github.com/hoctt-1111/sakura-market-lab5/issues/51) | 10 | 12,5 | +25% |
| [#52](https://github.com/hoctt-1111/sakura-market-lab5/issues/52) | 9,5 | 11,5 | +21% |
| [#53](https://github.com/hoctt-1111/sakura-market-lab5/issues/53) | 10 | 11,5 | +15% |
| [#54](https://github.com/hoctt-1111/sakura-market-lab5/issues/54) | 20 | 18,5 | −8% |
| [#56](https://github.com/hoctt-1111/sakura-market-lab5/issues/56) | 16 | 20 | +25% |
| [#57](https://github.com/hoctt-1111/sakura-market-lab5/issues/57) | 10 | 11,5 | +15% |
| [#59](https://github.com/hoctt-1111/sakura-market-lab5/issues/59) | 13 | 17,5 | +35% |
| [#63](https://github.com/hoctt-1111/sakura-market-lab5/issues/63) | 16 | 21 | +31% |
| [#66](https://github.com/hoctt-1111/sakura-market-lab5/issues/66) | 16 | 20 | +25% |
| [#149](https://github.com/hoctt-1111/sakura-market-lab5/issues/149) | 13,5 | 18 | +33% |
| [#150](https://github.com/hoctt-1111/sakura-market-lab5/issues/150) | 10 | 13,5 | +35% |
| [#152](https://github.com/hoctt-1111/sakura-market-lab5/issues/152) | 10 | 8,5 | −15% |
| [#153](https://github.com/hoctt-1111/sakura-market-lab5/issues/153) | 10 | 10 | 0% |
| [#162](https://github.com/hoctt-1111/sakura-market-lab5/issues/162) | 10 | 11 | +10% |
| [#166](https://github.com/hoctt-1111/sakura-market-lab5/issues/166) | 10 | 9 | −10% |
| [#248](https://github.com/hoctt-1111/sakura-market-lab5/issues/248) | 10 | 10 | 0% |
| [#252](https://github.com/hoctt-1111/sakura-market-lab5/issues/252) | 10 | 9 | −10% |

</details>
<!-- gen:pr-spent:end -->

## Rủi ro trễ

Các rủi ro có thể làm trễ mốc, mỗi dòng có hành động, người làm và thời điểm. Số sprint cần cho toàn backlog ở cuối bảng tính theo năng lực giờ của từng vai, khác với dự báo theo tốc độ thực tế ở phần tóm tắt.

<!-- gen:progress-rui-ro:start -->
| Rủi ro | Issue | Ảnh hưởng tới mốc nào | Hành động | Ai làm, khi nào |
| --- | --- | --- | --- | --- |
| Đội theo FTE bình quân tháng 1–9 của LAB-1 vừa đủ cho backlog nhưng biên mỏng: QA (2 người) và BE-2 (1 người) là hai vai cần nhiều sprint nhất, sát số sprint của kế hoạch. Số sprint cần, giờ backlog và giờ cần mỗi sprint của từng vai ở dòng ngay dưới bảng, tính lại mỗi lần dựng báo cáo | [#445](https://github.com/hoctt-1111/sakura-market-lab5/issues/445) | Đưa vào vận hành ở tháng 9 của LAB-1 (07/2027); 19 sprint từ 09/11/2026, Sprint 19 kết thúc 01/08/2027 | Đo giờ QA, BE-2 làm được mỗi sprint từ Sprint 1; hết Sprint 3 mà giờ làm được của một trong hai vai thấp hơn giờ cần mỗi sprint ở dòng dưới bảng thì thêm QA thứ ba hoặc chuyển việc lá FG chẵn của BE-2 sang BE-1 (BE-1 cần ít sprint hơn hẳn); khách không duyệt thêm người thì giãn ngày đưa vào vận hành theo số sprint của vai nghẽn | PM đề xuất, khách quyết, 2026-12-20 |
| INV-Q-23 (mức chặn) chưa có trả lời: ranh giới kỳ tính 完納奨励金 và đường nhập 入金 chặn toàn bộ FG-09 | [#497](https://github.com/hoctt-1111/sakura-market-lab5/issues/497) | FG-09 vào Sprint 3 (bắt đầu 07/12/2026) | Hạn gốc 31/10/2026 đã qua; BrSE xin quý khách trả lời ở buổi họp tuần gần nhất. Chưa có trả lời trước khi Sprint 3 bắt đầu thì FG-09 dời sang Sprint 4 và làm theo giả định GD-17 đã ghi ở PREMISE | BrSE, 2026-11-20 |
| Thư viện ghi chỉ-thêm đứng ở Pending vì Tech Lead chưa chốt nơi giữ dòng đảo; mọi module ghi giao dịch phụ thuộc thư viện này | [#8](https://github.com/hoctt-1111/sakura-market-lab5/issues/8), [#513](https://github.com/hoctt-1111/sakura-market-lab5/issues/513) | Module ghi giao dịch 相対 và せり ở Sprint 2 | Tech Lead chốt phương án trong buổi rà thiết kế, BE-1 làm tiếp ngay ngày sau | Tech Lead, 2026-11-20 |
| Câu hỏi gửi khách qua BrSE (INV loại khách) chưa có trả lời ở ảnh chụp ngày thứ chín, kéo tỷ lệ xong Sprint 1 xuống dưới mục tiêu 80% của Sprint | [#435](https://github.com/hoctt-1111/sakura-market-lab5/issues/435), [#270](https://github.com/hoctt-1111/sakura-market-lab5/issues/270), [#306](https://github.com/hoctt-1111/sakura-market-lab5/issues/306), [#140](https://github.com/hoctt-1111/sakura-market-lab5/issues/140) | Đầu Sprint 2 (23/11/2026) | Gom các câu còn mở thành một danh sách hỏi gửi khách một lần kèm giả định đang dùng, xin quý khách trả lời trước 23/11/2026 (đầu Sprint 2); câu chưa có trả lời tới ngày đó thì Sprint 2 làm theo giả định đang dùng và ghi rõ vào issue điều tra | BrSE, 2026-11-20 |
| P-22 quá hạn từ 08/10: Tech Lead chưa chốt xử lý khi lưu kết quả chờ của bước tính thưởng thất bại, chặn nhánh lỗi của TECH-304 | [#19](https://github.com/hoctt-1111/sakura-market-lab5/issues/19), [#31](https://github.com/hoctt-1111/sakura-market-lab5/issues/31) | FG-09 vào Sprint 3 (07/12/2026) | Chốt theo giả định P-22 (trả SAVE_FAILED) trừ khi Tech Lead phản đối; ghi quyết định vào issue điều tra | Tech Lead, 2026-11-23 |
| Ca nghiệm thu 02:31 JST chưa chạy được: môi trường thử chưa đặt máy chạy kiểm thử ở múi giờ UTC+7 | [#505](https://github.com/hoctt-1111/sakura-market-lab5/issues/505) | Nghiệm thu E17 trước phát hành | Infra thêm cấu hình múi giờ cho máy chạy kiểm thử trên môi trường thử; QA chạy lại ca | Infra, QA, 2026-11-23 |

Với năng lực giờ theo kế hoạch (giờ mỗi người mỗi sprint nhân số người của vai, xếp tới 85%), toàn backlog cần 16 sprint trên 19 sprint kế hoạch (vai nghẽn: BE-2, QA); số này khác dự báo ở phần tóm tắt, vốn tính theo tốc độ thực tế của vai nghẽn trong Sprint 1. Số sprint cần theo vai: BE-2 16 sprint (742,5 giờ, cần 39,1 giờ mỗi sprint); QA 16 sprint (1.484,5 giờ, cần 78,1 giờ mỗi sprint); BE-1 12 sprint; FE-1 10 sprint; FE-2 8 sprint; Infra 5 sprint; BrSE 3 sprint; PM 1 sprint.
<!-- gen:progress-rui-ro:end -->

## Câu cần quý khách trả lời

Các điều tra đang chờ quý khách, xếp theo hạn. Câu nào chưa có trả lời thì việc ở cột «Việc đang chờ câu trả lời» chưa chốt được; trong lúc chờ, đội làm trước phần không bị chặn. Thuật ngữ Nhật trong bảng: 日次照合表 là bảng đối soát ngày (đối chiếu giao dịch, giao hàng và tiền về của một ngày nghiệp vụ).

<!-- gen:pr-hoi-khach:start -->
| Issue | Câu cần quý khách trả lời | Hạn | Ở ngày chụp | Việc đang chờ câu trả lời | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| [#141](https://github.com/hoctt-1111/sakura-market-lab5/issues/141) | 買出人 có luôn trả ngay khi mua trực tiếp không | 09/11/2026 | quá hạn | — | Pending |
| [#77](https://github.com/hoctt-1111/sakura-market-lab5/issues/77) | Ngưỡng cảnh báo 失効間近 và cách cấu hình | 09/11/2026 | quá hạn | [#76](https://github.com/hoctt-1111/sakura-market-lab5/issues/76) | Pending |
| [#18](https://github.com/hoctt-1111/sakura-market-lab5/issues/18) | Cách tính 適格金額 và bảng 交付率 | 09/11/2026 | quá hạn | — | New |
| [#468](https://github.com/hoctt-1111/sakura-market-lab5/issues/468) | Mã hoá tệp xuất, mức thuế, vùng chạm và độ tương phản tablet | 09/11/2026 | quá hạn | [#300](https://github.com/hoctt-1111/sakura-market-lab5/issues/300) | Pending |
| [#142](https://github.com/hoctt-1111/sakura-market-lab5/issues/142) | Trạng thái lô và phạm vi huỷ giao dịch 相対 (một phần, kênh せり) | 09/11/2026 | quá hạn | [#133](https://github.com/hoctt-1111/sakura-market-lab5/issues/133) | Pending |
| [#139](https://github.com/hoctt-1111/sakura-market-lab5/issues/139) | Điều kiện và hạn mức bán cho bên thứ ba 第三者販売 | 09/11/2026 | quá hạn | — | New |
| [#409](https://github.com/hoctt-1111/sakura-market-lab5/issues/409) | Quy trình duyệt xoá cứng và kho lưu lạnh | 09/11/2026 | quá hạn | — | New |
| [#140](https://github.com/hoctt-1111/sakura-market-lab5/issues/140) | Chợ có tập quán đặt trước 事前予約 hay không | 09/11/2026 | quá hạn | — | Pending |
| [#216](https://github.com/hoctt-1111/sakura-market-lab5/issues/216) | Dung sai 精算 giữa số đã giao và số giao dịch | 09/11/2026 | quá hạn | — | New |
| [#78](https://github.com/hoctt-1111/sakura-market-lab5/issues/78) | Bảng chuyển trạng thái tư cách và trạng thái 再審査 | 23/11/2026 | — | [#73](https://github.com/hoctt-1111/sakura-market-lab5/issues/73), [#75](https://github.com/hoctt-1111/sakura-market-lab5/issues/75) | Pending |
| [#144](https://github.com/hoctt-1111/sakura-market-lab5/issues/144) | Cách gán bên bán 売り手 cho giao dịch 相対 ở hệ đích | 23/11/2026 | — | [#129](https://github.com/hoctt-1111/sakura-market-lab5/issues/129) | Pending |
| [#518](https://github.com/hoctt-1111/sakura-market-lab5/issues/518) | Vai được duyệt bản ghi 相対 và せり ở bước chờ xác nhận | 23/11/2026 | — | [#129](https://github.com/hoctt-1111/sakura-market-lab5/issues/129), [#173](https://github.com/hoctt-1111/sakura-market-lab5/issues/173) | New |
| [#177](https://github.com/hoctt-1111/sakura-market-lab5/issues/177) | Số lần tái せり tối đa cho mỗi lô | 23/11/2026 | — | [#173](https://github.com/hoctt-1111/sakura-market-lab5/issues/173) | Pending |
| [#217](https://github.com/hoctt-1111/sakura-market-lab5/issues/217) | Danh mục lý do và người xác nhận ngoại lệ giao hàng | 23/11/2026 | — | [#214](https://github.com/hoctt-1111/sakura-market-lab5/issues/214) | New |
| [#509](https://github.com/hoctt-1111/sakura-market-lab5/issues/509) | Giao dịch nào vào 日次照合表 và thế nào là lệch | 23/11/2026 | — | [#236](https://github.com/hoctt-1111/sakura-market-lab5/issues/236) | New |
| [#20](https://github.com/hoctt-1111/sakura-market-lab5/issues/20) | Ai xác nhận 次期差分 và cách đưa chênh lệch vào kỳ sau | 23/11/2026 | — | [#15](https://github.com/hoctt-1111/sakura-market-lab5/issues/15) | Pending |
| [#517](https://github.com/hoctt-1111/sakura-market-lab5/issues/517) | Báo cáo ngày do người chạy hay hệ tự lập khi hết 業務日 | 23/11/2026 | — | — | New |
| [#366](https://github.com/hoctt-1111/sakura-market-lab5/issues/366) | Danh mục sự kiện thông báo và sự kiện nào ở mức Critical | 23/11/2026 | — | [#362](https://github.com/hoctt-1111/sakura-market-lab5/issues/362), [#364](https://github.com/hoctt-1111/sakura-market-lab5/issues/364) | Pending |
| [#385](https://github.com/hoctt-1111/sakura-market-lab5/issues/385) | Yêu cầu xoá dữ liệu cá nhân nằm ở bảng chỉ thêm | 23/11/2026 | — | [#381](https://github.com/hoctt-1111/sakura-market-lab5/issues/381), [#382](https://github.com/hoctt-1111/sakura-market-lab5/issues/382) | Pending |
| [#143](https://github.com/hoctt-1111/sakura-market-lab5/issues/143) | Lượng khả dụng của lô khi bán một phần 相対 | 23/11/2026 | — | — | Pending |
| [#270](https://github.com/hoctt-1111/sakura-market-lab5/issues/270) | Số người giữ vai lập và vai duyệt bản quy tắc | 23/11/2026 | — | [#267](https://github.com/hoctt-1111/sakura-market-lab5/issues/267) | Pending |
| [#306](https://github.com/hoctt-1111/sakura-market-lab5/issues/306) | Chỉ số đã công bố dùng cho báo cáo tháng RPT-10, RPT-11 | 23/11/2026 | — | [#297](https://github.com/hoctt-1111/sakura-market-lab5/issues/297), [#298](https://github.com/hoctt-1111/sakura-market-lab5/issues/298) | Pending |
| [#307](https://github.com/hoctt-1111/sakura-market-lab5/issues/307) | Mục tiêu số ngày xử lý tranh chấp cho báo cáo RPT-09 | 23/11/2026 | — | [#296](https://github.com/hoctt-1111/sakura-market-lab5/issues/296) | New |
| [#511](https://github.com/hoctt-1111/sakura-market-lab5/issues/511) | 買出人 có được mua qua 相対 không, hạn tham gia quản lý thế nào | 23/11/2026 | — | [#73](https://github.com/hoctt-1111/sakura-market-lab5/issues/73), [#76](https://github.com/hoctt-1111/sakura-market-lab5/issues/76), [#129](https://github.com/hoctt-1111/sakura-market-lab5/issues/129) | New |
| [#516](https://github.com/hoctt-1111/sakura-market-lab5/issues/516) | Cách đếm trần 4 lần đổi bản quy tắc mỗi năm | 23/11/2026 | — | [#267](https://github.com/hoctt-1111/sakura-market-lab5/issues/267) | New |
| [#435](https://github.com/hoctt-1111/sakura-market-lab5/issues/435) | Nguồn di trú, độ sâu lịch sử cần nạp, ai quyết chênh lệch | Trước khi khoá quy tắc ánh xạ ở MIG-01 | — | — | Pending |
| [#194](https://github.com/hoctt-1111/sakura-market-lab5/issues/194) | Người đề nghị và số cấp duyệt bút toán đảo 赤伝 | Trước khi viết code FG-06 | — | — | New |
| [#305](https://github.com/hoctt-1111/sakura-market-lab5/issues/305) | Cách kết nối và môi trường thử với hệ kế toán | Trước UAT | — | — | New |
| [#469](https://github.com/hoctt-1111/sakura-market-lab5/issues/469) | Mẫu tablet hiện trường và danh sách trình duyệt đã duyệt | Trước lần chạy ma trận tương thích đầu tiên ở NFR-COMP/TEST | — | — | New |
| [#45](https://github.com/hoctt-1111/sakura-market-lab5/issues/45) | Vai nội bộ cho nhóm 照合事務 và 取引運用 | Trước khi viết RBAC ở LAB-5 | — | — | New |

Các câu dưới đây có hạn gốc trước ngày bắt đầu dự án 09/11/2026 và vẫn chưa có trả lời ở ngày chụp 19/11/2026:

| Issue | Câu cần chốt | Hạn đặt ban đầu | Việc đang chờ câu trả lời | Trạng thái |
| --- | --- | --- | --- | --- |
| [#44](https://github.com/hoctt-1111/sakura-market-lab5/issues/44) | Ngưỡng hết phiên và khoá tạm khi đăng nhập sai | 19/10/2026 | — | New |
| [#497](https://github.com/hoctt-1111/sakura-market-lab5/issues/497) | Ranh giới 対象期 của 完納奨励金 và đường nhập 入金 | 31/10/2026 | [#13](https://github.com/hoctt-1111/sakura-market-lab5/issues/13), [#15](https://github.com/hoctt-1111/sakura-market-lab5/issues/15) | New |
<!-- gen:pr-hoi-khach:end -->

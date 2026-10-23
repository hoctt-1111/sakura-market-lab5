# Tiêu chí audit

Thước đo: Quy ước vận hành GitHub Project của công ty, bản mã hoá trong công cụ audit nội bộ; không phải nguyên văn. Ngày: 2026-10-23.

| Mã | Chiều | Tiêu chí | Nguồn | Cách đo | Mức | Áp dụng | Lý do / ghi chú | Cách sửa |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | A | Mọi khoá seed có đúng một issue sống; không issue lạ | quy ước A · gate G-BOARD | khoá từ tiêu đề so với seed, bỏ bản thay thế | B | có |  | Khoá lạ: đóng issue kèm nhãn thay thế nếu thừa, hoặc thêm khoá vào seed nếu là việc thật. Khoá thiếu: tạo issue từ seed |
| A2 | A | Epic có story; story có sub-issue; điều tra không có con | task-breakdown §1 | đếm con sống theo cha | B | có |  | Epic, story rỗng: thêm con theo seed hoặc đóng kèm nhãn thay thế; điều tra có con: chuyển con lên story |
| A3 | A | Bản thay thế đã đóng, Status Closed, không giữ Sprint, ngày, giờ đã làm, Done Date | dong_thua · ticket đóng không còn là việc | lọc nhãn thay thế, soi state, Status, Sprint, Start, Due, Spent, Done | W | có |  | Bản thay thế đã đóng: đặt Status = Closed, xoá Sprint, Start Date, Due Date, Spent time, Done Date. Issue còn mở mà mang nhãn thay thế: đóng issue nếu đúng là bản thừa, hoặc gỡ nhãn nếu là việc thật |
| B1 | B | Item có Sprint khi và chỉ khi có trong kế hoạch sprint; Start, Due đúng ngày sprint | quy ước B · quy-uoc-sprint | so khoá và 3 field với sprint-plan | B | có |  | Gán hoặc gỡ Sprint theo kế hoạch sprint; đặt Start Date, Due Date bằng ngày của sprint |
| B2 | B | Chỉ việc lá và điều tra được gán Sprint; epic, story để trống | quy-uoc-sprint | tracker × Sprint | W | có |  | Gỡ Sprint khỏi epic, story; xếp việc lá của nó vào Sprint thay vào đó |
| B3 | B | Item trong Sprint có Owner, Start không sau Due | quy ước C (Start, Due bắt buộc) | 3 field | W | có |  | Điền Owner, Start Date, Due Date; ngày bắt đầu không sau hạn |
| B4 | B | Tổng giờ ước của một Owner trong một Sprint không vượt trần năng lực | quy-uoc-sprint (tran, so_nguoi) | cộng Estimated theo Owner × Sprint | W | có |  | Dời bớt việc lá của Owner đó sang sprint sau hoặc chia cho vị trí cùng bộ phận |
| C1 | C | Tiêu đề đúng khuôn [TRACKER] KHOÁ, tracker hợp lệ | quy ước C · seed_luat | regex tiêu đề | W | có |  | Sửa tiêu đề về khuôn [TRACKER] KHOÁ tên, tracker thuộc danh sách hợp lệ |
| C2 | C | Khoá đúng khuôn theo tầng (epic, story, lá có hậu tố bộ phận) | board_seed_rules | regex theo tracker | W | có |  | Sửa khoá theo khuôn của tầng (epic, story, lá có hậu tố bộ phận) |
| C3 | C | Lá FE, BE, DB, INFRA, PM, BRSE mang nhãn team khớp bộ phận | quy ước C (lá thiếu team) | nhãn team so hậu tố khoá | W | có |  | Gắn đúng một nhãn team khớp hậu tố bộ phận, gỡ nhãn team khác |
| C3b | C | Lá TEST mang nhãn team | quy ước C (lá thiếu team) | nhãn team trên lá TEST | I | có | bộ nhãn dự án không có nhãn team cho QA; ghi khoảng cách | Thêm nhãn team cho QA vào bộ nhãn rồi gắn cho lá kiểm thử (hoặc giữ, đã ghi khoảng cách) |
| C4 | C | Đúng một nhãn type, khớp tracker | quy ước C · labels.yaml | đếm nhãn type | W | có |  | Gắn đúng một nhãn type khớp tracker trong tiêu đề, gỡ nhãn type khác |
| C5 | C | Đủ Status, Priority, Owner, Story Point, Estimated time và người phụ trách | quy ước C (field bắt buộc) · đề LAB-5 | 5 field + assignee | W | có |  | Điền các field còn trống và gán người phụ trách |
| C6 | C | Priority hợp lệ; story ràng buộc đặc thù hoặc epic ưu tiên ít nhất High | priority_map · muc_uu_tien | field + nhãn ràng buộc + epic | W | có |  | Đặt Priority trong danh sách; issue mang nhãn ràng buộc đặc thù hoặc thuộc epic ưu tiên đặt High trở lên |
| C7 | C | Status thuộc luồng giả lập; QA Testing chỉ ở lá TEST | status_gia_lap | field × tracker | W | có |  | Đổi Status về một giá trị trong luồng; QA Testing chỉ dùng cho lá kiểm thử |
| C8 | C | Tiêu đề story song ngữ Nhật - Anh | quy ước C | - | W | không | Bài nộp viết tiếng Việt, thuật ngữ Nhật đặt trong ngoặc; repo không dành cho khách Nhật |  |
| C9 | C | Field Plan Sprint, Roadmap, Target version | quy ước C (field bắt buộc) | - | I | không | Board không có ba field này; sprint kế hoạch nằm ở tệp kế hoạch, Iteration Sprint đóng vai Target |  |
| D1 | D | Story Point, Estimated time, Spent time của cha bằng tổng con | quy ước D · luật tổng phần = gốc | cộng theo cha | B | có |  | Đặt Story Point, Estimated time, Spent time của cha bằng tổng con (chạy lại bước ghi field) |
| D2 | D | Status cha suy đúng từ con; epic, story không Closed trong giả lập | luật suy Status cha | suy rồi so | W | có |  | Đặt Status cha theo con: New khi mọi con chưa làm, ngược lại In Progress; không Closed khi chưa nghiệm thu |
| D3 | D | Sub-issues progress khớp số con thật | GitHub | so tổng con trên GitHub với đếm cha | I | có |  | Kiểm sub-issue của cha trên GitHub: con bị gỡ hoặc gắn nhầm cha |
| D4 | D | Owner lá đúng luật theo bộ phận, miền và ngoại lệ | owner_theo_leaf · owner_mien · owner_ngoai_le | tra luật theo khoá và epic | W | có |  | Đổi Owner theo luật: ngoại lệ, luật bộ phận, danh sách chuyển cân tải, miền theo epic |
| D5 | D | Sprint ghi trong thân khớp field; Slip đúng | quy ước D | - | W | không | Cần thân issue (ngoài phạm vi đọc field) và board không có field Slip |  |
| E1 | E | Mọi item trừ epic có cha đúng tầng | quy ước E · task-breakdown §1 | cha + tracker hai đầu | B | có |  | Gắn issue vào cha đúng tầng (story dưới epic, lá dưới story, điều tra dưới epic) |
| E2 | E | Item nằm đúng epic của seed | board_snapshot_rules | epic theo chuỗi cha so epic seed | W | có |  | Chuyển issue sang dưới epic mà seed ghi, hoặc sửa seed nếu đổi epic có chủ đích |
| E3 | E | Không cha nào quá 100 con | giới hạn sub-issue của GitHub | đếm | W | có |  | Tách cha thành nhiều cha, mỗi cha tối đa 100 con |
| F1 | F | Không hai issue sống cùng khoá | quy ước F | nhóm theo khoá, bỏ bản thay thế | B | có |  | Giữ một issue sống cho khoá; issue còn lại đóng kèm nhãn thay thế |
| G1 | G | Cha Closed mà còn con chưa Closed | quy ước G | cây | B | có |  | Mở lại cha (Status theo con) hoặc đóng nốt các con chưa xong |
| G2 | G | Closed khi và chỉ khi có Done Date; Done Date không sau ngày chụp; chưa làm thì không có giờ đã làm | luật giả lập | field | W | có |  | Closed thì điền Done Date không sau ngày xét; chưa Closed thì xoá Done Date; chưa làm thì xoá giờ đã làm |
| G3 | G | Status Closed mà issue GitHub còn mở | quy ước G (trạng thái xong) | field so state | I | có | ngoại lệ đã khai: giả lập không đóng issue trên GitHub | Đóng issue trên GitHub, hoặc giữ mở nếu là giả lập đã khai |
| G4 | G | Lá Closed không trái phụ thuộc; Done Date lá sau không trước lá trước | phu-thuoc-la.yaml | cây + Done Date | B | có |  | Mở lại lá về trạng thái chờ hoặc đóng phụ thuộc trước; Done Date lá sau không trước lá trước |
| H1 | H | Quá hạn: Due trước ngày chụp mà chưa Closed | quy ước H | field | W | có |  | Đóng việc, hoặc dời hạn kèm lý do trượt ở báo cáo tiến độ |
| H2 | H | Trượt: Done Date sau Due | quy ước H | field | I | có |  | Ghi lý do trượt; xem lại ước lượng của việc cùng loại |
| H3 | H | Field Slip | quy ước H | - | I | không | Board không có field Slip; trượt đo bằng H2 |  |
| I1 | I | Bug có Priority và dẫn chiếu lần chạy kiểm thử | quy ước I | - | I | không | Backlog không có tracker bug (một sprint giả lập, chưa có bug) |  |
| J1 | J | Thân lá khớp phạm vi story cha | quy ước J | - | W | không | Cần thân issue; băm thân đã khoá bằng bản đồ board khi chụp có thân |  |
| K1 | K | Story thay đổi yêu cầu đủ link pull request | quy ước K | - | W | không | Backlog không có tracker thay đổi yêu cầu, chưa có pull request |  |
| L1 | L | Giờ ước của một lá không vượt trần một sprint của vai | task-breakdown §1 · P-58 | Estimated × Owner | W | có |  | Tách lá thành phần nhỏ hơn hoặc tách story theo sprint, mỗi phần vừa một sprint của vai |
| L2 | L | Lá kế thừa nhãn ràng buộc đặc thù của story | seed_luat RANG_BUOC | nhãn cha so con | I | có |  | Gắn cho lá các nhãn ràng buộc đặc thù của story cha |
| L3 | L | Project public, đủ field theo cấu hình | đề LAB-5 · field_map | project.public, project.fields | B | có |  | Đặt Project public; tạo field còn thiếu với đúng tên trong cấu hình |

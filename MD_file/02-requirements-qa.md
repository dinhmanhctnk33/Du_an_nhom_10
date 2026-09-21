# PROMPT – XÂY DỰNG TÀI LIỆU REQUIREMENTS QA

## 1. VAI TRÒ

Bạn đóng vai trò đồng thời là:

- **Business Analyst (BA)**
- **Product Owner (PO)**
- **System Analyst**
- **Requirements Engineer**
- **Technical Writer**

Bạn có kinh nghiệm trong:

- BABOK v3;
- Requirements Engineering;
- Stakeholder Analysis;
- Requirements Elicitation;
- Interview & Survey Design;
- Business Process Analysis;
- User Story Mapping;
- Agile/Scrum;
- Prompt Engineering;
- AI-Augmented Software Development Lifecycle (SDLC).

Nhiệm vụ của bạn là **phân tích các tài liệu nguồn, xác định những điểm đã rõ/chưa rõ, thiết kế câu hỏi khai thác yêu cầu, ghi nhận giả định và câu hỏi mở, đồng thời tạo đầu vào có cấu trúc cho tài liệu SRS**.

Tài liệu được tạo ra là:

> **Requirements QA – Requirements Quality Assurance**

Đây là tài liệu **phân tích và làm rõ yêu cầu**, không phải tài liệu đặc tả yêu cầu chính thức.

---

# 2. MỤC TIÊU

Hoàn thiện tài liệu:

```text
02_GenAI_SoftwareDevelopment_requirements-qa.docx trong thư mục con Mau
```

Mục tiêu của tài liệu:

1. Xác định và phân tích stakeholder.
2. Tổng hợp thông tin yêu cầu hiện có.
3. Xác định những nội dung chưa rõ, thiếu hoặc có khả năng mâu thuẫn.
4. Thiết kế các câu hỏi cần đặt ra để làm rõ yêu cầu.
5. Ghi nhận câu trả lời nếu nguồn đã cung cấp.
6. Phân biệt rõ:
   - thông tin đã xác nhận;
   - thông tin cần xác nhận;
   - giả định;
   - câu hỏi mở.
7. Ghi nhận các quyết định sau khi làm rõ.
8. Xác định các yêu cầu dự kiến sẽ được chuyển sang tài liệu SRS.
9. Kiểm tra tính nhất quán của yêu cầu ở mức phân tích.
10. Xác định các rủi ro liên quan đến yêu cầu.
11. Chuẩn bị một bộ đầu vào có cấu trúc, có thể truy vết sang SRS.

---

# 3. RANH GIỚI TÀI LIỆU

## 3.1. Requirements QA được phép thực hiện

Tài liệu phải tập trung vào:

- Stakeholder Analysis;
- Requirements Elicitation;
- Requirements Clarification;
- Ambiguity Analysis;
- Conflict Analysis;
- Assumption Analysis;
- Open Questions;
- Decision Log;
- Draft Requirement Mapping;
- Requirements Risk;
- AI hỗ trợ quá trình phân tích yêu cầu.

## 3.2. Không thực hiện trong Requirements QA

Không biến tài liệu này thành SRS.

Không đặc tả chi tiết:

- toàn bộ Functional Requirements;
- toàn bộ Non-functional Requirements;
- Acceptance Criteria hoàn chỉnh;
- Class Diagram;
- Class/Method;
- Sequence Diagram;
- API Specification chi tiết;
- Database Schema chi tiết;
- Test Case chi tiết.

Các yêu cầu sau khi được làm rõ sẽ được chuẩn hóa và đặc tả chính thức trong:

```text
03_GenAI_SoftwareDevelopment_requirements-specification.docx
```

---

# 4. NGUỒN DỮ LIỆU

Bắt buộc đọc và phân tích đầy đủ các nguồn sau:

```text
informember.md
project.md
01_GenAI_SoftwareDevelopment_project-plan.docx trong thư mục con Mau
```

## 4.1. `informember.md`

Sử dụng để xác định:

- tên nhóm;
- danh sách thành viên;
- trưởng nhóm;
- vai trò đã được xác định.

## 4.2. `project.md`

Sử dụng để xác định:

- bối cảnh;
- vấn đề;
- mục tiêu;
- phạm vi;
- đối tượng sử dụng;
- chức năng;
- dữ liệu;
- AI;
- công nghệ;
- các ràng buộc đã được nêu.

## 4.3. `01_GenAI_SoftwareDevelopment_project-plan.docx`

Sử dụng để xác định:

- tiến độ;
- milestone;
- sprint;
- deliverable;
- phạm vi công việc;
- phân công;
- định hướng sử dụng AI;
- các nội dung liên quan đến Requirements QA.

---

# 5. NGUYÊN TẮC SỬ DỤNG NGUỒN

Đây là yêu cầu bắt buộc.

## 5.1. Không tự tạo dữ kiện

Không được tự tạo thành thông tin chính thức:

- stakeholder;
- chức năng;
- công nghệ;
- AI model;
- API;
- deadline;
- yêu cầu nghiệp vụ;
- dữ liệu;
- quy trình;
- quy tắc nghiệp vụ.

Nếu thông tin không xuất hiện trong nguồn, phải đánh dấu là:

> **Chưa có thông tin**

hoặc:

> **Giả định đề xuất**

Không được trình bày suy luận như một thông tin đã được xác nhận.

## 5.2. Phân biệt 3 loại thông tin

Mọi nội dung phải được phân loại thành:

### Source-confirmed

Thông tin được xác nhận trực tiếp từ tài liệu nguồn.

### Inference

Thông tin được suy luận hợp lý từ nguồn.

### Assumption

Thông tin được đề xuất để có thể tiếp tục phân tích nhưng chưa được xác nhận.

Không được trộn ba loại này.

---

# 6. QUY TRÌNH PHÂN TÍCH

Thực hiện theo pipeline:

```text
Đọc nguồn
   ↓
Xác định thông tin hiện có
   ↓
Phân tích stakeholder
   ↓
Phân tích phạm vi & nghiệp vụ
   ↓
Phát hiện thiếu / mơ hồ / mâu thuẫn
   ↓
Thiết kế câu hỏi elicitation
   ↓
Ghi nhận câu trả lời
   ↓
Ghi nhận Assumption / Open Question
   ↓
Ghi nhận Decision
   ↓
Draft Requirement Mapping
   ↓
Requirements QA Review
   ↓
Chuẩn bị đầu vào cho SRS
```

Không bỏ qua các bước quan trọng.

---

# 7. BƯỚC 1 – TỔNG HỢP REQUIREMENTS BASELINE

Trước khi đặt câu hỏi, tạo một baseline ngắn gồm:

- Project Name;
- Business Context;
- Business Problem;
- Project Objectives;
- Scope;
- Out of Scope;
- Stakeholders đã xác định;
- User Types;
- Main Business Processes;
- Main Functional Areas;
- AI-related Features;
- Data Entities được đề cập;
- Constraints;
- Existing Decisions;
- Existing Open Issues.

Mục đích là xác định:

> **Nhóm đã biết gì và nhóm chưa biết gì?**

Không được suy diễn thêm ngoài nguồn.

---

# 8. BƯỚC 2 – STAKEHOLDER ANALYSIS

Xác định stakeholder dựa trên tài liệu nguồn trước.

Chỉ bổ sung stakeholder hợp lý nếu có căn cứ từ phạm vi hoặc quy trình nghiệp vụ.

Mỗi stakeholder gồm:

| ID | Stakeholder | Vai trò | Mục tiêu | Thông tin cần khai thác | Mức ảnh hưởng | Trạng thái |
|---|---|---|---|---|---|---|

Sử dụng mã:

```text
STK-001
STK-002
...
```

### Trạng thái

Chỉ sử dụng:

- `Đã xác nhận`
- `Cần xác nhận`
- `Chưa có thông tin`

Không tự xác nhận stakeholder nếu nguồn chưa xác nhận.

---

# 9. BƯỚC 3 – REQUIREMENTS ELICITATION QUESTIONS

Thiết kế khoảng:

> **50–80 câu hỏi**

Số lượng có thể điều chỉnh nếu tài liệu nguồn quá ít hoặc quá nhiều, nhưng phải đảm bảo **đủ chiều sâu và không đặt câu hỏi trùng lặp**.

Câu hỏi phải được nhóm theo chủ đề.

## Nhóm A – Business & Scope

- mục tiêu nghiệp vụ;
- phạm vi;
- out-of-scope;
- success criteria;
- quy trình hiện tại;
- vấn đề cần giải quyết.

## Nhóm B – User & Stakeholder

- người dùng;
- vai trò;
- quyền;
- trách nhiệm;
- nhu cầu.

## Nhóm C – Parking Business Process

- xe vào;
- xác định xe;
- cấp vé;
- xác định vị trí;
- xe ra;
- tính phí;
- thanh toán;
- xử lý mất vé;
- xử lý sai thông tin.

## Nhóm D – Vehicle & Parking Management

- loại xe;
- vị trí;
- khu vực;
- trạng thái chỗ;
- xe đang gửi;
- xe tháng;
- dữ liệu lịch sử.

## Nhóm E – Ticket & Pricing

- vé;
- vé tháng;
- bảng giá;
- cách tính phí;
- miễn/giảm;
- thay đổi giá;
- xử lý ngoại lệ.

## Nhóm F – Reporting

- loại báo cáo;
- thời gian;
- bộ lọc;
- thống kê;
- export;
- quyền xem.

## Nhóm G – Authentication & Authorization

- đăng nhập;
- role;
- permission;
- session;
- account management.

## Nhóm H – Data

- dữ liệu bắt buộc;
- dữ liệu tùy chọn;
- validation;
- retention;
- backup;
- consistency.

## Nhóm I – AI

- mục đích AI;
- input;
- output;
- dữ liệu được sử dụng;
- quyền truy cập;
- prompt;
- hallucination;
- human verification;
- fallback;
- API/model;
- giới hạn AI.

## Nhóm J – Security

- authentication;
- authorization;
- sensitive data;
- API key;
- audit;
- input validation.

## Nhóm K – Performance & Availability

- response time;
- concurrency;
- uptime;
- timeout;
- rate limit.

## Nhóm L – Deployment & Operation

- môi trường;
- hosting;
- database;
- configuration;
- logging;
- monitoring.

## Nhóm M – Future Expansion

- mobile;
- camera;
- OCR;
- QR;
- payment gateway;
- IoT;
- AI nâng cao.

Chỉ đưa các mục Future Expansion vào dạng **câu hỏi**, không mặc định chúng thuộc phạm vi dự án.

---

# 10. CẤU TRÚC MỖI CÂU HỎI

Mỗi câu hỏi phải có:

| Trường | Nội dung |
|---|---|
| QA ID | `QA-001` |
| Category | Nhóm câu hỏi |
| Question | Câu hỏi |
| Purpose | Mục đích hỏi |
| Stakeholder | Người cần trả lời |
| Existing Answer | Câu trả lời nếu nguồn đã có |
| Status | Trạng thái |
| Related Topic | Chủ đề liên quan |
| Draft Requirement | Yêu cầu dự kiến liên quan |

### Status chỉ sử dụng:

- `Đã rõ`
- `Cần xác nhận`
- `Chưa có thông tin`

Không sử dụng trạng thái mơ hồ như:

- “Có vẻ ổn”;
- “Tạm thời”;
- “Có thể”.

---

# 11. BƯỚC 4 – AMBIGUITY ANALYSIS

Phát hiện những từ/cụm từ không đủ chính xác.

Ví dụ:

> “tìm kiếm nhanh”

Phải đặt câu hỏi:

- nhanh là bao nhiêu giây?
- dữ liệu nào được tìm?
- tìm theo trường nào?
- có fuzzy search không?
- ai được sử dụng?

Ví dụ:

> “AI hỗ trợ quản lý”

Phải làm rõ:

- AI hỗ trợ nhiệm vụ nào?
- input là gì?
- output là gì?
- ai sử dụng?
- AI có quyền truy cập dữ liệu nào?
- kết quả AI có được sử dụng trực tiếp không?
- có human verification không?

Tạo bảng:

| ID | Nội dung | Loại mơ hồ | Ảnh hưởng | Câu hỏi làm rõ | Trạng thái |
|---|---|---|---|---|---|

Mã:

```text
AMB-001
AMB-002
...
```

---

# 12. BƯỚC 5 – CONFLICT ANALYSIS

Tìm các yêu cầu hoặc thông tin có khả năng mâu thuẫn.

Ví dụ:

- một phần nói admin được sửa dữ liệu;
- phần khác chỉ cho manager sửa.

Hoặc:

- một nơi nói AI được sử dụng tự động;
- nơi khác yêu cầu người dùng xác nhận.

Tạo bảng:

| ID | Nội dung 1 | Nội dung 2 | Mâu thuẫn | Ảnh hưởng | Cách xử lý | Trạng thái |
|---|---|---|---|---|---|---|

Mã:

```text
CON-001
CON-002
...
```

Nếu không phát hiện mâu thuẫn, ghi rõ:

> **Không phát hiện mâu thuẫn trực tiếp trong các nguồn đã cung cấp.**

Không tự tạo conflict.

---

# 13. BƯỚC 6 – ASSUMPTIONS

Chỉ tạo assumption khi:

- nguồn chưa xác nhận;
- cần một giả định để tiếp tục phân tích;
- assumption có ảnh hưởng đến thiết kế yêu cầu.

Mã:

```text
ASM-001
ASM-002
...
```

Cấu trúc:

| ID | Assumption | Cơ sở | Ảnh hưởng | Người cần xác nhận | Status |
|---|---|---|---|---|---|

Status:

- `Chưa xác nhận`
- `Đã xác nhận`
- `Bị loại bỏ`

Không biến assumption thành requirement chính thức.

---

# 14. BƯỚC 7 – OPEN QUESTIONS

Open Question là câu hỏi chưa thể kết luận từ nguồn hiện tại.

Mã:

```text
OQ-001
OQ-002
...
```

Cấu trúc:

| ID | Open Question | Lý do | Ảnh hưởng | Người xác nhận | Priority | Status |
|---|---|---|---|---|---|---|

Priority:

- High;
- Medium;
- Low.

Ưu tiên High cho câu hỏi có khả năng ảnh hưởng đến:

- scope;
- architecture;
- database;
- AI;
- security;
- cost;
- timeline.

---

# 15. BƯỚC 8 – DECISION LOG

Khi một vấn đề đã được làm rõ, ghi nhận quyết định.

Mã:

```text
DEC-001
DEC-002
...
```

Cấu trúc:

| ID | Vấn đề | Quyết định | Cơ sở | Ngày | Người xác nhận | Requirement liên quan |
|---|---|---|---|---|---|---|

Nếu chưa có quyết định, không được tạo `DEC`.

---

# 16. BƯỚC 9 – DRAFT REQUIREMENT MAPPING

Sau khi phân tích QA, xác định những nội dung có khả năng trở thành requirement.

Mã:

```text
FR-DRAFT-001
NFR-DRAFT-001
AIR-DRAFT-001
```

Trong đó:

- `FR-DRAFT` = Functional Requirement dự kiến;
- `NFR-DRAFT` = Non-functional Requirement dự kiến;
- `AIR-DRAFT` = AI Requirement dự kiến.

Bảng:

| Draft ID | Nguồn QA | Nội dung đã làm rõ | Loại | Priority | Ghi chú cho SRS |
|---|---|---|---|---|---|

## Nguyên tắc

Chỉ ghi:

> **Yêu cầu dự kiến**

Không viết thành đặc tả SRS hoàn chỉnh.

Ví dụ:

Không viết:

> FR-001: Hệ thống phải cho phép nhân viên đăng nhập bằng username/password...

Nên viết:

> FR-DRAFT-001: Xác định cơ chế xác thực dành cho nhân viên bãi đỗ.

Sau khi quyết định được xác nhận, SRS mới chuẩn hóa thành requirement chính thức.

---

# 17. BƯỚC 10 – REQUIREMENTS TRACEABILITY

Phải đảm bảo có thể truy vết:

```text
Stakeholder
     ↓
Question
     ↓
Clarification
     ↓
Decision / Assumption
     ↓
Draft Requirement
     ↓
SRS
```

Tạo bảng traceability:

| Stakeholder | QA ID | AMB/CON/OQ | DEC/ASM | Draft Requirement | SRS Target |
|---|---|---|---|---|---|

Nếu chưa có SRS ID, ghi:

> `To be defined in SRS`

Không tự tạo SRS ID.

---

# 18. BƯỚC 11 – REQUIREMENTS RISK

Xác định rủi ro phát sinh từ yêu cầu.

Mã:

```text
RR-001
RR-002
...
```

Các nhóm rủi ro:

- Requirement Ambiguity;
- Requirement Conflict;
- Missing Requirement;
- Scope Creep;
- AI Requirement Uncertainty;
- Security Requirement Uncertainty;
- Performance Requirement Uncertainty;
- Stakeholder Availability.

Cấu trúc:

| ID | Risk | Cause | Impact | Probability | Severity | Mitigation | Owner |
|---|---|---|---|---|---|---|---|

Không đánh giá xác suất/mức độ nghiêm trọng nếu không có căn cứ; khi cần phải ghi là **đánh giá sơ bộ**.

---

# 19. AI SUPPORT TRONG REQUIREMENTS QA

Mô tả rõ AI được sử dụng để hỗ trợ:

- sinh câu hỏi elicitation;
- phân loại câu hỏi;
- phát hiện ambiguity;
- phát hiện conflict;
- nhóm requirements;
- chuẩn hóa thuật ngữ;
- phát hiện thiếu thông tin;
- đề xuất assumption;
- kiểm tra traceability;
- kiểm tra consistency.

## Human-in-the-loop

AI **không được xem là nguồn sự thật cuối cùng**.

Mọi kết quả do AI tạo phải được:

```text
AI Suggestion
      ↓
BA Review
      ↓
Source Verification
      ↓
Stakeholder Confirmation
      ↓
Final Decision
```

Không sử dụng output AI như requirement chính thức nếu chưa được kiểm chứng.

---

# 20. CẤU TRÚC TÀI LIỆU WORD

Tài liệu hoàn chỉnh cần có cấu trúc:

## 1. Introduction

- Purpose;
- Scope;
- Audience;
- Elicitation Approach;
- References.

## 2. Requirements Baseline

- Business Context;
- Business Problem;
- Objectives;
- Scope;
- Out of Scope;
- User Types;
- Main Processes;
- Functional Areas;
- AI Features;
- Constraints.

## 3. Stakeholder Analysis

## 4. Requirements Elicitation Questions

## 5. Clarification Log

## 6. Ambiguity Analysis

## 7. Conflict Analysis

## 8. Assumptions

## 9. Open Questions

## 10. Decision Log

## 11. Draft Requirement Mapping

## 12. Requirements Traceability

## 13. Requirements Risk

## 14. AI Support in Requirements QA

## 15. Conclusion

Không thêm các chương lớn khác nếu template không có.

---

# 21. QUY TẮC ĐỐI VỚI FILE WORD TEMPLATE

File:

```text
02_GenAI_SoftwareDevelopment_requirements-qa.docx
```

là **template chính thức**.

Phải chỉnh sửa trực tiếp trên template.

## Giữ nguyên

- Heading;
- font;
- style;
- bảng;
- numbering;
- layout;
- header/footer;
- page setup.

## Chỉ được

- thay placeholder;
- điền nội dung;
- bổ sung hàng trong bảng nếu cần;
- điều chỉnh kích thước bảng ở mức tối thiểu;
- điều chỉnh page break để tài liệu dễ đọc.

Không được tự ý:

- đổi template sang bố cục khác;
- tạo tài liệu mới từ đầu;
- xóa bảng;
- thay đổi hệ thống heading;
- đưa nội dung SRS vào Requirements QA.

---

# 22. KIỂM TRA CHẤT LƯỢNG TRƯỚC KHI XUẤT FILE

Bắt buộc thực hiện checklist:

## Source Validation

- [ ] Đã đọc đầy đủ 3 nguồn.
- [ ] Không bịa thông tin.
- [ ] Phân biệt source / inference / assumption.

## Stakeholder

- [ ] Stakeholder có căn cứ.
- [ ] Có mục tiêu và thông tin cần khai thác.
- [ ] Không tự xác nhận stakeholder chưa có nguồn.

## Elicitation

- [ ] Câu hỏi có mục đích.
- [ ] Không trùng lặp.
- [ ] Có stakeholder cần trả lời.
- [ ] Có trạng thái.

## Ambiguity

- [ ] Đã kiểm tra từ ngữ mơ hồ.
- [ ] Có impact.
- [ ] Có câu hỏi làm rõ.

## Conflict

- [ ] Đã kiểm tra mâu thuẫn.
- [ ] Không tự tạo conflict.
- [ ] Nếu không có conflict phải ghi rõ.

## Assumption

- [ ] Có mã ASM.
- [ ] Có cơ sở.
- [ ] Có người cần xác nhận.

## Open Question

- [ ] Có mã OQ.
- [ ] Có impact.
- [ ] Có priority.

## Decision

- [ ] Chỉ tạo DEC khi có quyết định.
- [ ] Có cơ sở và người xác nhận.

## Draft Requirement

- [ ] Có traceability.
- [ ] Chưa biến thành SRS.
- [ ] Có phân loại FR/NFR/AI.

## AI

- [ ] Có Human-in-the-loop.
- [ ] Có source verification.
- [ ] Không coi AI output là sự thật mặc định.

## Word

- [ ] Giữ nguyên template.
- [ ] Không còn placeholder.
- [ ] Không vỡ bảng.
- [ ] Không lỗi font.
- [ ] Không lỗi numbering.
- [ ] Không có trang trắng bất thường.
- [ ] Nội dung dễ đọc.

---

# 23. QUY TRÌNH THỰC HIỆN CUỐI CÙNG

Thực hiện chính xác theo trình tự:

```text
BƯỚC 1
Đọc informember.md
        ↓
BƯỚC 2
Đọc project.md
        ↓
BƯỚC 3
Đọc Project Plan
        ↓
BƯỚC 4
Xây dựng Requirements Baseline
        ↓
BƯỚC 5
Phân tích Stakeholder
        ↓
BƯỚC 6
Phát hiện Missing / Ambiguous / Conflict Information
        ↓
BƯỚC 7
Thiết kế 50–80 câu hỏi QA
        ↓
BƯỚC 8
Ghi nhận Answer / Status
        ↓
BƯỚC 9
Tạo Assumption / Open Question
        ↓
BƯỚC 10
Tạo Decision Log nếu có
        ↓
BƯỚC 11
Tạo Draft Requirement Mapping
        ↓
BƯỚC 12
Tạo Traceability
        ↓
BƯỚC 13
Phân tích Requirement Risk
        ↓
BƯỚC 14
Kiểm tra chất lượng
        ↓
BƯỚC 15
Điền trực tiếp vào Word Template
        ↓
BƯỚC 16
Kiểm tra định dạng Word
        ↓
BƯỚC 17
Xuất file hoàn chỉnh
```

---

# 24. OUTPUT CUỐI CÙNG

Xuất file:

```text
02_GenAI_SoftwareDevelopment_requirements-qa.docx
```

File phải là bản hoàn thiện từ **template gốc**, không phải một tài liệu được thiết kế lại.

Sau khi hoàn thành, báo cáo ngắn gọn:

- số lượng stakeholder;
- số lượng câu hỏi QA;
- số lượng câu hỏi đã rõ;
- số lượng câu hỏi cần xác nhận;
- số lượng ambiguity;
- số lượng conflict;
- số lượng assumption;
- số lượng open question;
- số lượng decision;
- số lượng draft requirement;
- số lượng requirement risk;
- các vấn đề quan trọng còn cần xác nhận;
- xác nhận file Word đã được lưu đúng tên và đúng định dạng.

Không viết lại toàn bộ nội dung Requirements QA trong phần trả lời.

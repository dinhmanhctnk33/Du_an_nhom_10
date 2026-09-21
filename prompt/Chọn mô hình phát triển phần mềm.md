# PROMPT LỰA CHỌN MÔ HÌNH PHÁT TRIỂN PHẦN MỀM

## 1. Vai trò

Bạn là **Software Project Manager, Business Analyst và Software Engineering Lecturer** có nhiều năm kinh nghiệm trong việc lựa chọn mô hình phát triển phần mềm cho các dự án thực tế, đặc biệt là các dự án có tích hợp **AI/Computer Vision**.

Hãy phân tích và lựa chọn **mô hình phát triển phần mềm phù hợp nhất** cho đề tài:

> **“Xây dựng hệ thống quản lý bãi đỗ xe có tích hợp AI trong thực tế”**

Đây là **dự án sinh viên trong môn “Ứng dụng trí tuệ nhân tạo”**, vì vậy phải cân bằng giữa:

* Tính phù hợp với nghiệp vụ thực tế.
* Khả năng triển khai của sinh viên.
* Thời gian thực hiện có giới hạn.
* Quy mô nhóm dự án.
* Mức độ thay đổi yêu cầu.
* Đặc thù phát triển chức năng AI.
* Khả năng kiểm thử và đánh giá mô hình AI.
* Khả năng trình bày, bảo vệ trước giảng viên.

---

# 2. Các skill cần vận dụng

Hãy vận dụng tư duy và phương pháp từ các skill liên quan trên `skills.sh`:

### `project-planning`

Dùng để đánh giá:

* Quy mô dự án.
* Độ phức tạp.
* Phân chia công việc.
* Khả năng lập kế hoạch theo giai đoạn/sprint.
* Khả năng thích nghi khi yêu cầu thay đổi.

Skill này nhấn mạnh việc điều chỉnh cách quản lý dự án theo **team size và project complexity**, thay vì áp dụng một quy trình cứng nhắc.

### `prd`

Dùng để xem xét:

* Yêu cầu nghiệp vụ.
* Yêu cầu AI.
* Phạm vi.
* Tiêu chí thành công.
* Các ràng buộc.
* Khả năng chia dự án thành các giai đoạn phát triển.

Đặc biệt lưu ý rằng dự án AI cần có cách đánh giá kết quả khác với phần mềm thông thường.

### `council`

Áp dụng tư duy **so sánh nhiều phương án trước khi đưa ra quyết định**, tập trung vào:

* Ưu điểm.
* Nhược điểm.
* Trade-off.
* Rủi ro.
* Chi phí triển khai.
* Khả năng kiểm thử.
* Khả năng thích nghi.

Không được chọn mô hình ngay từ đầu rồi tìm lý do để biện minh.

### `documentation-and-adrs`

Áp dụng nguyên tắc:

> **Document the decision, not just the result.**

Tức là phải ghi rõ:

**Các mô hình được xem xét → Tiêu chí đánh giá → Kết quả so sánh → Mô hình được chọn → Vì sao chọn → Vì sao loại các phương án còn lại.**

Điều này đặc biệt hữu ích để đưa trực tiếp vào phần **“Lựa chọn mô hình phát triển phần mềm”** của báo cáo.

### `ai-feature-prd`

Vận dụng tư duy đặc thù của hệ thống AI:

* Kết quả AI mang tính xác suất.
* Cần dữ liệu để phát triển/đánh giá.
* Cần đánh giá mô hình.
* Có thể phải điều chỉnh mô hình/dữ liệu trong quá trình phát triển.
* AI cần được kiểm thử và đánh giá riêng với phần mềm nghiệp vụ.

---

# 3. Bối cảnh dự án

Hãy sử dụng các thông tin sau làm **bối cảnh mặc định**:

### Tên đề tài

**“Xây dựng hệ thống quản lý bãi đỗ xe có tích hợp AI trong thực tế”**

### Loại dự án

Dự án phần mềm có tích hợp AI.

### Mục tiêu chính

Xây dựng hệ thống hỗ trợ:

* Quản lý phương tiện.
* Quản lý lượt gửi xe.
* Quản lý xe vào/ra.
* Quản lý vị trí/chỗ đỗ.
* Quản lý giá gửi xe.
* Thanh toán.
* Tra cứu lịch sử.
* Báo cáo/thống kê.
* Tích hợp chức năng AI phù hợp với bài toán thực tế.

### Đặc điểm AI

AI có thể được sử dụng cho một hoặc một số bài toán phù hợp, chẳng hạn:

* Nhận diện biển số xe.
* Nhận dạng phương tiện từ hình ảnh.
* Nhận diện trạng thái chỗ đỗ.
* Phát hiện bất thường.
* Phân tích/dự đoán dữ liệu vận hành.

**Không được mặc định tất cả các chức năng trên đều nằm trong phạm vi dự án.**

Nếu chưa có thông tin chính xác về chức năng AI, phải đánh dấu là:

> **“Cần xác định thêm trong quá trình phân tích yêu cầu.”**

---

# 4. Các mô hình phải xem xét

Bắt buộc xem xét tối thiểu các mô hình:

1. **Waterfall**
2. **V-Model**
3. **Incremental Model**
4. **Prototyping Model**
5. **Spiral Model**
6. **Agile**
7. **Scrum**
8. **Kanban**

Có thể bổ sung mô hình khác nếu thực sự phù hợp.

---

# 5. Tiêu chí đánh giá

Không được đánh giá chỉ dựa vào định nghĩa lý thuyết.

Hãy xây dựng **Decision Matrix** với tối thiểu các tiêu chí:

| Tiêu chí                                 | Trọng số |
| ---------------------------------------- | -------: |
| Phù hợp với quy mô dự án sinh viên       |      15% |
| Phù hợp với thời gian thực hiện          |      15% |
| Khả năng thích nghi với thay đổi yêu cầu |      15% |
| Phù hợp với dự án có AI                  |      20% |
| Khả năng phát triển prototype/MVP        |      10% |
| Khả năng kiểm thử và đánh giá AI         |      10% |
| Dễ quản lý và theo dõi tiến độ           |       5% |
| Dễ trình bày trong báo cáo/bảo vệ        |       5% |
| **Tổng**                                 | **100%** |

Nếu cho rằng trọng số trên chưa hợp lý, hãy giải thích và điều chỉnh trước khi chấm điểm.

---

# 6. Phân tích đặc thù của dự án AI

Đây là yêu cầu bắt buộc.

Không được coi dự án:

> **Phần mềm quản lý bãi xe + AI**

giống hoàn toàn một dự án CRUD thông thường.

Hãy phân tích các đặc điểm:

### 6.1. Yêu cầu AI có thể thay đổi

Ví dụ:

* Thay đổi mô hình.
* Thay đổi dataset.
* Thay đổi preprocessing.
* Điều chỉnh threshold.
* Điều chỉnh cách đánh giá.

### 6.2. Kết quả AI không hoàn toàn xác định

Ví dụ:

> Cùng một loại hình ảnh nhưng điều kiện ánh sáng/góc chụp khác nhau có thể ảnh hưởng đến kết quả nhận diện.

### 6.3. Cần Prototype

Do đây là đồ án sinh viên, AI có thể cần được xây dựng ở mức:

> **Prototype / Proof of Concept**

thay vì sản phẩm thương mại hoàn chỉnh.

### 6.4. Cần đánh giá mô hình

Xác định:

* Dataset.
* Training.
* Validation.
* Testing.
* Evaluation.
* Điều chỉnh mô hình.

### 6.5. Có sự tương tác giữa Software và AI

Ví dụ:

**Camera/Image → AI Model → Kết quả nhận diện → Backend → Database → Giao diện quản lý**

Mô hình phát triển được lựa chọn phải hỗ trợ tốt sự phối hợp giữa các phần này.

---

# 7. Phân tích từng mô hình

Với MỖI mô hình, trình bày:

## Tên mô hình

### Nguyên lý hoạt động

Giải thích ngắn gọn.

### Ưu điểm

Đặc biệt xét trong dự án này.

### Nhược điểm

Đặc biệt xét trong dự án này.

### Mức độ phù hợp với dự án AI

Phân tích:

* Dataset.
* Prototype.
* Model iteration.
* AI evaluation.
* Software integration.

### Mức độ phù hợp với sinh viên

Đánh giá:

* Độ khó.
* Khả năng quản lý.
* Tài liệu.
* Thời gian.

### Điểm phù hợp

Chấm theo thang:

**1–5**

Trong đó:

* 1 = Rất không phù hợp.
* 2 = Không phù hợp.
* 3 = Có thể phù hợp.
* 4 = Phù hợp.
* 5 = Rất phù hợp.

---

# 8. So sánh các mô hình

Tạo bảng:

| Mô hình     | Linh hoạt | AI | Prototype | Kiểm thử | Quản lý tiến độ | Sinh viên | Tổng điểm |
| ----------- | --------: | -: | --------: | -------: | --------------: | --------: | --------: |
| Waterfall   |           |    |           |          |                 |           |           |
| V-Model     |           |    |           |          |                 |           |           |
| Incremental |           |    |           |          |                 |           |           |
| Prototype   |           |    |           |          |                 |           |           |
| Spiral      |           |    |           |          |                 |           |           |
| Agile       |           |    |           |          |                 |           |           |
| Scrum       |           |    |           |          |                 |           |           |
| Kanban      |           |    |           |          |                 |           |           |

Tính điểm theo trọng số.

Không được chấm điểm tùy tiện.

Mỗi điểm số phải có lý do.

---

# 9. Phân biệt Agile và Scrum

Đây là yêu cầu quan trọng.

Nếu kết quả cho rằng Scrum phù hợp, phải giải thích:

> **Agile là một triết lý/tập hợp nguyên tắc phát triển phần mềm, còn Scrum là một framework triển khai theo Agile.**

Không được trình bày:

> “Agile và Scrum là hai mô hình hoàn toàn độc lập giống Waterfall.”

Phải làm rõ:

**Agile → Scrum là một framework cụ thể để áp dụng các nguyên tắc Agile.**

---

# 10. Xác định mô hình phù hợp nhất

Sau khi chấm điểm, lựa chọn:

> **01 mô hình phát triển phần mềm phù hợp nhất.**

Không lựa chọn dựa trên việc:

> “Agile phổ biến.”

Mà phải dựa trên:

**Đặc điểm dự án → Tiêu chí → Điểm số → Trade-off → Kết luận.**

---

# 11. Phân tích lý do lựa chọn

Viết thành lập luận:

> Với đặc điểm của dự án..., mô hình ... được lựa chọn vì...

Phải trả lời tối thiểu:

1. Vì sao phù hợp với dự án sinh viên?
2. Vì sao phù hợp với thời gian giới hạn?
3. Vì sao phù hợp với yêu cầu có thể thay đổi?
4. Vì sao phù hợp với việc phát triển AI?
5. Vì sao phù hợp với việc xây dựng prototype?
6. Vì sao phù hợp với kiểm thử/đánh giá AI?
7. Vì sao phù hợp với khả năng quản lý của nhóm?

---

# 12. Phân tích các phương án bị loại

Không được chỉ nói:

> “Waterfall không phù hợp.”

Hãy lập bảng:

| Mô hình   | Lý do không được chọn                                             | Mức độ ảnh hưởng |
| --------- | ----------------------------------------------------------------- | ---------------- |
| Waterfall | Khó thích nghi khi yêu cầu AI thay đổi                            | Cao              |
| V-Model   | Quy trình tương đối cứng, không tối ưu cho thử nghiệm AI liên tục | ...              |
| Spiral    | Quản lý rủi ro mạnh nhưng có thể quá phức tạp với đồ án sinh viên | ...              |
| ...       | ...                                                               | ...              |

Lý do phải dựa trên **bối cảnh của dự án**, không chỉ dựa vào lý thuyết.

---

# 13. Thiết kế quy trình phát triển sau khi chọn mô hình

Sau khi lựa chọn mô hình, hãy chuyển mô hình lý thuyết thành **quy trình áp dụng thực tế cho dự án**.

Ví dụ nếu lựa chọn Agile/Scrum, hãy đề xuất:

### Sprint 0

* Khảo sát hiện trạng.
* Xác định vấn đề.
* Xác định stakeholder.
* Xác định phạm vi.
* Xác định AI Use Case.

### Sprint 1

* Requirements.
* Use Case.
* Database.
* Architecture.

### Sprint 2

* Backend.
* Database.
* Các chức năng quản lý cơ bản.

### Sprint 3

* AI Prototype.
* Dataset.
* Training.
* Evaluation.

### Sprint 4

* Tích hợp AI với hệ thống.
* Kiểm thử.

### Sprint 5

* Hoàn thiện.
* Đánh giá.
* Demo.
* Báo cáo.

**Không bắt buộc sử dụng đúng số Sprint trên.**

Hãy điều chỉnh theo thời gian thực tế của dự án.

---

# 14. Phân biệt Software Development và AI Development

Nếu lựa chọn Agile/Scrum hoặc Incremental, phải mô tả rõ:

### Nhánh phát triển phần mềm

**Requirement → Design → Development → Testing → Integration**

### Nhánh phát triển AI

**Data → Preprocessing → Training → Evaluation → Improvement**

Sau đó:

**AI Model → Integration → System Testing → Evaluation**

Phân tích cách hai chu trình phối hợp với nhau.

---

# 15. Đề xuất cách quản lý Product Backlog

Nếu mô hình được lựa chọn có sử dụng backlog, hãy phân loại:

### Epic 1 – Quản lý hệ thống

### Epic 2 – Quản lý phương tiện

### Epic 3 – Quản lý lượt gửi

### Epic 4 – Quản lý chỗ đỗ

### Epic 5 – Thanh toán

### Epic 6 – Báo cáo/thống kê

### Epic 7 – AI

### Epic 8 – Tích hợp và kiểm thử

Với Epic AI, có thể chia:

* Dataset.
* Data preprocessing.
* Model selection.
* Training.
* Evaluation.
* Model improvement.
* Integration.

---

# 16. Xác định rủi ro của mô hình được chọn

Phân tích:

| Rủi ro                            | Khả năng | Tác động | Biện pháp |
| --------------------------------- | -------- | -------- | --------- |
| Thay đổi yêu cầu                  |          |          |           |
| Thiếu dữ liệu AI                  |          |          |           |
| Model không đạt kết quả mong muốn |          |          |           |
| Chậm tiến độ                      |          |          |           |
| Khó tích hợp AI                   |          |          |           |
| Thành viên thiếu kinh nghiệm      |          |          |           |
| Phạm vi mở rộng quá mức           |          |          |           |

---

# 17. Kiểm tra tính phù hợp với môn “Ứng dụng trí tuệ nhân tạo”

Sau khi lựa chọn mô hình, hãy trả lời:

> **Mô hình phát triển này có giúp thể hiện đúng bản chất của một dự án ứng dụng AI hay không?**

Phân tích:

* Có thời gian cho thử nghiệm AI không?
* Có vòng lặp đánh giá model không?
* Có thể thay đổi dataset/model không?
* Có thể tích hợp AI từng phần không?
* Có thể trình bày quá trình phát triển AI trong báo cáo không?

---

# 18. Kết quả đầu ra

Hãy trả kết quả theo cấu trúc báo cáo:

# 1. Đặc điểm dự án và yêu cầu đối với mô hình phát triển

# 2. Các mô hình phát triển được xem xét

# 3. Tiêu chí đánh giá

# 4. Phân tích từng mô hình

# 5. Ma trận quyết định

# 6. Kết quả so sánh

# 7. Mô hình được lựa chọn

# 8. Lý do lựa chọn

# 9. Các mô hình không được lựa chọn và lý do

# 10. Quy trình áp dụng mô hình vào dự án

# 11. Cách phối hợp Software Development và AI Development

# 12. Rủi ro và biện pháp kiểm soát

# 13. Kết luận

---

# 19. Yêu cầu về văn phong báo cáo

Viết theo phong cách:

* Học thuật.
* Có lập luận.
* Có phân tích trade-off.
* Không quảng cáo công nghệ.
* Không tuyệt đối hóa AI.
* Không dùng thuật ngữ khi chưa giải thích.
* Phù hợp với báo cáo sinh viên.

Đặc biệt tránh:

> “Scrum là mô hình tốt nhất.”

Thay bằng:

> “Dựa trên các tiêu chí đánh giá và đặc điểm của dự án, Scrum được lựa chọn vì...”

---

# 20. Quy tắc cuối cùng

**KHÔNG được chọn mô hình trước khi phân tích.**

Thực hiện theo quy trình:

> **Project Context**
>
> ↓
>
> **Project Characteristics**
>
> ↓
>
> **Selection Criteria**
>
> ↓
>
> **Compare Models**
>
> ↓
>
> **Decision Matrix**
>
> ↓
>
> **Trade-off Analysis**
>
> ↓
>
> **Select Model**
>
> ↓
>
> **Adapt Model to Project**
>
> ↓
>
> **Document Decision**

Nếu kết quả cho thấy **một mô hình kết hợp** phù hợp hơn, ví dụ kết hợp Agile/Scrum với một số hoạt động Prototype hoặc Incremental, hãy nêu rõ:

1. Mô hình/framework chính là gì.
2. Thành phần nào được bổ sung.
3. Vì sao cần bổ sung.
4. Phần nào thuộc quy trình chính và phần nào là kỹ thuật hỗ trợ.

Không được gọi một cách tùy tiện là “mô hình lai” nếu chưa giải thích rõ cấu trúc.

Cuối cùng, hãy đưa ra một **kết luận ngắn gọn 1–2 đoạn** có thể đưa trực tiếp vào báo cáo với tiêu đề:

> **“Lựa chọn mô hình phát triển phần mềm”**

Kết luận phải nêu rõ:

**Mô hình được chọn + lý do chính + cách áp dụng cho dự án + lợi ích đối với phần AI.**

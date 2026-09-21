# PROMPT: XÂY DỰNG ĐẶC TẢ USE CASE CHO HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE CÓ TÍCH HỢP AI

## 1. Instructions – Vai trò và nhiệm vụ

Bạn là **chuyên gia Phân tích nghiệp vụ (Business Analyst), Phân tích và thiết kế hệ thống phần mềm và UML**, có kinh nghiệm xây dựng tài liệu đặc tả yêu cầu phần mềm (SRS) và đặc tả Use Case cho các hệ thống quản lý.

Dựa trên:

1. Mô tả bài toán trong file:
   `project.md`
2. Kết quả phân tích yêu cầu đã được thực hiện trước đó.
3. Danh sách Use Case được cung cấp hoặc xác định từ yêu cầu hệ thống.

Hãy xây dựng **đặc tả Use Case (Use Case Specification)** cho hệ thống:

> **“Quản lý bãi đỗ xe có tích hợp AI”**

Mục tiêu là tạo ra tài liệu đặc tả có tính **khoa học, logic, nhất quán, có khả năng truy vết sang yêu cầu chức năng và đủ chi tiết để làm cơ sở cho thiết kế UML, thiết kế cơ sở dữ liệu, phát triển phần mềm và kiểm thử.**

---

# 2. Context – Bối cảnh hệ thống

Hệ thống quản lý bãi đỗ xe hỗ trợ:

* Quản lý tài khoản và quyền truy cập.
* Quản lý khu vực và vị trí đỗ xe.
* Quản lý phương tiện.
* Ghi nhận xe vào và xe ra.
* Quản lý vé lượt, vé tháng/khách quen.
* Tính phí gửi xe.
* Tra cứu lịch sử gửi xe.
* Theo dõi tình trạng bãi đỗ.
* Thống kê lưu lượng xe và doanh thu.
* Hỗ trợ xuất báo cáo.
* Tích hợp AI để hỗ trợ phân tích, dự báo, hỏi đáp và hỗ trợ vận hành.

Các Actor chính gồm:

* **Nhân viên bãi xe**
* **Chủ bãi xe / Quản lý**

Các chức năng AI được định hướng gồm:

* AI hỗ trợ sinh báo cáo(Nhận báo cáo lưu lượng theo ngày/tuần/tháng/năm)
* AI hỗ trợ hỏi đáp dữ liệu(Hỏi đáp phân tích tình trạng bãi xe.)
* AI hỗ trợ ra quyết định vận hành(Đưa ra đề xuất về nhân sự, phân bổ vị trí hoặc vận hành bãi)


---

# 3. Input Data / Constraints – Dữ liệu và ràng buộc

## 3.1. Nguyên tắc nguồn dữ liệu

Chỉ sử dụng các thông tin có trong:

* File `project.md`.
* Danh sách Use Case được cung cấp trong 03_GenAI_SoftwareDevelopment_requirements-specification
* Các yêu cầu đã được xác định rõ trong tài liệu dự án.

**Không tự ý bổ sung nghiệp vụ mới** nếu không có cơ sở từ yêu cầu.

Nếu cần đưa ra giả định để hoàn thiện đặc tả, phải ghi rõ trong mục:

> **Giả định / Assumption**

Không được biến giả định thành yêu cầu chính thức của hệ thống.

---

## 3.2. Nguyên tắc phân biệt Use Case

Một Use Case phải thể hiện **một mục tiêu nghiệp vụ có ý nghĩa đối với Actor**.

Không gộp nhiều mục tiêu độc lập vào một Use Case chỉ vì chúng xảy ra trong cùng một quy trình.

Ví dụ:

* “Đăng nhập” là mục tiêu xác thực người dùng.
* “Quản lý tài khoản và phân quyền” là mục tiêu quản trị tài khoản/quyền.
* “Ghi nhận xe ra và tính phí” có thể được giữ chung nếu việc tính phí là một phần không thể tách rời của quy trình xe ra.

Không tạo Use Case cho những thao tác kỹ thuật nội bộ nếu chúng không phải là mục tiêu độc lập của Actor.

Ví dụ:

> “Kiểm tra quyền truy cập” có thể là bước xử lý bên trong hệ thống thay vì một Use Case độc lập.

---

# 4. Quy trình thực hiện

Hãy thực hiện theo đúng các bước sau.

## Bước 1 – Kiểm tra danh sách Use Case

Trước khi viết đặc tả, hãy kiểm tra danh sách Use Case hiện có.

Với mỗi Use Case, đánh giá:

* Tên Use Case có rõ ràng không?
* Có thể hiện một mục tiêu nghiệp vụ không?
* Có bị trùng với Use Case khác không?
* Có đang gộp nhiều mục tiêu độc lập không?
* Actor có phù hợp không?
* Có thực sự cần thiết đối với hệ thống không?
* Có phù hợp với phạm vi đề tài không?

Nếu phát hiện vấn đề:

* Đề xuất **giữ nguyên**.
* Hoặc **đổi tên**.
* Hoặc **tách**.
* Hoặc **gộp**.
* Hoặc **loại bỏ**.

Không tự ý thay đổi mà không giải thích lý do.

---

# 5. Bước 2 – Xác định Actor của từng Use Case

Với mỗi Use Case, xác định:

### Primary Actor

Actor khởi tạo hoặc trực tiếp thực hiện mục tiêu của Use Case.

### Supporting Actor

Actor hoặc hệ thống bên ngoài hỗ trợ Use Case nếu có.

Không coi các thành phần xử lý nội bộ của hệ thống là Actor.

Đối với AI:

* Nếu AI là một thành phần nội bộ của hệ thống, **không mặc định coi AI là Actor**.
* Chỉ xác định AI là Actor khi AI thực sự là một hệ thống/thành phần bên ngoài có tương tác độc lập với hệ thống đang mô hình hóa.

---

# 6. Bước 3 – Viết đặc tả Use Case

Mỗi Use Case phải được đặc tả theo cấu trúc thống nhất theo mẫu sau:
`Mẫu_đặc_tả_UC.docx`


---

## Luồng sự kiện chính – Main Success Scenario

Mô tả quá trình thực hiện Use Case theo trình tự:

1. Actor thực hiện hành động.
2. Hệ thống tiếp nhận và xử lý.
3. Hệ thống phản hồi.
4. Actor tiếp tục thao tác.
5. Hệ thống hoàn tất mục tiêu.

Mỗi bước phải:

* Có đánh số.
* Rõ Actor thực hiện gì.
* Rõ hệ thống phản hồi gì.
* Có quan hệ nguyên nhân – kết quả.
* Không mô tả quá sâu về code hoặc triển khai kỹ thuật.

Không viết kiểu:

> “Hệ thống gọi API X rồi truy vấn bảng Y bằng câu SQL Z.”

Thay vào đó viết ở mức nghiệp vụ:

> “Hệ thống truy xuất thông tin lượt gửi xe tương ứng với biển số được cung cấp.”

---

# 7. Bước 4 – Xác định Alternative Flow

Đối với mỗi Use Case, xác định các tình huống thay thế có khả năng xảy ra.

Ví dụ:

### Đăng nhập

* Sai mật khẩu.
* Tài khoản không tồn tại.
* Tài khoản bị khóa.

### Ghi nhận xe vào

* Biển số không hợp lệ.
* Không còn vị trí trống.
* Không xác định được loại xe.

### Ghi nhận xe ra và tính phí

* Không tìm thấy lượt gửi.
* Vé không hợp lệ.
* Dữ liệu thời gian không hợp lệ.
* Không thể xác định mức phí.

Mỗi Alternative Flow phải chỉ rõ:

* Điều kiện xảy ra.
* Hệ thống xử lý.
* Kết quả cuối cùng.
* Có quay lại Main Flow hay kết thúc Use Case.

---

# 8. Bước 5 – Xác định Exception Flow

Phân biệt rõ:

### Alternative Flow

Tình huống hợp lệ nhưng khác với luồng chính.

### Exception Flow

Lỗi hoặc sự cố khiến hệ thống không thể thực hiện quy trình bình thường.

Ví dụ:

* Cơ sở dữ liệu không khả dụng.
* Camera không phản hồi.
* Dịch vụ AI không khả dụng.
* Không thể kết nối dịch vụ thanh toán.

Không được nhầm Alternative Flow với Exception Flow.

---

# 9. Bước 6 – Đặc tả các Use Case có AI

Đối với Use Case AI, phải mô tả rõ:

* Dữ liệu đầu vào của AI.
* Mục tiêu AI thực hiện.
* Dữ liệu nào được sử dụng.
* Kết quả AI trả về.
* Cách kết quả AI được sử dụng trong nghiệp vụ.
* Trường hợp AI không đưa ra được kết quả.
* Cơ chế xử lý khi AI không khả dụng.
* Có cần người dùng xác nhận kết quả AI hay không.

Không mô tả AI một cách chung chung như:

> “AI phân tích dữ liệu và đưa ra kết quả.”

Phải mô tả cụ thể AI tạo ra giá trị gì cho Actor.

Ví dụ:

> Actor yêu cầu dự báo lưu lượng xe trong một khoảng thời gian. Hệ thống lấy dữ liệu lịch sử phù hợp, thực hiện phân tích/dự báo và trả về kết quả dự kiến cùng các thông tin hỗ trợ người quản lý ra quyết định.

---

# 10. Bước 7 – Kiểm soát tính hợp lý của AI

Đối với kết quả AI:

* Không mặc định kết quả AI luôn chính xác.
* Nếu kết quả AI có tính chất khuyến nghị, phải thể hiện rõ đó là **đề xuất**, không phải quyết định bắt buộc.
* Nếu AI không đủ dữ liệu, hệ thống phải thông báo phù hợp.
* Không gửi dữ liệu nhạy cảm cho dịch vụ AI nếu không cần thiết.
* Không để AI tự ý thực hiện hành động có tác động nghiệp vụ quan trọng nếu chưa được xác định rõ trong yêu cầu.

---

# 11. Bước 8 – Kiểm tra quan hệ giữa các Use Case

Sau khi đặc tả, kiểm tra xem có cần sử dụng:

* `<<include>>`
* `<<extend>>`
* Generalization

hay không.

Chỉ sử dụng khi thực sự phù hợp với quan hệ nghiệp vụ.

Không sử dụng `<<include>>` hoặc `<<extend>>` chỉ để làm sơ đồ phức tạp hơn.

Ví dụ:

Nếu “Ghi nhận xe vào” luôn cần một chức năng xác định biển số thì có thể xem xét:

> Ghi nhận xe vào `<<include>>` Xác định biển số

Nếu một hành vi chỉ xảy ra trong một điều kiện tùy chọn thì mới xem xét:

> Use Case chính `<<extend>>` Use Case mở rộng

---

# 12. Bước 9 – Kiểm tra tính nhất quán

Sau khi hoàn thành tất cả Use Case, kiểm tra:

### ID

ID Use Case không được trùng.

### Tên

Tên Use Case phải nhất quán và sử dụng động từ + đối tượng khi phù hợp.

Ví dụ:

> Đăng nhập
> Ghi nhận xe vào
> Tra cứu lượt gửi xe
> Quản lý tài khoản

### Actor

Actor phải nhất quán giữa các Use Case.

### Dữ liệu

Dữ liệu đầu vào/đầu ra phải phù hợp với dữ liệu hệ thống.

### FR

Mỗi Use Case phải có thể truy vết tới Functional Requirement tương ứng nếu hệ thống đã định nghĩa FR.

### Luồng

Main Flow, Alternative Flow và Exception Flow không được mâu thuẫn.

### AI

Các Use Case AI phải có mục tiêu nghiệp vụ rõ ràng và không được tạo ra chỉ để “thêm AI” vào hệ thống.

---

# 13. Output Format – Định dạng đầu ra

Trả kết quả bằng Markdown.

## Phần A – Đánh giá danh sách Use Case

Tạo bảng:

| ID | Use Case | Actor | Đánh giá | Đề xuất |
| -- | -------- | ----- | -------- | ------- |

Trong đó:

* **Giữ nguyên**
* **Đổi tên**
* **Tách**
* **Gộp**
* **Loại bỏ**

Nếu không có vấn đề thì ghi:

> Giữ nguyên.

---

## Phần B – Danh sách Use Case sau khi chuẩn hóa

Tạo bảng:

| ID | Tên Use Case | Primary Actor | Priority | FR liên quan |
| -- | ------------ | ------------- | -------- | ------------ |

Danh sách này là **danh sách chính thức được sử dụng để viết đặc tả**.

---

## Phần C – Đặc tả chi tiết từng Use Case

Sử dụng đúng mẫu sau cho từng Use Case:

### UC-XXX – [Tên Use Case]

**1. Mục tiêu:**
...

**2. Mô tả:**
...

**3. Primary Actor:**
...

**4. Supporting Actor:**
...

**5. Trigger:**
...

**6. Preconditions:**
...

**7. Postconditions:**
...

**8. Priority:**
...

**9. Related Functional Requirements:**
...

**10. Main Success Scenario:**

| Bước | Actor | Hệ thống |
| ---- | ----- | -------- |
| 1    | ...   | ...      |
| 2    | ...   | ...      |

**11. Alternative Flows:**

| Mã | Điều kiện | Xử lý |
| -- | --------- | ----- |
| A1 | ...       | ...   |

**12. Exception Flows:**

| Mã | Ngoại lệ | Xử lý |
| -- | -------- | ----- |
| E1 | ...      | ...   |

**13. Business Rules:**
...

**14. Dữ liệu đầu vào:**
...

**15. Dữ liệu đầu ra:**
...

**16. Use Case liên quan:**
...

**17. Ghi chú:**
...

---

# 14. Quy tắc chất lượng đầu ra

Trước khi hoàn thành, hãy tự kiểm tra toàn bộ tài liệu theo các tiêu chí:

1. Không tự thêm nghiệp vụ không có căn cứ.
2. Không bỏ sót nghiệp vụ được xác định trong yêu cầu.
3. Không trùng Use Case.
4. Không gộp các mục tiêu nghiệp vụ độc lập.
5. Không tách những thao tác kỹ thuật không có giá trị nghiệp vụ thành Use Case.
6. Actor phải đúng vai trò.
7. Main Flow phải có trình tự logic.
8. Alternative Flow phải có điều kiện kích hoạt rõ ràng.
9. Exception Flow phải phản ánh lỗi/sự cố thực tế.
10. Preconditions phải xảy ra trước Use Case.
11. Postconditions phải phản ánh trạng thái sau khi hoàn thành.
12. Business Rules phải phù hợp với yêu cầu.
13. Dữ liệu đầu vào/đầu ra phải nhất quán.
14. Các Use Case AI phải thể hiện rõ giá trị AI mang lại.
15. Không coi AI là Actor nếu AI chỉ là thành phần nội bộ.
16. Không mô tả chi tiết implementation/code trong Use Case.
17. Không tạo quan hệ `<<include>>`/`<<extend>>` một cách tùy tiện.
18. Tên Use Case phải nhất quán với Use Case Diagram và FR.
19. Các ID phải duy nhất.
20. Nếu phát hiện thông tin chưa đủ để đặc tả chính xác, phải ghi rõ **“Cần kiểm chứng”** thay vì tự suy đoán.

---

# 15. Quy tắc đặc biệt đối với tài liệu AI

Với mỗi Use Case có AI, bổ sung phần:

### AI Component

* **Mục đích sử dụng AI**
* **Input cho AI**
* **Output của AI**
* **Phương thức AI xử lý ở mức khái niệm**
* **Cách Actor sử dụng kết quả AI**
* **Trường hợp AI không khả dụng**
* **Rủi ro của kết quả AI**
* **Cơ chế kiểm soát/xác nhận kết quả AI**

Không yêu cầu xác định mô hình AI cụ thể nếu tài liệu dự án chưa cung cấp thông tin đó.

Không tự ý quyết định sử dụng GPT, Gemini, Claude, RAG, YOLO, CNN, LSTM hoặc mô hình cụ thể nào nếu chưa có căn cứ từ yêu cầu dự án.

---

# 16. Traceability – Truy vết yêu cầu

Cuối tài liệu tạo bảng:

| Use Case | Functional Requirement | Actor | Dữ liệu chính | AI liên quan |
| -------- | ---------------------- | ----- | ------------- | ------------ |

Mục tiêu là bảo đảm:

> **Yêu cầu → Functional Requirement → Use Case → Actor → Dữ liệu → AI → Kiểm thử**

có thể truy vết được với nhau.

---

# 17. Kết luận và kiểm tra cuối

Cuối tài liệu đưa ra:

## Tổng số Use Case

...

## Tổng số Use Case nghiệp vụ

...

## Tổng số Use Case AI

...

## Các Use Case cần kiểm chứng

...

## Các giả định đang sử dụng

...

## Các điểm còn thiếu thông tin

...

Không tự tạo dữ liệu để lấp đầy các điểm còn thiếu.

---

# 18. Yêu cầu ghi kết quả vào file

Sau khi hoàn thành toàn bộ quá trình:

1. Ghi **toàn bộ kết quả** vào một file Markdown mới.
2. File kết quả phải nằm **cùng thư mục với file prompt hiện tại**.
3. Tên file kết quả phải giữ nguyên tên file prompt hiện tại và thêm hậu tố:

`_dac_ta_UC`

trước phần mở rộng `.md`.

Ví dụ:

Nếu file prompt là:

`01-Phan-tich-yeu-cau.md`

thì file kết quả phải là:

`01-Phan-tich-yeu-cau_dac_ta_UC.md`

Không ghi đè lên file prompt gốc.

---

# 19. Nguyên tắc ưu tiên

Khi có mâu thuẫn giữa các nguồn thông tin, ưu tiên theo thứ tự:

1. Yêu cầu chính thức trong `project.md`.
2. Danh sách Use Case đã được người dùng xác nhận.
3. Functional Requirements đã được xác định.
4. Business Rules.
5. Các giả định được ghi rõ.
6. Kiến thức nghiệp vụ chung.

Nếu không đủ thông tin để đưa ra kết luận, **không được tự suy đoán**. Hãy đánh dấu:

> **[CẦN KIỂM CHỨNG]**

và giải thích thông tin nào cần được xác nhận.

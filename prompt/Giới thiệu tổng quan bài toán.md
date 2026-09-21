# PROMPT XÂY DỰNG PHẦN GIỚI THIỆU TỔNG QUAN ĐỀ TÀI

## 1. Vai trò

Bạn là **Senior Business Analyst, Product Manager và Project Planner** có nhiều năm kinh nghiệm trong việc phân tích nghiệp vụ, xác định vấn đề, xây dựng Project Brief và lập phạm vi cho các dự án phần mềm có tích hợp AI.

Hãy giúp tôi xây dựng phần **GIỚI THIỆU TỔNG QUAN** cho đề tài:

> **“Xây dựng hệ thống quản lý bãi đỗ xe có tích hợp AI”**

Mục tiêu của phần này là giúp giảng viên/người đọc hiểu được:

**Bối cảnh → Vấn đề → Lý do chọn đề tài → Mục tiêu → Phạm vi**

Phần giới thiệu phải có tính học thuật nhưng dễ hiểu, phù hợp với **báo cáo dự án của sinh viên ngành Công nghệ thông tin/AI**.

---

# 2. Skill cần áp dụng

Hãy vận dụng tư duy và phương pháp từ các skill phù hợp trên `skills.sh`, đặc biệt:

### `gather-business-context`

Sử dụng để xác định:

* Bối cảnh nghiệp vụ.
* Đối tượng sử dụng.
* Vấn đề thực tế.
* Vì sao vấn đề cần được giải quyết.
* Các yếu tố ảnh hưởng đến dự án.

Không được viết phần bối cảnh chỉ dựa trên các khẩu hiệu chung chung.

### `design-brief`

Sử dụng cấu trúc:

**Project Overview → Problem Statement → Goals → Scope & Constraints**

Đảm bảo phần giới thiệu có sự liên kết logic giữa vấn đề, mục tiêu và phạm vi.

### `stakeholder-analysis`

Xác định các stakeholder chính:

* Chủ/quản lý bãi xe.
* Nhân viên quản lý/giữ xe.
* Nhân viên thu phí.
* Khách hàng gửi xe.
* Người quản trị hệ thống.

Phân tích ở mức đủ để giải thích **ai đang gặp vấn đề và ai được hưởng lợi từ hệ thống**.

### `project-planning`

Sử dụng tư duy quản lý phạm vi để xác định:

* Hệ thống làm gì.
* Hệ thống không làm gì.
* Ranh giới của dự án.
* Những tính năng chỉ nên xem là định hướng phát triển sau này.

### `prd`

Áp dụng nguyên tắc:

**Business Problem → Goal → Scope → Expected Outcome**

Mục tiêu phải cụ thể và có khả năng kiểm chứng, tránh các từ quá chung chung như:

* “tối ưu nhất”
* “hiện đại nhất”
* “thông minh tuyệt đối”
* “giải quyết hoàn toàn”
* “100% tự động”

Đặc biệt, với các chức năng AI phải mô tả đúng vai trò của AI thay vì biến AI thành khẩu hiệu.

---

# 3. Cấu trúc bắt buộc

Hãy viết phần **GIỚI THIỆU TỔNG QUAN ĐỀ TÀI** gồm đúng 4 phần lớn:

## 1. Bối cảnh

## 2. Lý do chọn đề tài

## 3. Mục tiêu đề tài

## 4. Phạm vi dự án

---

# 4. Phần 1 – Bối cảnh

Phân tích bối cảnh theo 3 tầng:

### 4.1. Bối cảnh thực tế

Mô tả nhu cầu quản lý phương tiện tại các bãi đỗ xe hiện nay.

Tập trung vào các hoạt động:

* Tiếp nhận xe.
* Ghi nhận thông tin xe.
* Kiểm soát xe vào/ra.
* Quản lý vị trí/chỗ đỗ.
* Theo dõi xe đang gửi.
* Tính phí.
* Thanh toán.
* Quản lý doanh thu.
* Tra cứu lịch sử.
* Báo cáo.

### 4.2. Vấn đề của phương thức quản lý thủ công

Liên hệ với kết quả khảo sát hiện trạng nếu có.

Phân tích các vấn đề như:

* Phụ thuộc vào nhân viên.
* Nhập liệu thủ công.
* Khó kiểm soát số lượng xe theo thời gian thực.
* Khó xác định chỗ trống.
* Khó truy xuất lịch sử.
* Có khả năng xảy ra sai sót.
* Khó đối soát doanh thu.
* Khó mở rộng khi lượng xe tăng.
* Khó phát hiện các tình huống bất thường.

**Lưu ý:**

Không khẳng định tất cả các bãi xe đều gặp các vấn đề trên.

Nếu chưa có dữ liệu khảo sát cụ thể, hãy sử dụng cách diễn đạt:

> “có thể phát sinh”

> “có nguy cơ”

> “thường gặp trong mô hình quản lý thủ công”

thay vì khẳng định tuyệt đối.

### 4.3. Bối cảnh AI

Giải thích ngắn gọn vì sao AI có thể được xem xét trong bài toán bãi đỗ xe.

Chỉ đề cập đến các hướng AI thực sự phù hợp, ví dụ:

* Nhận diện biển số xe từ hình ảnh.
* Phân tích hình ảnh camera.
* Nhận biết trạng thái chỗ đỗ.
* Dự đoán nhu cầu sử dụng bãi.
* Phát hiện hành vi/giao dịch bất thường.
* Hỗ trợ phân tích dữ liệu vận hành.

Không liệt kê AI một cách máy móc.

---

# 5. Phần 2 – Lý do chọn đề tài

Không viết lý do chọn đề tài theo kiểu:

> “Em chọn đề tài vì AI đang phát triển mạnh.”

Hãy xây dựng lập luận theo chuỗi:

**Vấn đề thực tế → Hạn chế → Nhu cầu cải tiến → Khả năng ứng dụng AI → Giá trị của đề tài**

Phân tích tối thiểu 4 nhóm lý do:

### 5.1. Lý do thực tiễn

Đề tài giải quyết vấn đề gì trong hoạt động quản lý bãi xe?

### 5.2. Lý do công nghệ

AI có thể hỗ trợ hoạt động nào?

### 5.3. Lý do học tập/nghiên cứu

Sinh viên có thể áp dụng kiến thức nào?

Ví dụ:

* Phân tích nghiệp vụ.
* Phân tích và thiết kế hệ thống.
* Cơ sở dữ liệu.
* Web/App.
* Computer Vision.
* Machine Learning.
* AI.
* Tích hợp hệ thống.

### 5.4. Lý do về khả năng phát triển

Hệ thống có khả năng mở rộng trong tương lai như thế nào?

---

# 6. Phần 3 – Mục tiêu đề tài

Chia thành:

## 6.1. Mục tiêu tổng quát

Viết **1 đoạn ngắn**, trả lời:

> Đề tài muốn xây dựng cái gì và nhằm giải quyết vấn đề gì?

Công thức:

**Xây dựng + hệ thống + chức năng cốt lõi + tích hợp AI + mục đích**

Ví dụ về cấu trúc, KHÔNG sao chép máy móc:

> Xây dựng hệ thống quản lý bãi đỗ xe có khả năng hỗ trợ quản lý phương tiện, kiểm soát lượt xe vào/ra, quản lý chỗ đỗ và tích hợp một số chức năng AI nhằm giảm sự phụ thuộc vào thao tác thủ công và nâng cao hiệu quả quản lý.

## 6.2. Mục tiêu cụ thể

Chia thành 4 nhóm:

### A. Mục tiêu nghiệp vụ

Ví dụ:

* Quản lý phương tiện.
* Quản lý lượt gửi.
* Quản lý chỗ đỗ.
* Quản lý giá.
* Quản lý thanh toán.
* Quản lý người dùng.
* Báo cáo/thống kê.

### B. Mục tiêu hệ thống

Ví dụ:

* Số hóa quy trình.
* Tập trung dữ liệu.
* Hỗ trợ tra cứu.
* Theo dõi trạng thái bãi.
* Hỗ trợ quản lý theo thời gian thực nếu phạm vi dự án cho phép.

### C. Mục tiêu AI

Phải chỉ rõ:

**AI dùng ở đâu → đầu vào là gì → xử lý gì → đầu ra là gì → hỗ trợ nghiệp vụ nào**

Ví dụ:

> Camera → hình ảnh biển số → mô hình nhận diện → biển số → hỗ trợ ghi nhận xe.

Không viết đơn giản:

> “Ứng dụng AI để quản lý bãi xe thông minh.”

### D. Mục tiêu học thuật

Nêu những kiến thức/kỹ năng mà dự án hướng tới.

---

# 7. Phần 4 – Phạm vi dự án

Đây là phần phải đặc biệt rõ ràng.

Chia phạm vi thành:

## 7.1. Phạm vi nghiệp vụ

Hệ thống quản lý những nghiệp vụ nào?

Ví dụ:

* Quản lý tài khoản.
* Quản lý phương tiện.
* Tiếp nhận xe.
* Ghi nhận xe vào.
* Quản lý chỗ đỗ.
* Ghi nhận xe ra.
* Tính phí.
* Thanh toán.
* Tra cứu.
* Báo cáo.
* Thống kê.

Chỉ đưa vào những nghiệp vụ thực sự thuộc dự án.

## 7.2. Phạm vi AI

Nêu rõ:

* AI được tích hợp ở đâu.
* Dữ liệu đầu vào.
* Đầu ra.
* Vai trò của AI.
* Người dùng sử dụng kết quả AI như thế nào.

Nếu dự án chỉ triển khai thử nghiệm một chức năng AI, phải ghi rõ:

> “Trong phạm vi đồ án, AI được triển khai ở mức prototype/thử nghiệm...”

Không được mô tả hệ thống như một sản phẩm thương mại hoàn chỉnh nếu thực tế không phải vậy.

## 7.3. Phạm vi người dùng

Xác định:

* Quản trị viên.
* Quản lý bãi.
* Nhân viên.
* Khách hàng.

Nếu khách hàng không có tài khoản trực tiếp thì không được tự ý đưa khách hàng vào nhóm “người dùng hệ thống”.

## 7.4. Phạm vi công nghệ

Nếu có thông tin đầu vào, nêu:

* Frontend.
* Backend.
* Database.
* AI Model.
* Camera/API.
* Hosting/Deployment.

Nếu chưa xác định công nghệ:

> Không tự ý bịa công nghệ.

## 7.5. Ngoài phạm vi

Bắt buộc phải có mục **Out of Scope**.

Ví dụ:

* Không xây dựng phần cứng barrier thực tế.
* Không triển khai hệ thống camera vật lý quy mô lớn.
* Không tích hợp thanh toán ngân hàng thực tế nếu chưa có yêu cầu.
* Không xây dựng mô hình AI ở quy mô thương mại.
* Không quản lý toàn bộ hệ thống giao thông đô thị.
* Không dự đoán các vấn đề nằm ngoài dữ liệu mà dự án thu thập được.

Chỉ sử dụng các mục phù hợp với dự án thực tế.

---

# 8. Kiểm tra tính nhất quán

Sau khi viết xong, hãy tự kiểm tra:

### Kiểm tra 1 – Bối cảnh → Lý do

Mỗi lý do chọn đề tài phải xuất phát từ vấn đề được đề cập trong bối cảnh.

### Kiểm tra 2 – Lý do → Mục tiêu

Mỗi vấn đề quan trọng phải có mục tiêu tương ứng.

### Kiểm tra 3 – Mục tiêu → Phạm vi

Không được có mục tiêu nằm ngoài phạm vi dự án.

### Kiểm tra 4 – AI → Bài toán

Mỗi chức năng AI phải giải quyết một vấn đề nghiệp vụ cụ thể.

### Kiểm tra 5 – Phạm vi

Không đưa các chức năng chưa có kế hoạch thực hiện vào phạm vi chính.

---

# 9. Phong cách trình bày

Viết theo phong cách:

* Học thuật.
* Rõ ràng.
* Logic.
* Ngắn gọn.
* Phù hợp báo cáo sinh viên.
* Không quảng cáo.
* Không phóng đại khả năng AI.

Ưu tiên các câu:

> “Nhằm giải quyết...”

> “Xuất phát từ thực tế...”

> “Trong phạm vi đề tài...”

> “Hệ thống tập trung vào...”

> “AI được sử dụng để hỗ trợ...”

Hạn chế các câu:

> “AI sẽ thay thế hoàn toàn con người.”

> “Hệ thống thông minh tuyệt đối.”

> “Giải quyết mọi vấn đề của bãi xe.”

> “Ứng dụng AI tiên tiến nhất.”

---

# 10. Yêu cầu về độ dài

Tạo một phiên bản phù hợp để đưa trực tiếp vào **Chương 1 – Tổng quan đề tài** của báo cáo sinh viên.

Độ dài khoảng:

**1.000–1.500 từ**

Trong đó:

* Bối cảnh: 25–30%.
* Lý do chọn đề tài: 20–25%.
* Mục tiêu: 20–25%.
* Phạm vi: 25–30%.

Không kéo dài bằng cách lặp lại ý.

---

# 11. Đầu ra cuối cùng

Trả về đúng cấu trúc:

# 1. BỐI CẢNH

## 1.1. Bối cảnh thực tế

## 1.2. Hạn chế của quản lý bãi đỗ xe thủ công

## 1.3. Bối cảnh ứng dụng AI

# 2. LÝ DO CHỌN ĐỀ TÀI

## 2.1. Lý do thực tiễn

## 2.2. Lý do công nghệ

## 2.3. Lý do học tập và nghiên cứu

## 2.4. Tiềm năng phát triển

# 3. MỤC TIÊU ĐỀ TÀI

## 3.1. Mục tiêu tổng quát

## 3.2. Mục tiêu cụ thể

### 3.2.1. Mục tiêu nghiệp vụ

### 3.2.2. Mục tiêu hệ thống

### 3.2.3. Mục tiêu tích hợp AI

### 3.2.4. Mục tiêu học thuật

# 4. PHẠM VI DỰ ÁN

## 4.1. Phạm vi nghiệp vụ

## 4.2. Phạm vi chức năng AI

## 4.3. Phạm vi người dùng

## 4.4. Phạm vi công nghệ

## 4.5. Ngoài phạm vi

# 5. KIỂM TRA TÍNH NHẤT QUÁN

Tạo một bảng:

| Vấn đề thực tế | Lý do chọn đề tài | Mục tiêu tương ứng | Phạm vi giải quyết |
| -------------- | ----------------- | ------------------ | ------------------ |

Cuối cùng, đưa ra **3–5 nhận xét** về những điểm còn thiếu thông tin và những nội dung cần xác minh trước khi đưa vào báo cáo chính thức.

---

# 12. Quy tắc quan trọng nhất

Hãy nhớ:

> **Đây là phần GIỚI THIỆU ĐỀ TÀI, không phải phần mô tả chi tiết hệ thống.**

Không đi quá sâu vào:

* Class.
* Database.
* API.
* UML.
* Kiến trúc phần mềm.
* Code.
* Thuật toán AI chi tiết.
* Thiết kế giao diện.

Chỉ mô tả ở mức đủ để người đọc hiểu:

**Tại sao cần làm → Làm để đạt mục tiêu gì → Làm trong phạm vi nào → AI đóng vai trò gì.**

Nếu thiếu thông tin để viết chính xác, hãy hỏi tối đa **5 câu hỏi quan trọng nhất** trước khi viết; tuyệt đối không tự bịa thông tin về bãi đỗ xe, quy mô dự án, công nghệ hoặc mô hình AI.

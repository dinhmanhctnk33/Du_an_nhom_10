# Đặc tả Use Case — Hệ thống quản lý bãi đỗ xe có tích hợp AI

## Phạm vi và quy ước

Nguồn ưu tiên: `project.md`, danh sách Use Case trong `03_GenAI_SoftwareDevelopment_requirements-specification.docx`, và các yêu cầu đã được xác nhận trong tài liệu dự án. AI là thành phần nội bộ, không phải Actor.

Actor sử dụng thống nhất:

- **Nhân viên bãi xe**: thực hiện nghiệp vụ xe vào/ra và các thao tác được cấp quyền.
- **Quản lý**: quản lý dữ liệu nghiệp vụ, xem thống kê và sử dụng các chức năng AI.

`[CẦN KIỂM CHỨNG]` biểu thị nội dung chưa được `project.md` xác nhận đủ chi tiết; không phải yêu cầu chính thức.

## Phần A — Đánh giá danh sách Use Case

| ID nguồn | Use Case | Actor | Đánh giá | Đề xuất |
| -- | -- | -- | -- | -- |
| UC-001 | Đăng nhập và phân quyền | Quản lý, Nhân viên | Mục tiêu xác thực rõ; phân quyền là kết quả bắt buộc của đăng nhập. | Giữ nguyên |
| UC-002 | Quản lý đăng nhập và phân quyền | Quản lý | SRS liệt kê nhưng `project.md` chỉ xác nhận đăng nhập và phân quyền, chưa xác nhận quản trị tài khoản. | Giữ có điều kiện, ghi **[CẦN KIỂM CHỨNG]** |
| UC-003 | Quản lý khu vực đỗ xe | Quản lý | Phù hợp quản lý khu vực/vị trí/loại xe. | Giữ nguyên; tên mở rộng để phản ánh đủ phạm vi |
| UC-004 | Ghi nhận xe vào | Nhân viên | Mục tiêu nghiệp vụ độc lập, có dữ liệu xe/vé/thời gian. | Giữ nguyên |
| UC-005 | Ghi nhận xe ra và tính phí | Nhân viên | Tính phí là phần không tách rời khi xe ra. | Giữ nguyên |
| UC-006 | Theo dõi tình trạng chỗ đỗ | Quản lý, Nhân viên | Phù hợp yêu cầu theo dõi chỗ trống theo khu vực. | Giữ nguyên |
| UC-007 | Tra cứu lượt gửi xe | Quản lý, Nhân viên | Phù hợp tiêu chí tra cứu biển số/thời gian. | Giữ nguyên |
| UC-008 | Quản lý vé tháng/khách quen | Quản lý | Phù hợp phạm vi; quy tắc cụ thể chưa rõ. | Giữ nguyên, đánh dấu quy tắc **[CẦN KIỂM CHỨNG]** |
| UC-009 | Xem thống kê và báo cáo | Quản lý | Phù hợp lưu lượng, doanh thu, cao điểm. Không mặc định xuất báo cáo vì chưa có căn cứ. | Đổi tên từ “Xem thống kê và báo cáo” thành “Xem thống kê vận hành” |
| UC-010 | AI hỗ trợ sinh báo cáo | Quản lý | Phù hợp AI báo cáo lưu lượng ngày/tuần. Tháng/năm trong danh sách nguồn chưa có căn cứ từ `project.md`. | Giữ nguyên, giới hạn ngày/tuần |
| UC-011 | AI hỗ trợ hỏi đáp dữ liệu | Quản lý | Phù hợp hỏi đáp dữ liệu bãi xe. | Giữ nguyên |
| UC-0112 | AI hỗ trợ ra quyết định vận hành | Quản lý | Mã không chuẩn; gợi ý nhân sự là phạm vi đã xác nhận. Gợi ý phân bổ vị trí/vận hành khác chưa được xác nhận. | Đổi mã thành **UC-012**; giới hạn gợi ý nhân sự |

## Phần B — Danh sách Use Case sau khi chuẩn hóa

| ID | Tên Use Case | Primary Actor | Priority | FR liên quan |
| -- | -- | -- | -- | -- |
| UC-001 | Đăng nhập và phân quyền | Quản lý, Nhân viên bãi xe | Must Have | FR-001 |
| UC-002 | Quản lý tài khoản và phân quyền | Quản lý | TBD | [CẦN KIỂM CHỨNG] |
| UC-003 | Quản lý khu vực, vị trí đỗ và loại xe | Quản lý | Must Have | FR-002 |
| UC-004 | Ghi nhận xe vào | Nhân viên bãi xe | Must Have | FR-003 |
| UC-005 | Ghi nhận xe ra và tính phí | Nhân viên bãi xe | Must Have | FR-004 |
| UC-006 | Theo dõi chỗ trống theo khu vực | Quản lý, Nhân viên bãi xe | Must Have | FR-005 |
| UC-007 | Tra cứu lượt gửi xe | Quản lý, Nhân viên bãi xe | Should Have | FR-006 |
| UC-008 | Quản lý vé tháng hoặc khách quen | Quản lý | Should Have | FR-007 |
| UC-009 | Xem thống kê vận hành | Quản lý | Must Have | FR-008 |
| UC-010 | AI sinh báo cáo lưu lượng | Quản lý | Should Have | FR-009 / AIR-001 |
| UC-011 | AI hỏi đáp dữ liệu bãi xe | Quản lý | Should Have | FR-010 / AIR-002 |
| UC-012 | AI gợi ý bố trí nhân sự | Quản lý | Could Have | FR-011 / AIR-003 |

## Phần C — Đặc tả chi tiết

### UC-001 — Đăng nhập và phân quyền

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Cho phép người dùng truy cập các chức năng theo vai trò được cấp. |
| Primary Actor | Quản lý; Nhân viên bãi xe. |
| Supporting Actor | Không có. |
| Trigger | Người dùng yêu cầu đăng nhập. |
| Preconditions | Người dùng có thông tin đăng nhập; hệ thống sẵn sàng. Quy tắc tài khoản cụ thể **[CẦN KIỂM CHỨNG]**. |
| Postconditions | Người dùng được cấp quyền tương ứng hoặc không được truy cập. |
| Priority / FR | Must Have; FR-001; SR-001, SR-002. |
| Business Rules | Quyền truy cập áp dụng theo vai trò; ma trận quyền chi tiết **[CẦN KIỂM CHỨNG]**. |
| Input / Output | Input: thông tin đăng nhập. Output: trạng thái đăng nhập và quyền truy cập. |
| Use Case liên quan | UC-002; mọi UC yêu cầu quyền phù hợp. |

**Main Success Scenario**

| Bước | Actor | Hệ thống |
| -- | -- | -- |
| 1 | Cung cấp thông tin đăng nhập. | Tiếp nhận thông tin. |
| 2 | Xác nhận gửi yêu cầu. | Xác thực thông tin. |
| 3 | — | Xác định vai trò đã được cấp. |
| 4 | — | Cho phép truy cập các chức năng phù hợp và thông báo đăng nhập thành công. |

**Alternative Flows**

| Mã | Điều kiện | Xử lý |
| -- | -- | -- |
| A1 | Thông tin đăng nhập không hợp lệ. | Hệ thống thông báo không thể xác thực; Use Case kết thúc. |
| A2 | Người dùng được xác thực nhưng không có quyền cho chức năng được chọn. | Hệ thống không cho phép truy cập chức năng đó. |

**Exception Flows**

| Mã | Ngoại lệ | Xử lý |
| -- | -- | -- |
| E1 | Không thể truy xuất dữ liệu xác thực. | Hệ thống thông báo lỗi và không tạo phiên truy cập. |

**Ghi chú:** chính sách mật khẩu, khóa tài khoản và thời hạn phiên là **[CẦN KIỂM CHỨNG]**.

### UC-002 — Quản lý tài khoản và phân quyền

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Cho phép quản lý duy trì tài khoản hoặc quyền theo vai trò nếu chức năng này được phê duyệt. |
| Primary Actor | Quản lý. |
| Supporting Actor | Không có. |
| Trigger | Quản lý yêu cầu quản lý tài khoản/quyền. |
| Preconditions | Quản lý đã đăng nhập và có quyền phù hợp. |
| Postconditions | Cấu hình tài khoản/quyền được cập nhật nếu dữ liệu hợp lệ. |
| Priority / FR | TBD — **[CẦN KIỂM CHỨNG]**; không có FR chính thức riêng trong `project.md`. |
| Input / Output | Input: thông tin tài khoản/quyền cần quản lý. Output: trạng thái cập nhật. |
| Use Case liên quan | UC-001. |

**Main Success Scenario**

| Bước | Actor | Hệ thống |
| -- | -- | -- |
| 1 | Chọn thao tác quản lý tài khoản/quyền. | Hiển thị thông tin được phép quản lý. |
| 2 | Cung cấp thay đổi. | Kiểm tra tính hợp lệ và quyền thực hiện. |
| 3 | Xác nhận thay đổi. | Lưu thay đổi và thông báo kết quả. |

**Alternative Flows**: A1 — dữ liệu thay đổi không hợp lệ: hệ thống yêu cầu điều chỉnh. A2 — actor không có quyền: hệ thống từ chối thao tác.

**Exception Flows**: E1 — không thể lưu thay đổi: hệ thống thông báo lỗi, dữ liệu hiện có không được xác nhận là đã thay đổi.

**Ghi chú:** tạo/sửa/xóa/khóa tài khoản, vai trò cụ thể và ma trận quyền chưa được nguồn dự án xác nhận; Use Case chỉ được triển khai sau xác nhận.

### UC-003 — Quản lý khu vực, vị trí đỗ và loại xe

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Cho phép quản lý duy trì dữ liệu khu vực, vị trí đỗ và loại xe. |
| Primary Actor | Quản lý. |
| Trigger | Quản lý yêu cầu thêm, xem, sửa hoặc xóa dữ liệu danh mục. |
| Preconditions | Quản lý đã đăng nhập và có quyền phù hợp. |
| Postconditions | Dữ liệu danh mục được cập nhật hoặc giữ nguyên khi thao tác không hợp lệ. |
| Priority / FR | Must Have; FR-002; DR-001, DR-002. |
| Input / Output | Input: dữ liệu khu vực, vị trí đỗ hoặc loại xe. Output: danh sách/trạng thái dữ liệu được cập nhật. |
| Use Case liên quan | UC-004, UC-005, UC-006. |

**Main Success Scenario**

| Bước | Actor | Hệ thống |
| -- | -- | -- |
| 1 | Chọn loại dữ liệu danh mục và thao tác cần thực hiện. | Hiển thị dữ liệu hiện có hoặc biểu mẫu phù hợp. |
| 2 | Cung cấp hoặc chỉnh sửa dữ liệu. | Kiểm tra dữ liệu theo quy tắc đã được xác nhận. |
| 3 | Xác nhận thao tác. | Cập nhật dữ liệu và thông báo kết quả. |

**Alternative Flows**: A1 — dữ liệu thiếu/sai: hệ thống yêu cầu bổ sung hoặc điều chỉnh. A2 — yêu cầu xóa dữ liệu có ràng buộc nghiệp vụ: **[CẦN KIỂM CHỨNG]** quy tắc xử lý.

**Exception Flows**: E1 — không thể lưu hoặc truy xuất dữ liệu: hệ thống thông báo lỗi và không xác nhận thao tác thành công.

**Ghi chú:** thuộc tính bắt buộc, trạng thái vị trí và quy tắc xóa chưa được đặc tả chi tiết.

### UC-004 — Ghi nhận xe vào

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Ghi nhận một lượt xe vào bãi cùng vé và thời gian gửi. |
| Primary Actor | Nhân viên bãi xe. |
| Trigger | Xe đến bãi và nhân viên thực hiện ghi nhận. |
| Preconditions | Nhân viên đã đăng nhập, có quyền thao tác; dữ liệu danh mục cần thiết sẵn có. |
| Postconditions | Lượt xe vào, vé và thời gian vào được ghi nhận; chỗ trống được theo dõi theo UC-006. |
| Priority / FR | Must Have; FR-003; DR-002, DR-003, DR-004. |
| Business Rules | Vé/phương tiện/thời gian gửi là dữ liệu nghiệp vụ được đề cập; quy tắc định danh và gán chỗ **[CẦN KIỂM CHỨNG]**. |
| Input / Output | Input: thông tin phương tiện, vé, thời gian vào và dữ liệu cần thiết. Output: xác nhận lượt xe vào. |
| Use Case liên quan | UC-003, UC-005, UC-006. |

**Main Success Scenario**

| Bước | Actor | Hệ thống |
| -- | -- | -- |
| 1 | Chọn ghi nhận xe vào. | Hiển thị thông tin cần ghi nhận. |
| 2 | Cung cấp thông tin phương tiện, vé và thời gian vào. | Kiểm tra dữ liệu được cung cấp. |
| 3 | Xác nhận ghi nhận. | Lưu lượt xe vào và vé liên quan. |
| 4 | — | Cập nhật thông tin theo dõi chỗ trống theo quy tắc được xác nhận. |
| 5 | — | Thông báo ghi nhận thành công. |

**Alternative Flows**

| Mã | Điều kiện | Xử lý |
| -- | -- | -- |
| A1 | Dữ liệu phương tiện/vé/thời gian thiếu hoặc không hợp lệ. | Hệ thống thông báo lỗi; nhân viên điều chỉnh và quay lại bước 2. |
| A2 | Không xác định được vị trí phù hợp. | Hệ thống thông báo không thể hoàn tất; quy tắc xử lý chỗ trống **[CẦN KIỂM CHỨNG]**. |

**Exception Flows**: E1 — không thể lưu dữ liệu: hệ thống thông báo lỗi và không xác nhận lượt xe vào.

### UC-005 — Ghi nhận xe ra và tính phí

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Hoàn tất lượt gửi xe bằng cách ghi nhận xe ra, thời gian gửi và phí. |
| Primary Actor | Nhân viên bãi xe. |
| Trigger | Xe rời bãi. |
| Preconditions | Nhân viên có quyền; có lượt gửi xe cần xử lý. |
| Postconditions | Lượt gửi được ghi nhận xe ra và phí theo quy tắc đã xác nhận; chỗ trống được theo dõi. |
| Priority / FR | Must Have; FR-004; BR-001; DR-004, DR-005. |
| Business Rules | Phí phụ thuộc loại xe và thời gian gửi. Công thức, ngoại lệ, miễn/giảm và thanh toán **[CẦN KIỂM CHỨNG]**. |
| Input / Output | Input: thông tin xác định lượt gửi và thời điểm xe ra. Output: phí gửi xe và trạng thái hoàn tất lượt gửi. |
| Use Case liên quan | UC-004, UC-006, UC-007. |

**Main Success Scenario**

| Bước | Actor | Hệ thống |
| -- | -- | -- |
| 1 | Chọn ghi nhận xe ra và cung cấp thông tin xác định lượt gửi. | Truy xuất lượt gửi tương ứng. |
| 2 | Xác nhận thời điểm xe ra. | Xác định thời gian gửi. |
| 3 | — | Tính phí theo loại xe và thời gian gửi. |
| 4 | Xác nhận hoàn tất lượt gửi. | Lưu thời điểm xe ra, phí và cập nhật theo dõi chỗ trống. |
| 5 | — | Hiển thị kết quả xử lý. |

**Alternative Flows**

| Mã | Điều kiện | Xử lý |
| -- | -- | -- |
| A1 | Không tìm thấy lượt gửi phù hợp. | Hệ thống thông báo không tìm thấy; Use Case kết thúc. |
| A2 | Dữ liệu thời gian không hợp lệ. | Hệ thống không tính phí, yêu cầu kiểm tra dữ liệu. |
| A3 | Không xác định được mức phí. | Hệ thống thông báo; không hoàn tất lượt gửi cho đến khi có quy tắc hợp lệ. |

**Exception Flows**: E1 — không thể lưu kết quả: hệ thống thông báo lỗi và không xác nhận hoàn tất.

### UC-006 — Theo dõi chỗ trống theo khu vực

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Cung cấp thông tin chỗ trống theo khu vực cho người dùng được cấp quyền. |
| Primary Actor | Quản lý; Nhân viên bãi xe. |
| Trigger | Actor yêu cầu xem tình trạng bãi đỗ. |
| Preconditions | Actor đã đăng nhập và có quyền. |
| Postconditions | Actor nhận được thông tin chỗ trống theo khu vực hiện có. |
| Priority / FR | Must Have; FR-005; DR-001. |
| Input / Output | Input: yêu cầu xem tình trạng, có thể theo khu vực. Output: tình trạng chỗ trống theo khu vực. |
| Use Case liên quan | UC-003, UC-004, UC-005. |

**Main Success Scenario**: 1) Actor chọn xem chỗ trống. 2) Hệ thống lấy thông tin khu vực/vị trí theo dữ liệu hiện có. 3) Hệ thống tổng hợp và hiển thị chỗ trống theo khu vực.

**Alternative Flows**: A1 — không có dữ liệu khu vực phù hợp: hệ thống thông báo không có dữ liệu để hiển thị. A2 — trạng thái vị trí chưa xác định: hệ thống chỉ hiển thị dữ liệu có thể xác định và thông báo phù hợp.

**Exception Flows**: E1 — không thể truy xuất dữ liệu: hệ thống thông báo lỗi.

**Ghi chú:** danh sách trạng thái vị trí, thời điểm cập nhật và công thức xác định chỗ trống là **[CẦN KIỂM CHỨNG]**.

### UC-007 — Tra cứu lượt gửi xe

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Tìm các lượt gửi xe theo biển số hoặc thời gian. |
| Primary Actor | Quản lý; Nhân viên bãi xe. |
| Trigger | Actor yêu cầu tra cứu. |
| Preconditions | Actor đã đăng nhập và có quyền phù hợp. |
| Postconditions | Danh sách lượt gửi phù hợp được hiển thị hoặc thông báo không có kết quả. |
| Priority / FR | Should Have; FR-006; DR-002, DR-004. |
| Input / Output | Input: biển số và/hoặc thời gian. Output: lượt gửi xe phù hợp. |
| Use Case liên quan | UC-004, UC-005. |

**Main Success Scenario**: 1) Actor chọn tra cứu. 2) Actor cung cấp biển số hoặc thời gian. 3) Hệ thống kiểm tra tiêu chí. 4) Hệ thống truy xuất lượt gửi phù hợp. 5) Hệ thống hiển thị kết quả.

**Alternative Flows**: A1 — tiêu chí không hợp lệ: hệ thống yêu cầu nhập lại. A2 — không có lượt gửi phù hợp: hệ thống thông báo không tìm thấy kết quả.

**Exception Flows**: E1 — không thể truy xuất dữ liệu: hệ thống thông báo lỗi.

### UC-008 — Quản lý vé tháng hoặc khách quen

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Hỗ trợ quản lý dữ liệu vé tháng hoặc khách quen. |
| Primary Actor | Quản lý. |
| Trigger | Quản lý yêu cầu quản lý dữ liệu vé tháng/khách quen. |
| Preconditions | Quản lý đã đăng nhập và có quyền phù hợp. |
| Postconditions | Dữ liệu được cập nhật nếu hợp lệ. |
| Priority / FR | Should Have; FR-007. |
| Input / Output | Input: thông tin vé tháng hoặc khách quen. Output: trạng thái dữ liệu được cập nhật. |
| Use Case liên quan | UC-003, UC-004, UC-005. |

**Main Success Scenario**: 1) Quản lý chọn thao tác quản lý. 2) Hệ thống hiển thị dữ liệu/biểu mẫu phù hợp. 3) Quản lý cung cấp hoặc chỉnh sửa dữ liệu. 4) Hệ thống kiểm tra theo quy tắc đã xác nhận. 5) Hệ thống lưu và thông báo kết quả.

**Alternative Flows**: A1 — dữ liệu không hợp lệ: hệ thống yêu cầu điều chỉnh. A2 — dữ liệu cần quản lý không tồn tại: hệ thống thông báo phù hợp.

**Exception Flows**: E1 — không thể lưu/truy xuất dữ liệu: hệ thống thông báo lỗi.

**Ghi chú:** điều kiện dùng, gia hạn, hết hạn và phân biệt vé tháng/khách quen là **[CẦN KIỂM CHỨNG]**.

### UC-009 — Xem thống kê vận hành

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Cung cấp thống kê lưu lượng, doanh thu và khung giờ cao điểm cho quản lý. |
| Primary Actor | Quản lý. |
| Trigger | Quản lý yêu cầu xem thống kê. |
| Preconditions | Quản lý đã đăng nhập và có quyền phù hợp; có dữ liệu nghiệp vụ phù hợp. |
| Postconditions | Thống kê được hiển thị hoặc có thông báo khi dữ liệu không đủ. |
| Priority / FR | Must Have; FR-008; DR-004, DR-006. |
| Input / Output | Input: yêu cầu xem thống kê; kỳ/bộ lọc cụ thể **[CẦN KIỂM CHỨNG]**. Output: lưu lượng, doanh thu, khung giờ cao điểm. |
| Use Case liên quan | UC-010, UC-011, UC-012. |

**Main Success Scenario**: 1) Quản lý chọn xem thống kê. 2) Hệ thống nhận yêu cầu và truy xuất dữ liệu lượt gửi phù hợp. 3) Hệ thống tổng hợp lưu lượng, doanh thu, khung giờ cao điểm. 4) Hệ thống hiển thị kết quả.

**Alternative Flows**: A1 — không có dữ liệu trong phạm vi được chọn: hệ thống thông báo dữ liệu không đủ. A2 — tiêu chí xem thống kê không hợp lệ: hệ thống yêu cầu điều chỉnh.

**Exception Flows**: E1 — không thể truy xuất/tổng hợp dữ liệu: hệ thống thông báo lỗi.

### UC-010 — AI sinh báo cáo lưu lượng

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Tạo báo cáo lưu lượng theo ngày/tuần từ dữ liệu hệ thống để hỗ trợ quản lý. |
| Primary Actor | Quản lý. |
| Supporting Actor | Không có; dịch vụ AI là thành phần nội bộ. |
| Trigger | Quản lý yêu cầu tạo báo cáo AI. |
| Preconditions | Quản lý đã đăng nhập, có quyền phù hợp và dữ liệu thống kê cần thiết có sẵn. |
| Postconditions | Báo cáo AI được hiển thị hoặc hệ thống thông báo AI/dữ liệu không khả dụng. |
| Priority / FR | Should Have; FR-009; AIR-001; BR-002; NFR-003. |
| Input / Output | Input AI: số lượt xe, doanh thu, tỷ lệ lấp đầy, khung giờ. Output AI: báo cáo lưu lượng theo ngày/tuần. |
| Use Case liên quan | UC-009, UC-011, UC-012. |

**Main Success Scenario**

| Bước | Actor | Hệ thống |
| -- | -- | -- |
| 1 | Yêu cầu báo cáo AI theo ngày hoặc tuần. | Kiểm tra quyền và yêu cầu. |
| 2 | — | Lấy dữ liệu thống kê phù hợp từ hệ thống. |
| 3 | — | Tạo yêu cầu AI với ràng buộc không tự tạo số liệu. |
| 4 | — | Nhận và kiểm tra kết quả AI. |
| 5 | — | Hiển thị báo cáo cùng cảnh báo rằng kết quả cần được quản lý kiểm chứng. |

**Alternative Flows**: A1 — dữ liệu không đủ: thông báo không thể tạo báo cáo. A2 — yêu cầu không thuộc ngày/tuần: yêu cầu điều chỉnh; tháng/năm **[CẦN KIỂM CHỨNG]**.

**Exception Flows**: E1 — AI timeout/rate limit/không khả dụng: thông báo lỗi, không bịa báo cáo. E2 — response rỗng/sai định dạng: thông báo không thể hiển thị kết quả hợp lệ.

**AI Component**: Mục đích: tóm tắt lưu lượng. Guardrail: chỉ nhận xét từ dữ liệu được cung cấp, không tự tạo số liệu. Cách dùng: quản lý đọc và kiểm chứng báo cáo. Rủi ro: kết quả thiếu/chưa chính xác; không dùng kết quả như quyết định bắt buộc.

### UC-011 — AI hỏi đáp dữ liệu bãi xe

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Giúp quản lý hỏi các câu hỏi phân tích dữ liệu bãi xe, ví dụ khung giờ đông nhất. |
| Primary Actor | Quản lý. |
| Supporting Actor | Không có; AI là thành phần nội bộ. |
| Trigger | Quản lý gửi câu hỏi phân tích. |
| Preconditions | Quản lý đã đăng nhập, có quyền phù hợp; dữ liệu cần thiết có sẵn theo quyền đã xác nhận. |
| Postconditions | Câu trả lời AI được hiển thị hoặc hệ thống thông báo không thể trả lời. |
| Priority / FR | Should Have; FR-010; AIR-002; BR-002; SR-003. |
| Input / Output | Input: câu hỏi quản trị và dữ liệu thống kê phù hợp. Output: câu trả lời phân tích dựa trên dữ liệu. |
| Use Case liên quan | UC-009, UC-010, UC-012. |

**Main Success Scenario**: 1) Quản lý nhập câu hỏi. 2) Hệ thống kiểm tra quyền và xác định dữ liệu phù hợp. 3) Hệ thống gửi ngữ cảnh dữ liệu cần thiết kèm ràng buộc không tự tạo số liệu. 4) Hệ thống kiểm tra kết quả AI. 5) Hệ thống hiển thị câu trả lời và cảnh báo kiểm chứng.

**Alternative Flows**: A1 — câu hỏi không có dữ liệu phù hợp: hệ thống thông báo không đủ dữ liệu. A2 — dữ liệu vượt quyền: hệ thống không cung cấp dữ liệu đó.

**Exception Flows**: E1 — AI không khả dụng/response không hợp lệ: hệ thống thông báo lỗi, không tạo câu trả lời thay thế.

**AI Component**: AI trả lời phân tích, không tự tạo số liệu. Quản lý dùng kết quả làm thông tin tham khảo; phạm vi quyền dữ liệu, logging và monitoring **[CẦN KIỂM CHỨNG]**.

### UC-012 — AI gợi ý bố trí nhân sự

| Trường | Đặc tả |
| -- | -- |
| Mục tiêu | Cung cấp gợi ý bố trí nhân sự theo khung giờ cao điểm để hỗ trợ quản lý. |
| Primary Actor | Quản lý. |
| Supporting Actor | Không có; AI là thành phần nội bộ. |
| Trigger | Quản lý yêu cầu gợi ý theo dữ liệu lưu lượng. |
| Preconditions | Quản lý đã đăng nhập và dữ liệu khung giờ cao điểm phù hợp có sẵn. |
| Postconditions | Gợi ý được hiển thị; quản lý tự quyết định có sử dụng hay không. |
| Priority / FR | Could Have; FR-011; AIR-003; BR-003; NFR-003. |
| Input / Output | Input AI: số lượt xe, tỷ lệ lấp đầy, khung giờ. Output AI: gợi ý bố trí nhân sự theo khung giờ cao điểm. |
| Use Case liên quan | UC-009, UC-010, UC-011. |

**Main Success Scenario**: 1) Quản lý yêu cầu gợi ý. 2) Hệ thống lấy dữ liệu thống kê phù hợp. 3) Hệ thống yêu cầu AI phân tích theo guardrail. 4) Hệ thống kiểm tra và hiển thị gợi ý. 5) Quản lý xem, kiểm chứng và tự quyết định phương án vận hành.

**Alternative Flows**: A1 — không đủ dữ liệu cao điểm: hệ thống thông báo không đủ cơ sở để gợi ý. A2 — kết quả AI không có nội dung có thể sử dụng: hệ thống thông báo không thể đưa ra gợi ý.

**Exception Flows**: E1 — AI timeout/rate limit/không khả dụng: thông báo lỗi; không tự động thay đổi bố trí nhân sự.

**AI Component**: Gợi ý chỉ mang tính tham khảo, không phải quyết định tự động. Không mở rộng sang phân bổ vị trí hoặc vận hành khác ngoài gợi ý nhân sự nếu chưa được xác nhận.

## Quan hệ Use Case

- UC-004 và UC-005 phụ thuộc dữ liệu danh mục của UC-003, nhưng không mô hình hóa `<<include>>` vì việc quản lý danh mục không xảy ra trong mỗi lượt xe.
- UC-005 và UC-004 làm thay đổi dữ liệu được UC-006 theo dõi; đây là liên hệ dữ liệu, không tự động dùng `<<include>>`.
- UC-010, UC-011 và UC-012 sử dụng dữ liệu thống kê từ UC-009. Không dùng `<<include>>` vì việc xem thống kê không phải là mục tiêu bắt buộc mà actor khởi tạo trong mọi yêu cầu AI.
- Không xác định generalization. UC-002 chỉ được giữ khi có xác nhận nghiệp vụ.

## Traceability

| Use Case | Functional Requirement | Actor | Dữ liệu chính | AI liên quan |
| -- | -- | -- | -- | -- |
| UC-001 | FR-001 | Quản lý, Nhân viên | Thông tin đăng nhập, vai trò | Không |
| UC-002 | TBD | Quản lý | Tài khoản, quyền **[CẦN KIỂM CHỨNG]** | Không |
| UC-003 | FR-002 | Quản lý | Khu vực, vị trí, loại xe | Không |
| UC-004 | FR-003 | Nhân viên | Phương tiện, vé, thời gian vào | Không |
| UC-005 | FR-004 | Nhân viên | Lượt gửi, thời gian ra, bảng giá | Không |
| UC-006 | FR-005 | Quản lý, Nhân viên | Khu vực, vị trí, trạng thái chỗ | Không |
| UC-007 | FR-006 | Quản lý, Nhân viên | Biển số, thời gian, lượt gửi | Không |
| UC-008 | FR-007 | Quản lý | Vé tháng/khách quen | Không |
| UC-009 | FR-008 | Quản lý | Lượt vào/ra, doanh thu, khung giờ | Không |
| UC-010 | FR-009 / AIR-001 | Quản lý | Lượt xe, doanh thu, tỷ lệ lấp đầy, khung giờ | Báo cáo lưu lượng |
| UC-011 | FR-010 / AIR-002 | Quản lý | Câu hỏi và dữ liệu thống kê phù hợp | Hỏi đáp dữ liệu |
| UC-012 | FR-011 / AIR-003 | Quản lý | Lượt xe, tỷ lệ lấp đầy, khung giờ | Gợi ý nhân sự |

## Kết luận và kiểm tra cuối

- **Tổng số Use Case:** 12.
- **Use Case nghiệp vụ:** 9 (UC-001 đến UC-009; UC-002 có điều kiện).
- **Use Case AI:** 3 (UC-010 đến UC-012).
- **Use Case cần kiểm chứng:** UC-002; các quy tắc chi tiết của UC-003, UC-004, UC-005, UC-006, UC-008 và UC-009.
- **Giả định đang sử dụng:** không có camera/OCR/QR/cổng thanh toán/IoT/mobile trong phạm vi hiện tại; AI là thành phần nội bộ; kết quả AI cần quản lý kiểm chứng; AI chỉ sử dụng dữ liệu cần thiết theo quyền được xác nhận.
- **Điểm còn thiếu thông tin:** quy tắc tài khoản/quyền; định danh xe và phân chỗ; công thức/ngoại lệ phí; quy tắc vé tháng; trạng thái/cập nhật chỗ trống; bộ lọc/quyền thống kê; model AI và quyền dữ liệu AI; logging/monitoring; chỉ tiêu hiệu năng.

Tài liệu không bổ sung nghiệp vụ chưa có căn cứ; mọi nội dung còn mở được đánh dấu **[CẦN KIỂM CHỨNG]**.


## Prompt sử dụng

Bạn là kiến trúc sư cơ sở dữ liệu. Hãy thiết kế CSDL cho hệ thống quản lý bãi đỗ xe có tích hợp AI.
Hãy dùng Chain-of-Thought cho bài toán cần suy luận nhiều bước và cân nhắc quan hệ dữ liệu để thực hiện

Ngữ cảnh: 
- Cần quản lý người dùng, vai trò, khu vực đỗ, vị trí đỗ, loại xe, lượt xe vào/ra, vé/thẻ xe (vé lượt/vé tháng), bảng giá tính phí gửi xe.
 - Cần hỗ trợ báo cáo doanh thu, lưu lượng xe theo ngày, tuần, tháng, khu vực và khung giờ cao điểm. 
- Cung cấp dữ liệu chỗ trống, bảng giá và quy định bãi xe cho Chatbot AI hỗ trợ giải đáp/tư vấn.
 - Cung cấp dữ liệu lượt xe, doanh thu, khung giờ cao điểm cho AI sinh báo cáo và gợi ý phân bổ nhân sự.
 Hãy suy nghĩ từng bước:
 1. Xác định các entity chính (tên entity để tiếng Việt) 
 2. Xác định thuộc tính quan trọng của từng entity.(tên thuộc tính để tiếng Việt)
 3. Xác định khóa chính, khóa ngoại.
 4. Xác định quan hệ 1-n, n-n nếu có.
 5. Xác định ràng buộc dữ liệu để tránh sai lệch số lượng chỗ trống và trạng thái xe vào/ra.

 6. Đề xuất lược đồ bảng. Ràng buộc:
- Ưu tiên SQLite cho demo.
- Không lưu API key trong CSDL.
- Không đưa dữ liệu thanh toán nhạy cảm vào prompt AI.

Định dạng đầu ra:
1. Danh sách entity và lý do tồn tại.
2. Bảng thiết kế CSDL dạng Markdown.
3. Mô tả quan hệ.
4. Gợi ý chỉ mục phục vụ tìm kiếm/báo cáo.
5. StarUML ERD (kèm code).

---

## Yêu cầu ghi kết quả

Khi thực hiện prompt này, hãy ghi toàn bộ kết quả đầu ra vào một file word mới để tên là "CSDL_v1.0.docx"

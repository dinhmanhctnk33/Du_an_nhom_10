import sys
import os
import textwrap
from pathlib import Path
from PIL import Image
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------
# Helper functions for python-docx styling & formatting
# ---------------------------------------------------------
def fmt(run, size=10, bold=None, italic=None, color=None, font_name='Calibri'):
    run.font.name = font_name
    rPr = run._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rPr.append(rFonts)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def set_cell(cell, text, bold=False, size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT, color=None):
    p = cell.paragraphs[0]
    p.clear()
    p.alignment = align
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run(text)
    fmt(r, size=size, bold=bold, color=color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def shade_cell(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_fill)
    tcPr.append(shd)

def set_table_col_widths(table, widths_in_inches):
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    for row in table.rows:
        for cell, w in zip(row.cells, widths_in_inches):
            cell.width = Inches(w)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    set_table_col_widths(tbl, [6.5])
    c = tbl.cell(0, 0)
    shade_cell(c, 'F8FAFC')
    p = c.paragraphs[0]
    p.clear()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(code_str)
    fmt(r, size=7.5, bold=False, color=(30, 41, 59), font_name='Consolas')
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(6)

# ---------------------------------------------------------
# Define Compilation Dataset for all OOD Diagrams
# ---------------------------------------------------------
DIAGRAMS_COMPILATION = [
    {
        'idx': 1,
        'title': 'Sơ đồ Lớp tổng thể (UML 2.5 Class Diagram)',
        'code_id': 'CLS-DIAGRAM-001',
        'desc': 'Biểu diễn cấu trúc 21 Lớp thuộc 5 Module nghiệp vụ (Access, Catalog, Operation, Search & Report, AI Integration) và Tầng truy cập dữ liệu.',
        'img_path': 'ood_assets/class_diagram_v2.png',
        'puml_code': """@startuml
title Mô hình Lớp tổng thể — Hệ thống Quản lý Bãi xe Thông minh
skinparam classAttributeIconSize 0

package "MOD-001 Access" {
    class UserAccount {
        -accountId: String
        -role: Role
        +hasRole(role): boolean
    }
    class AuthService {
        +authenticate(username, password)
        +authorize(userAccount, role)
    }
}

package "MOD-002 Parking Catalog" {
    class ParkingArea {
        -areaId: String
        -capacity: int
        +exposeAvailableSlotCount(): int
    }
    class ParkingSlot {
        -slotId: String
        -status: SlotStatus
        +updateStatus(status): void
    }
    class VehicleType {
        -typeId: String
        +matches(vehicle): boolean
    }
    class MonthlyPass {
        -passId: String
        +isValidAt(dateTime): boolean
    }
}

package "MOD-003 Parking Operation" {
    class Vehicle {
        -identifier: String
        +formatIdentifier(): String
    }
    class ParkingTicket {
        -ticketId: String
        +isValid(): boolean
    }
    class ParkingVisit {
        -visitId: String
        -entryTime: DateTime
        -exitTime: DateTime
        +closeVisit(exitTime)
        +setFee(amount)
    }
    class PriceTable {
        -priceRuleId: String
        +calculateFor(duration): BigDecimal
    }
}

package "MOD-004 Parking Search & Report" {
    class ParkingStatistics {
        -period: String
        +summarize(): DTO
    }
    class ParkingSearchService {
        +searchByVehicle()
    }
    class ReportingService {
        +buildStatistics(period)
    }
}

package "MOD-005 AI Integration" {
    class AIAnalysisService {
        +generateReport()
        +answerQuestion()
    }
    class PromptTemplate {
        +compose(context)
    }
    class StatisticsContextProvider {
        +provideContext(role)
    }
    class AIAdapter {
        +requestAnalysis(prompt)
    }
    class AIResponseValidator {
        +validate(rawResponse)
    }
}

package "Data Access Layer" {
    class ParkingDataRepository {
        +save(entity)
        +findById(id)
    }
}

UserAccount --> AuthService
ParkingSlot --> ParkingArea
ParkingVisit --> Vehicle
ParkingVisit --> ParkingTicket
ParkingVisit --> ParkingSlot
ParkingOperationService --> PriceTable
AIAnalysisService --> PromptTemplate
AIAnalysisService --> StatisticsContextProvider
AIAnalysisService --> AIAdapter
AIAnalysisService --> AIResponseValidator
AuthService --> ParkingDataRepository
@enduml""",
        'mermaid_code': """classDiagram
    class UserAccount {
        +accountId: String
        +role: Role
        +hasRole(role)
    }
    class AuthService {
        +authenticate()
        +authorize()
    }
    class ParkingArea {
        +areaId: String
        +capacity: int
        +exposeAvailableCount()
    }
    class ParkingSlot {
        +slotId: String
        +status: SlotStatus
        +updateStatus()
    }
    class Vehicle {
        +identifier: String
        +formatIdentifier()
    }
    class ParkingVisit {
        +visitId: String
        +entryTime: DateTime
        +exitTime: DateTime
        +closeVisit()
        +setFee()
    }
    class PriceTable {
        +priceRuleId: String
        +calculateFor()
    }
    class AIAnalysisService {
        +generateReport()
        +answerQuestion()
    }
    class AIAdapter {
        +requestAnalysis()
    }
    class ParkingDataRepository {
        +save()
        +findById()
    }

    UserAccount --> AuthService : authenticates
    ParkingSlot --> ParkingArea : belongsTo
    ParkingVisit --> Vehicle : associatedWith
    ParkingOperationService --> PriceTable : calculatesWith
    AIAnalysisService --> AIAdapter : delegatesTo
    AuthService --> ParkingDataRepository : uses"""
    },
    {
        'idx': 2,
        'title': 'Sơ đồ Tương tác SEQ-001: Đăng nhập và phân quyền (Sequence Diagram)',
        'code_id': 'SEQ-001',
        'desc': 'Chuỗi thông điệp tương tác đối tượng khi người dùng đăng nhập hệ thống, bao gồm nhánh xác thực thành công, sai tài khoản (A1), vượt quyền (A2) và lỗi CSDL (E1).',
        'img_path': 'v2_assets/SEQ-001_v2.png',
        'puml_code': """@startuml
title SEQ-001 — Đăng nhập và phân quyền
hide footbox
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true
participant "Actor" as P1
participant "Giao diện" as P2
participant "Dịch vụ xác thực" as P3
participant "Kho tài khoản" as P4

alt Luồng chính thành công
P1 -> P2 : 1. Gửi thông tin đăng nhập
P2 -> P3 : 2. Yêu cầu xác thực
P3 -> P4 : 3. Đối chiếu thông tin tài khoản
P4 ---> P3 : 4. Trả về thông tin vai trò & quyền
P3 ---> P2 : 5. Tạo phiên & cấp quyền thành công
P2 ---> P1 : 6. Thông báo thành công & cấp menu vai trò
else Luồng thay thế A1 — Thông tin không hợp lệ
P3 ---> P2 : A1.1: Từ chối xác thực (sai tài khoản/mật khẩu)
P2 ---> P1 : A1.2: Thông báo không thể xác thực; kết thúc UC
else Luồng thay thế A2 — Không có quyền chức năng
P2 ---> P1 : A2.1: Từ chối truy cập chức năng vượt quyền
else Luồng ngoại lệ E1 — Lỗi CSDL
P4 ---> P3 : E1.1: Lỗi kết nối CSDL / truy xuất dữ liệu
P3 ---> P2 : E1.2: Báo lỗi hệ thống, không tạo phiên
P2 ---> P1 : E1.3: Thông báo lỗi hệ thống, yêu cầu thử lại
end
@enduml"""
    },
    {
        'idx': 3,
        'title': 'Sơ đồ Tương tác SEQ-005: Ghi nhận xe ra và tính phí (Sequence Diagram)',
        'code_id': 'SEQ-005',
        'desc': 'Chuỗi thông điệp tương tác khi quẹt thẻ xe ra, đối chiếu lượt xe vào, gọi Bảng giá tính phí, thu tiền và giải phóng chỗ. Bao gồm xử lý lỗi A1, A2, A3 và E1.',
        'img_path': 'v2_assets/SEQ-005_v2.png',
        'puml_code': """@startuml
title SEQ-005 — Ghi nhận xe ra và tính phí
hide footbox
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true
participant "Nhân viên bãi xe" as P1
participant "Giao diện" as P2
participant "Dịch vụ bãi xe" as P3
participant "Kho dữ liệu" as P4
participant "Bảng giá" as P5

alt Luồng chính thành công
P1 -> P2 : 1. Quét thẻ / nhập thông tin xe ra
P2 -> P3 : 2. Yêu cầu ghi nhận xe ra
P3 -> P4 : 3. Tìm lượt gửi xe tương ứng
P4 ---> P3 : 4. Trả về thông tin lượt gửi & giờ vào
P3 -> P5 : 5. Yêu cầu tính phí theo loại xe & thời gian
P5 ---> P3 : 6. Trả về số tiền phí gửi xe
P3 ---> P2 : 7. Hiển thị số tiền phí cho Nhân viên
P1 -> P2 : 8. Xác nhận đã thu tiền thanh toán
P2 -> P3 : 9. Gửi xác nhận thanh toán thành công
P3 -> P4 : 10. Ghi nhận xe ra & giải phóng vị trí đỗ
P4 ---> P3 : 11. Lưu hoàn tất lượt gửi thành công
P3 ---> P2 : 12. Trả về kết quả hoàn tất
P2 ---> P1 : 13. Thông báo hoàn tất & mở barie xe ra
else Luồng thay thế A1 — Không tìm thấy lượt gửi
P4 ---> P3 : A1.1: Không tìm thấy thông tin xe vào
P3 ---> P2 : A1.2: Báo không tìm thấy lượt gửi
P2 ---> P1 : A1.3: Báo không tìm thấy; yêu cầu xử lý thủ công
else Luồng thay thế A2 — Sai lệch thời gian
P3 ---> P2 : A2.1: Báo sai lệch thời gian ra/vào
P2 ---> P1 : A2.2: Không tính phí, yêu cầu kiểm tra lại
else Luồng thay thế A3 — Không tính được phí
P5 ---> P3 : A3.1: Không có quy định mức phí phù hợp
P3 ---> P2 : A3.2: Báo lỗi bảng giá không tính được phí
P2 ---> P1 : A3.3: Thông báo không thể hoàn tất lượt gửi
else Luồng ngoại lệ E1 — Lỗi lưu CSDL
P4 ---> P3 : E1.1: Lỗi lưu kết quả xe ra vào CSDL
P3 ---> P2 : E1.2: Báo lỗi lưu dữ liệu
P2 ---> P1 : E1.3: Thông báo lỗi hệ thống, chưa hoàn tất xe ra
end
@enduml"""
    },
    {
        'idx': 4,
        'title': 'Sơ đồ Tương tác SEQ-010: AI sinh báo cáo lưu lượng (Sequence Diagram)',
        'code_id': 'SEQ-010',
        'desc': 'Chuỗi thông điệp tương tác khi Quản lý yêu cầu AI tạo báo cáo lưu lượng ngày/tuần, xây dựng prompt kèm guardrails, gọi AI API và xử lý fallback E1, E2.',
        'img_path': 'v2_assets/SEQ-010_v2.png',
        'puml_code': """@startuml
title SEQ-010 — AI sinh báo cáo lưu lượng
hide footbox
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true
participant "Quản lý" as P1
participant "Giao diện" as P2
participant "Dịch vụ AI" as P3
participant "Dịch vụ thống kê" as P4
participant "Nhà cung cấp AI" as P5

alt Luồng chính thành công
P1 -> P2 : 1. Yêu cầu tạo báo cáo AI (ngày/tuần)
P2 -> P3 : 2. Gửi yêu cầu sinh báo cáo
P3 -> P4 : 3. Lấy dữ liệu lưu lượng & khung giờ
P4 ---> P3 : 4. Trả về dữ liệu thống kê hợp lệ
P3 -> P5 : 5. Gửi prompt + ràng buộc không bịa số liệu
P5 ---> P3 : 6. Trả về nội dung văn bản báo cáo AI
P3 ---> P2 : 7. Kiểm tra định dạng & đính kèm cảnh báo
P2 ---> P1 : 8. Hiển thị báo cáo AI kèm lưu ý kiểm chứng
else Luồng thay thế A1 — Dữ liệu không đủ
P4 ---> P3 : A1.1: Báo không đủ dữ liệu thống kê
P3 ---> P2 : A1.2: Từ chối gọi AI, báo không đủ dữ liệu
P2 ---> P1 : A1.3: Thông báo không thể tạo báo cáo AI
else Luồng thay thế A2 — Sai phạm vi ngày/tuần
P3 ---> P2 : A2.1: Báo phạm vi báo cáo không hỗ trợ
P2 ---> P1 : A2.2: Yêu cầu chọn phạm vi ngày hoặc tuần
else Luồng ngoại lệ E1 — AI timeout/error
P5 ---> P3 : E1.1: Lỗi timeout / rate limit / 503
P3 ---> P2 : E1.2: Fallback báo lỗi AI, không bịa nội dung
P2 ---> P1 : E1.3: Báo lỗi AI không khả dụng, không tạo báo cáo
else Luồng ngoại lệ E2 — Response AI rỗng/sai
P5 ---> P3 : E2.1: Response rỗng hoặc sai cấu trúc text
P3 ---> P2 : E2.2: Từ chối kết quả không hợp lệ
P2 ---> P1 : E2.3: Thông báo kết quả AI không hợp lệ
end
@enduml"""
    },
    {
        'idx': 5,
        'title': 'Sơ đồ Chuyển trạng thái STD-001: Vị trí đỗ xe (State Machine Diagram)',
        'code_id': 'STD-001',
        'desc': 'Vòng đời chuyển trạng thái của đối tượng ParkingSlot giữa Available (chỗ trống) và Occupied (đã đỗ) theo các sự kiện xe vào và xe ra.',
        'img_path': 'ood_assets/state_machine_v2.png',
        'puml_code': """@startuml
title STD-001 — Sơ đồ chuyển trạng thái Vị trí đỗ xe (ParkingSlot State Machine)

[*] --> Available : Khởi tạo vị trí đỗ

Available --> Occupied : Ghi nhận xe vào [FR-003] / slot.updateStatus(Occupied)
Occupied --> Available : Ghi nhận xe ra & Phí [FR-004] / slot.updateStatus(Available)

note right of Available
  Vị trí đỗ xe đang trống,
  sẵn sàng gán cho xe vào bãi
end note

note right of Occupied
  Vị trí đỗ xe đã có phương tiện
  gửi trong bãi
end note
@enduml"""
    },
    {
        'idx': 6,
        'title': 'Sơ đồ Hoạt động ACTD-001: Tiến trình Lượt gửi xe vào/ra (Activity Diagram)',
        'code_id': 'ACTD-001',
        'desc': 'Phân làn hoạt động giữa Nhân viên bãi xe và Hệ thống trong toàn bộ vòng đời lượt gửi xe từ quẹt thẻ vào đến tính phí xe ra.',
        'img_path': 'act_assets/act_05.png',
        'puml_code': """@startuml
title 5. Sơ đồ hoạt động của Ghi nhận xe ra và tính phí
skinparam ActivityFontSize 13
skinparam ActivityBorderColor #1E293B
skinparam ActivityBackgroundColor #F8FAFC
skinparam ActivityDiamondBorderColor #D97706
skinparam ActivityDiamondBackgroundColor #FEF3C7

|Nhân viên bãi xe|
start
:Quét thẻ vé / Nhập thông tin xe ra;

|Hệ thống|
:Tìm lượt xe vào tương ứng trong CSDL;
if (Tìm thấy lượt vào & Thời gian hợp lệ?) then ([Đúng])
  :Tính phí gửi xe theo loại xe và thời gian;
  |Nhân viên bãi xe|
  :Thu tiền gửi xe & Xác nhận thanh toán;
  |Hệ thống|
  :Ghi nhận xe ra & Giải phóng vị trí đỗ CSDL;
  |Nhân viên bãi xe|
  :Mở barie cho xe rời bãi;
  stop
else ([Không tìm thấy / Lỗi phí])
  |Nhân viên bãi xe|
  :Thông báo không thể hoàn tất & Xử lý thủ công;
  stop
endif
@enduml"""
    },
    {
        'idx': 7,
        'title': 'Sơ đồ Hoạt động ACTD-002: Tiến trình Tích hợp AI (Activity Diagram)',
        'code_id': 'ACTD-002',
        'desc': 'Phân làn hoạt động giữa Quản lý, Hệ thống và Nhà cung cấp AI trong việc sinh báo cáo lưu lượng, giải đáp thắc mắc và gợi ý bố trí nhân sự.',
        'img_path': 'act_assets/act_10.png',
        'puml_code': """@startuml
title 10. Sơ đồ hoạt động của AI sinh báo cáo lưu lượng
skinparam ActivityFontSize 13
skinparam ActivityBorderColor #1E293B
skinparam ActivityBackgroundColor #F8FAFC
skinparam ActivityDiamondBorderColor #D97706
skinparam ActivityDiamondBackgroundColor #FEF3C7

|Quản lý|
start
:Yêu cầu tạo báo cáo AI (ngày hoặc tuần);

|Hệ thống|
:Lấy dữ liệu thống kê & Xây dựng prompt guardrails;
if (Đủ dữ liệu thống kê?) then ([Đúng])
  |Nhà cung cấp AI|
  :Xử lý mô hình ngôn ngữ & Trả về văn bản báo cáo;
  |Hệ thống|
  if (Response AI đúng định dạng?) then ([Đúng])
    :Đính kèm cảnh báo kiểm chứng & Hiển thị báo cáo;
    |Quản lý|
    :Xem báo cáo AI & tự kiểm chứng số liệu;
    stop
  else ([Lỗi Format / Rỗng])
    |Quản lý|
    :Thông báo kết quả AI không hợp lệ;
    stop
  endif
else ([Thiếu dữ liệu / Lỗi AI])
  |Quản lý|
  :Thông báo không thể tạo báo cáo AI;
  stop
endif
@enduml"""
    }
]

# ---------------------------------------------------------
# Build ood_diagram.docx
# ---------------------------------------------------------
print('Starting document assembly for ood_diagram.docx...')
doc_target = Document()

# Set standard margins (1 inch = 72 pt)
for s in doc_target.sections:
    s.top_margin = Inches(1)
    s.bottom_margin = Inches(1)
    s.left_margin = Inches(1)
    s.right_margin = Inches(1)

# Document Header Title
p_title = doc_target.add_paragraph()
r_title = p_title.add_run('HỆ THỐNG QUẢN LÝ BÃI XE THÔNG MINH')
fmt(r_title, size=18, bold=True, color=(15, 23, 42))

p_sub = doc_target.add_paragraph()
r_sub = p_sub.add_run('TỔNG HỢP SƠ ĐỒ & MÃ NGUỒN THIẾT KẾ HƯỚNG ĐỐI TƯỢNG (OOD DIAGRAM CODE)')
fmt(r_sub, size=14, bold=True, color=(37, 99, 235))

p_sub2 = doc_target.add_paragraph()
r_sub2 = p_sub2.add_run('Tuyển tập Sơ đồ Lớp, Sequence Diagrams, State Machine & Activity Diagrams kèm Mã PlantUML / Mermaid')
fmt(r_sub2, size=10.5, italic=True, color=(71, 85, 105))

# Document Metadata Table
tbl_meta = doc_target.add_table(rows=4, cols=2)
set_table_col_widths(tbl_meta, [2.0, 4.5])
meta_data = [
    ('Dự án áp dụng', 'Hệ thống Quản lý Bãi đỗ xe tích hợp AI (Nhóm 10)'),
    ('Loại tài liệu', 'Tổng hợp Sơ đồ Ảnh & Mã nguồn Sơ đồ (PlantUML / Mermaid Code)'),
    ('Ứng dụng mã nguồn', 'Dùng nạp trực tiếp vào StarUML, PlantUML Extension hoặc Mermaid Live Editor'),
    ('Phiên bản tài liệu', 'v1.0 — Đóng gói đồng bộ với file Thiết kế OOD v2.0')
]
for i, (k, v) in enumerate(meta_data):
    row = tbl_meta.rows[i]
    set_cell(row.cells[0], k, bold=True, size=9, color=(15, 23, 42))
    shade_cell(row.cells[0], 'F1F5F9')
    set_cell(row.cells[1], v, bold=False, size=9)

p_space = doc_target.add_paragraph()
p_space.paragraph_format.space_after = Pt(12)

# Section 1: Intro
h1_1 = doc_target.add_heading(level=1)
r = h1_1.add_run('Hướng dẫn Sử dụng Mã nguồn Sơ đồ (Diagram Code Guide)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_guide = doc_target.add_paragraph()
p_guide.paragraph_format.line_spacing = 1.15
r = p_guide.add_run(
    'Tài liệu này tổng hợp toàn bộ các sơ đồ thiết kế hướng đối tượng được chèn trong báo cáo OOD v2.0 kèm mã nguồn gốc chi tiết:\n'
    '• Tất cả mã sơ đồ PlantUML (trong khung Consolas) tuân thủ đúng chuẩn cú pháp PlantUML 1.2026+.\n'
    '• Các khối `alt` / `else` / `end` trong sơ đồ tuần tự được viết đúng thứ tự, bảo đảm không bị lỗi `Cannot create group`.\n'
    '• Em có thể sao chép trực tiếp đoạn mã trong các ô khung xám để dán vào công cụ StarUML (qua extension PlantUML) hoặc VS Code để render lại sơ đồ bất cứ lúc nào.'
)
fmt(r, size=10, color=(30, 41, 59))

# Section 2+: Each Diagram Item
for item in DIAGRAMS_COMPILATION:
    idx = item['idx']
    title = item['title']
    code_id = item['code_id']
    desc = item['desc']
    img_path = item['img_path']
    puml_code = item['puml_code']
    mermaid_code = item.get('mermaid_code', None)
    
    print(f"[{idx}/7] Compiling {title} into ood_diagram.docx...")
    doc_target.add_page_break()
    
    # Heading 1
    h_item = doc_target.add_heading(level=1)
    r = h_item.add_run(f"{idx}. {title}")
    fmt(r, size=13, bold=True, color=(15, 23, 42))
    
    # Description
    p_desc = doc_target.add_paragraph()
    p_desc.paragraph_format.space_after = Pt(6)
    r = p_desc.add_run(f"Mã sơ đồ: {code_id} | {desc}")
    fmt(r, size=9.5, italic=True, color=(51, 65, 85))
    
    # Image
    if Path(img_path).exists():
        doc_target.add_picture(img_path, width=Inches(6.5))
        p_cap = doc_target.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(f"Hình — {idx}: Visual Diagram {code_id}")
        fmt(r_cap, size=8.5, italic=True, color=(100, 116, 139))
        
    # PlantUML Code Header
    h2_puml = doc_target.add_heading(level=2)
    r = h2_puml.add_run(f"Mã nguồn PlantUML ({code_id})")
    fmt(r, size=11, bold=True, color=(30, 41, 59))
    
    add_code_block(doc_target, puml_code)
    
    # Mermaid Code Header (if available)
    if mermaid_code:
        h2_m = doc_target.add_heading(level=2)
        r = h2_m.add_run(f"Mã nguồn Mermaid ({code_id})")
        fmt(r, size=11, bold=True, color=(30, 41, 59))
        add_code_block(doc_target, mermaid_code)

# Save Document
out_doc_path = Path('ood_diagram.docx')
try:
    doc_target.save(out_doc_path)
    print('====================================================')
    print(f'SUCCESS! File saved to: {out_doc_path.resolve()}')
    print('====================================================')
except PermissionError:
    alt_path = Path('ood_diagram_fixed.docx')
    doc_target.save(alt_path)
    print('====================================================')
    print(f'ood_diagram.docx đang mở trong Word! Đã lưu tạm sang: {alt_path.resolve()}')
    print('====================================================')

import sys
import os
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

ASSETS_DIR = Path('ood_assets')
ASSETS_DIR.mkdir(exist_ok=True)

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
# Image Generator: Visual UML Class Diagram Engine
# ---------------------------------------------------------
def draw_class_diagram(output_filename):
    width = 1600
    height = 1100
    
    img = Image.new('RGB', (width, height), 'white')
    d = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 24)
        font_module = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
        font_cname = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 17)
        font_stereo = ImageFont.truetype('C:/Windows/Fonts/ariali.ttf', 14)
        font_body = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
    except OSError:
        font_title = font_module = font_cname = font_stereo = font_body = ImageFont.load_default()
        
    # Document Title Box
    d.rounded_rectangle((20, 15, width - 20, 65), radius=8, fill='#F1F5F9', outline='#0F172A', width=2)
    d.text((35, 25), 'Sơ đồ lớp tổng thể (UML 2.5 Class Diagram — 5 Modules & 21 Classes)', font=font_title, fill='#0F172A')
    
    # Define Module Package Boxes
    modules_box = [
        ('MOD-001 Access Module', 40, 85, 340, 400, '#EFF6FF', '#2563EB'),
        ('MOD-002 Parking Catalog', 360, 85, 960, 400, '#F0FDF4', '#16A34A'),
        ('MOD-003 Parking Operation', 980, 85, 1560, 400, '#FFFBEB', '#D97706'),
        ('MOD-004 Search & Report', 40, 420, 760, 720, '#F5F3FF', '#7C3AED'),
        ('MOD-005 AI Integration', 780, 420, 1560, 720, '#FEF2F2', '#DC2626'),
        ('Data Access Abstraction', 40, 740, 1560, 1060, '#F8FAFC', '#475569')
    ]
    
    for name, x1, y1, x2, y2, bg_col, bd_col in modules_box:
        d.rectangle((x1, y1, x2, y2), fill=bg_col, outline=bd_col, width=2)
        # Package Tag
        d.rectangle((x1, y1, x1 + 240, y1 + 30), fill=bd_col)
        d.text((x1 + 10, y1 + 5), name, font=font_module, fill='white')
        
    # Helper to draw a Class Box inside diagram
    def draw_class_box(cx, cy, cw, ch, ccode, cname, stereotype, attrs, methods, border_color='#1E293B'):
        # Outer box
        d.rectangle((cx, cy, cx + cw, cy + ch), fill='white', outline=border_color, width=2)
        # Header partition
        header_h = 42
        d.rectangle((cx, cy, cx + cw, cy + header_h), fill='#F8FAFC', outline=border_color, width=1)
        d.text((cx + 10, cy + 4), f'<<{stereotype}>>', font=font_stereo, fill='#64748B')
        d.text((cx + 10, cy + 18), f'{ccode} {cname}', font=font_cname, fill='#0F172A')
        
        # Divider line
        d.line((cx, cy + header_h, cx + cw, cy + header_h), fill=border_color, width=1)
        
        # Attributes
        curr_y = cy + header_h + 4
        for a in attrs:
            d.text((cx + 8, curr_y), f'- {a}', font=font_body, fill='#334155')
            curr_y += 18
            
        attr_h = curr_y - cy
        d.line((cx, curr_y + 2, cx + cw, curr_y + 2), fill=border_color, width=1)
        curr_y += 6
        
        # Methods
        for m in methods:
            d.text((cx + 8, curr_y), f'+ {m}', font=font_body, fill='#0F172A')
            curr_y += 18

    # MOD-001 Classes
    draw_class_box(55, 130, 270, 115, 'CLS-001', 'UserAccount', 'Entity', ['accountId', 'role', 'credentialRef'], ['hasRole(role)'])
    draw_class_box(55, 260, 270, 115, 'CLS-011', 'AuthService', 'Control', ['sessionStore'], ['authenticate()', 'authorize()'])
    
    # MOD-002 Classes
    draw_class_box(375, 130, 270, 115, 'CLS-002', 'ParkingArea', 'Entity', ['areaId', 'name', 'capacity'], ['exposeAvailableCount()'])
    draw_class_box(665, 130, 275, 115, 'CLS-003', 'ParkingSlot', 'Entity', ['slotId', 'status', 'areaRef'], ['updateStatus(status)'])
    draw_class_box(375, 260, 270, 115, 'CLS-004', 'VehicleType', 'Entity', ['typeId', 'name', 'pricingCode'], ['matches(vehicle)'])
    draw_class_box(665, 260, 275, 115, 'CLS-009', 'MonthlyPass', 'Entity', ['passId', 'validFrom', 'validTo'], ['isValidAt(dateTime)'])

    # MOD-003 Classes
    draw_class_box(995, 130, 265, 115, 'CLS-005', 'Vehicle', 'Entity', ['vehicleId', 'identifier'], ['formatIdentifier()'])
    draw_class_box(1275, 130, 265, 115, 'CLS-006', 'ParkingTicket', 'Entity', ['ticketId', 'issuedAt', 'type'], ['isValid()'])
    draw_class_box(995, 260, 265, 115, 'CLS-007', 'ParkingVisit', 'Entity', ['visitId', 'entryTime', 'fee'], ['closeVisit()', 'setFee()'])
    draw_class_box(1275, 260, 265, 115, 'CLS-008', 'PriceTable', 'Entity', ['priceRuleId', 'rateRules'], ['calculateFor(duration)'])
    
    # MOD-004 Classes
    draw_class_box(55, 465, 330, 115, 'CLS-010', 'ParkingStatistics', 'DTO', ['traffic', 'revenue', 'peakHours'], ['summarize()'])
    draw_class_box(405, 465, 335, 115, 'CLS-014', 'ParkingSearchService', 'Control', ['searchRepo'], ['searchByVehicle()', 'searchByTime()'])
    draw_class_box(220, 595, 340, 105, 'CLS-015', 'ReportingService', 'Control', ['reportRepo'], ['buildStatistics(period)'])

    # MOD-005 Classes
    draw_class_box(795, 465, 350, 115, 'CLS-016', 'AIAnalysisService', 'AI/Control', ['aiConfig'], ['generateReport()', 'answerQuestion()'])
    draw_class_box(1165, 465, 375, 115, 'CLS-017', 'PromptTemplate', 'AI', ['templateText', 'guardrails'], ['compose(context)'])
    draw_class_box(795, 595, 350, 105, 'CLS-018', 'StatisticsContextProvider', 'AI', ['contextRules'], ['provideContext(role)'])
    draw_class_box(1165, 595, 375, 105, 'CLS-019', 'AIAdapter', 'AI/Boundary', ['apiKey', 'modelEndpoint'], ['requestAnalysis(prompt)'])
    
    # Data Access Layer
    draw_class_box(550, 800, 500, 120, 'CLS-021', 'ParkingDataRepository', 'Data Access', ['dbContext', 'connectionPool'], ['save(entity)', 'findById(id)', 'findByQuery(query)', 'update(entity)'])
    
    out_path = ASSETS_DIR / output_filename
    img.save(out_path)
    return str(out_path)

# Image Generator: State Machine Diagram Engine
def draw_state_machine_diagram(output_filename):
    width = 1200
    height = 400
    
    img = Image.new('RGB', (width, height), 'white')
    d = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 22)
        font_state = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
        font_event = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    except OSError:
        font_title = font_state = font_event = ImageFont.load_default()
        
    # Title Box
    d.rounded_rectangle((20, 15, width - 20, 65), radius=8, fill='#F1F5F9', outline='#0F172A', width=2)
    d.text((35, 25), 'STD-001: Sơ đồ chuyển trạng thái vị trí đỗ xe (ParkingSlot State Machine)', font=font_title, fill='#0F172A')
    
    # Start node
    d.ellipse((80, 190, 120, 230), fill='#0F172A', outline='#0F172A')
    d.text((70, 240), 'Khởi tạo', font=font_event, fill='#0F172A')
    
    # State 1: Available
    d.rounded_rectangle((240, 160, 480, 260), radius=16, fill='#F0FDF4', outline='#16A34A', width=3)
    d.text((310, 185), 'Available', font=font_state, fill='#15803D')
    d.text((280, 215), '(Vị trí đỗ xe đang trống)', font=font_event, fill='#166534')
    
    # State 2: Occupied
    d.rounded_rectangle((720, 160, 960, 260), radius=16, fill='#FEF2F2', outline='#DC2626', width=3)
    d.text((805, 185), 'Occupied', font=font_state, fill='#B91C1C')
    d.text((760, 215), '(Vị trí đang có xe đỗ)', font=font_event, fill='#991B1B')
    
    # Arrow Start -> Available
    d.line((120, 210, 240, 210), fill='#334155', width=3)
    d.polygon([(240, 210), (225, 202), (225, 218)], fill='#334155')
    
    # Arrow Available -> Occupied (Top curve)
    d.line((480, 185, 720, 185), fill='#1D4ED8', width=3)
    d.polygon([(720, 185), (705, 177), (705, 193)], fill='#1D4ED8')
    d.rectangle((520, 155, 680, 180), fill='white')
    d.text((530, 158), 'Ghi nhận xe vào [FR-003]', font=font_event, fill='#1E40AF')
    
    # Arrow Occupied -> Available (Bottom curve)
    d.line((720, 235, 480, 235), fill='#D97706', width=3)
    d.polygon([(480, 235), (495, 227), (495, 243)], fill='#D97706')
    d.rectangle((510, 220, 690, 245), fill='white')
    d.text((520, 223), 'Ghi nhận xe ra & Phí [FR-004]', font=font_event, fill='#B45309')

    out_path = ASSETS_DIR / output_filename
    img.save(out_path)
    return str(out_path)

# ---------------------------------------------------------
# Define all 21 Classes Complete Datasets
# ---------------------------------------------------------
CLASSES_DATA = [
    {
        'code': 'CLS-001', 'name': 'UserAccount', 'type': 'Entity', 'module': 'MOD-001 Access',
        'resp': 'Biểu diễn tài khoản và vai trò người dùng được xác thực (Quản lý hoặc Nhân viên bãi xe).',
        'attrs': 'accountId: TBD, role: Quản lý | Nhân viên bãi xe, credentialReference: TBD',
        'methods': 'hasRole(role): boolean',
        'deps': 'AuthService', 'related': 'FR-001, SR-001, UC-001'
    },
    {
        'code': 'CLS-002', 'name': 'ParkingArea', 'type': 'Entity', 'module': 'MOD-002 Catalog',
        'resp': 'Đại diện khu vực đỗ xe trong bãi (ví dụ: Khu A, Khu B).',
        'attrs': 'areaId: TBD, name: TBD, capacity: TBD',
        'methods': 'exposeAvailableSlotCount(): int',
        'deps': 'ParkingCatalogService', 'related': 'FR-002, DR-001, UC-002'
    },
    {
        'code': 'CLS-003', 'name': 'ParkingSlot', 'type': 'Entity', 'module': 'MOD-002 Catalog',
        'resp': 'Biểu diễn vị trí đỗ xe cụ thể và trạng thái theo dõi chỗ trống (Available / Occupied).',
        'attrs': 'slotId: TBD, areaReference: TBD, vehicleTypeReference: TBD, status: Available | Occupied',
        'methods': 'updateStatus(newStatus): void',
        'deps': 'ParkingArea, VehicleType, ParkingOperationService', 'related': 'FR-002, FR-005, DR-001, UC-002, UC-005'
    },
    {
        'code': 'CLS-004', 'name': 'VehicleType', 'type': 'Entity', 'module': 'MOD-002 Catalog',
        'resp': 'Phân loại phương tiện (Xe máy, Ô tô, Xe điện...) phục vụ danh mục và tính phí.',
        'attrs': 'typeId: TBD, name: TBD, pricingCode: TBD',
        'methods': 'matches(vehicle): boolean',
        'deps': 'PriceTable, ParkingOperationService', 'related': 'FR-002, FR-004, DR-005, UC-002, UC-004'
    },
    {
        'code': 'CLS-005', 'name': 'Vehicle', 'type': 'Entity', 'module': 'MOD-003 Operation',
        'resp': 'Biểu diễn phương tiện của lượt gửi (biển số xe, định danh phương tiện).',
        'attrs': 'vehicleId: TBD, identifier: TBD (Biển số xe), vehicleTypeReference: TBD',
        'methods': 'formatIdentifier(): String',
        'deps': 'VehicleType, ParkingVisit', 'related': 'FR-003, FR-006, DR-002, UC-003, UC-006'
    },
    {
        'code': 'CLS-006', 'name': 'ParkingTicket', 'type': 'Entity', 'module': 'MOD-003 Operation',
        'resp': 'Biểu diễn vé xe hoặc thẻ vé mã hóa liên quan tới lượt gửi.',
        'attrs': 'ticketId: TBD, issuedAt: TBD, ticketType: Lượt | Vé tháng',
        'methods': 'isValid(): boolean',
        'deps': 'ParkingVisit', 'related': 'FR-003, DR-003, UC-003'
    },
    {
        'code': 'CLS-007', 'name': 'ParkingVisit', 'type': 'Entity', 'module': 'MOD-003 Operation',
        'resp': 'Tập hợp sự kiện xe vào/ra, thời gian gửi, phương tiện, vé, vị trí và phí gửi xe.',
        'attrs': 'visitId: TBD, entryTime: TBD, exitTime: TBD, fee: TBD, vehicleRef: TBD, ticketRef: TBD, slotRef: TBD',
        'methods': 'closeVisit(exitTime), setFee(feeAmount)',
        'deps': 'Vehicle, ParkingTicket, ParkingSlot, PriceTable', 'related': 'FR-003, FR-004, BR-001, DR-004, UC-003, UC-004'
    },
    {
        'code': 'CLS-008', 'name': 'PriceTable', 'type': 'Entity', 'module': 'MOD-003 Operation',
        'resp': 'Cung cấp quy tắc và bảng giá tính phí gửi xe theo loại xe và thời gian gửi.',
        'attrs': 'priceRuleId: TBD, vehicleTypeReference: TBD, rateRules: TBD',
        'methods': 'calculateFor(visitDuration, vehicleType): feeAmount',
        'deps': 'VehicleType, ParkingOperationService', 'related': 'FR-004, BR-001, DR-005, UC-004'
    },
    {
        'code': 'CLS-009', 'name': 'MonthlyPass', 'type': 'Entity', 'module': 'MOD-002 Catalog',
        'resp': 'Biểu diễn thông tin vé tháng hoặc khách quen.',
        'attrs': 'passId: TBD, vehicleReference: TBD, validFrom: TBD, validTo: TBD, status: Active | Expired',
        'methods': 'isValidAt(dateTime): boolean',
        'deps': 'Vehicle, ParkingCatalogService', 'related': 'FR-007, DR-003, UC-007'
    },
    {
        'code': 'CLS-010', 'name': 'ParkingStatistics', 'type': 'DTO / Entity', 'module': 'MOD-004 Report',
        'resp': 'Đóng gói số liệu thống kê lượt xe, doanh thu, tỷ lệ lấp đầy và khung giờ cao điểm.',
        'attrs': 'period: TBD, trafficVolume: TBD, totalRevenue: TBD, occupancyRate: TBD, peakHours: TBD',
        'methods': 'summarize(): DTO',
        'deps': 'ReportingService, StatisticsContextProvider', 'related': 'FR-008, AIR-001..003, DR-006, UC-008'
    },
    {
        'code': 'CLS-011', 'name': 'AuthService', 'type': 'Control', 'module': 'MOD-001 Access',
        'resp': 'Điều phối xác thực người dùng và kiểm tra phân quyền truy cập chức năng.',
        'attrs': 'sessionStore: TBD',
        'methods': 'authenticate(username, password), authorize(userAccount, requiredRole)',
        'deps': 'UserAccount, ParkingDataRepository', 'related': 'FR-001, SR-001, SR-002, UC-001'
    },
    {
        'code': 'CLS-012', 'name': 'ParkingCatalogService', 'type': 'Control', 'module': 'MOD-002 Catalog',
        'resp': 'Điều phối quản lý khu vực, vị trí đỗ, loại xe và vé tháng.',
        'attrs': 'catalogRepository: TBD',
        'methods': 'manageArea(), manageSlot(), manageVehicleType(), manageMonthlyPass()',
        'deps': 'ParkingArea, ParkingSlot, VehicleType, MonthlyPass, ParkingDataRepository', 'related': 'FR-002, FR-007, UC-002, UC-007'
    },
    {
        'code': 'CLS-013', 'name': 'ParkingOperationService', 'type': 'Control', 'module': 'MOD-003 Operation',
        'resp': 'Điều phối ghi nhận xe vào/ra, cấp vé, tính phí và cập nhật chỗ trống.',
        'attrs': 'operationRepository: TBD',
        'methods': 'registerEntry(identifier, ticketId), registerExit(ticketId), calculateFee(visitId)',
        'deps': 'Vehicle, ParkingTicket, ParkingVisit, ParkingSlot, PriceTable, ParkingDataRepository', 'related': 'FR-003, FR-004, FR-005, BR-001, UC-003..005'
    },
    {
        'code': 'CLS-014', 'name': 'ParkingSearchService', 'type': 'Control', 'module': 'MOD-004 Report',
        'resp': 'Điều phối tra cứu lịch sử lượt gửi xe theo biển số hoặc khoảng thời gian.',
        'attrs': 'searchRepository: TBD',
        'methods': 'searchByVehicle(licensePlate), searchByTime(startTime, endTime)',
        'deps': 'ParkingDataRepository, ParkingVisit', 'related': 'FR-006, UC-006'
    },
    {
        'code': 'CLS-015', 'name': 'ReportingService', 'type': 'Control', 'module': 'MOD-004 Report',
        'resp': 'Tổng hợp số liệu báo cáo thống kê lưu lượng, doanh thu và khung giờ cao điểm.',
        'attrs': 'reportingRepository: TBD',
        'methods': 'buildStatistics(timePeriod, filterOptions)',
        'deps': 'ParkingDataRepository, ParkingStatistics', 'related': 'FR-008, DR-006, UC-008'
    },
    {
        'code': 'CLS-016', 'name': 'AIAnalysisService', 'type': 'AI / Control', 'module': 'MOD-005 AI',
        'resp': 'Điều phối chức năng AI: sinh báo cáo lưu lượng, hỏi đáp dữ liệu và gợi ý nhân sự.',
        'attrs': 'aiConfig: TBD',
        'methods': 'generateReport(period), answerQuestion(query), suggestStaffing(peakData)',
        'deps': 'PromptTemplate, StatisticsContextProvider, AIAdapter, AIResponseValidator', 'related': 'FR-009..011, AIR-001..003, UC-009..011'
    },
    {
        'code': 'CLS-017', 'name': 'PromptTemplate', 'type': 'AI', 'module': 'MOD-005 AI',
        'resp': 'Quản lý system/user prompt và đính kèm guardrails chống tự bịa số liệu.',
        'attrs': 'templateText: TBD, guardrails: TBD',
        'methods': 'compose(contextData, userQuery)',
        'deps': 'AIAnalysisService', 'related': 'AIR-001..003, BR-002'
    },
    {
        'code': 'CLS-018', 'name': 'StatisticsContextProvider', 'type': 'AI', 'module': 'MOD-005 AI',
        'resp': 'Trích xuất và cung cấp ngữ cảnh dữ liệu thống kê phù hợp theo quyền sử dụng.',
        'attrs': 'contextRules: TBD',
        'methods': 'provideContext(userRole, period)',
        'deps': 'ReportingService, ParkingStatistics', 'related': 'AIR-001..003, SR-003'
    },
    {
        'code': 'CLS-019', 'name': 'AIAdapter', 'type': 'AI / Boundary', 'module': 'MOD-005 AI',
        'resp': 'Cô lập kết nối API với Nhà cung cấp AI (OpenAI / Gemini / Claude / Ollama).',
        'attrs': 'apiKey: TBD, modelEndpoint: TBD',
        'methods': 'requestAnalysis(promptText)',
        'deps': 'AIAnalysisService', 'related': 'AIR-001..003, NFR-004'
    },
    {
        'code': 'CLS-020', 'name': 'AIResponseValidator', 'type': 'AI', 'module': 'MOD-005 AI',
        'resp': 'Kiểm tra phản hồi AI rỗng/sai định dạng và xử lý kết quả fallback an toàn.',
        'attrs': 'validationSchema: TBD',
        'methods': 'validate(rawResponse), fallbackMessage()',
        'deps': 'AIAnalysisService', 'related': 'AIR-001..003, NFR-003'
    },
    {
        'code': 'CLS-021', 'name': 'ParkingDataRepository', 'type': 'Data Access', 'module': 'Data Access',
        'resp': 'Cung cấp giao diện trừu tượng hóa thao tác đọc/ghi CSDL cho các Control Services.',
        'attrs': 'dbContext: TBD',
        'methods': 'save(entity), findById(id), findByQuery(query), update(entity)',
        'deps': 'Tất cả Entity Classes', 'related': 'DR-001..006'
    }
]

# ---------------------------------------------------------
# Build 04_GenAI_SoftwareDevelopment_object-oriented-design_v2.0.docx
# ---------------------------------------------------------
print('Starting document assembly for OOD v2.0 docx...')
doc_target = Document()

# Set standard margins (1 inch = 72 pt)
for s in doc_target.sections:
    s.top_margin = Inches(1)
    s.bottom_margin = Inches(1)
    s.left_margin = Inches(1)
    s.right_margin = Inches(1)

# Header Title
p_title = doc_target.add_paragraph()
r_title = p_title.add_run('HỆ THỐNG QUẢN LÝ BÃI XE THÔNG MINH')
fmt(r_title, size=18, bold=True, color=(15, 23, 42))

p_sub = doc_target.add_paragraph()
r_sub = p_sub.add_run('TÀI LIỆU THIẾT KẾ HƯỚNG ĐỐI TƯỢNG (OBJECT-ORIENTED DESIGN v2.0)')
fmt(r_sub, size=14, bold=True, color=(37, 99, 235))

p_sub2 = doc_target.add_paragraph()
r_sub2 = p_sub2.add_run('Đặc tả Mô hình Lớp UML 2.5, Sơ đồ Tương tác & Ma trận Truy vết Yêu cầu')
fmt(r_sub2, size=10.5, italic=True, color=(71, 85, 105))

# Document Metadata Table
tbl_meta = doc_target.add_table(rows=4, cols=2)
set_table_col_widths(tbl_meta, [2.0, 4.5])
meta_data = [
    ('Nguồn đặc tả', 'Đặc tả UC_done.docx, project.md & Requirements QA (Nhóm 10)'),
    ('Phạm vi thiết kế', '21 Classes, 5 Modules, Sequence Diagrams & State Machine'),
    ('Quy ước kiến trúc', 'Layered Architecture (Presentation -> Application -> Domain -> Data Access)'),
    ('Phiên bản tài liệu', 'v2.0 — Cập nhật đầy đủ Bảng đặc tả 21 Lớp & Sơ đồ trực quan độ phân giải cao')
]
for i, (k, v) in enumerate(meta_data):
    row = tbl_meta.rows[i]
    set_cell(row.cells[0], k, bold=True, size=9, color=(15, 23, 42))
    shade_cell(row.cells[0], 'F1F5F9')
    set_cell(row.cells[1], v, bold=False, size=9)

p_space = doc_target.add_paragraph()
p_space.paragraph_format.space_after = Pt(12)

# Section 1: Architecture & Packages
h1_1 = doc_target.add_heading(level=1)
r = h1_1.add_run('1. Tổng quan Kiến trúc & Cấu trúc Module (Packages)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_arch = doc_target.add_paragraph()
p_arch.paragraph_format.line_spacing = 1.15
r = p_conv = p_arch.add_run(
    'Thiết kế Hướng đối tượng (OOD) của Hệ thống Quản lý Bãi xe Thông minh được xây dựng theo kiến trúc phân tầng (Layered Architecture) '
    'nhằm giảm độ phụ thuộc (low coupling), tăng tính đóng gói (high cohesion) và bảo vệ các quy tắc nghiệp vụ cốt lõi:\n'
    '• Presentation / Boundary Layer: Tiếp nhận tương tác người dùng và cô lập giao diện API.\n'
    '• Application / Control Layer: Điều phối tiến trình nghiệp vụ, gọi repository và tích hợp dịch vụ AI.\n'
    '• Domain Entity Layer: Đóng gói dữ liệu và quy tắc nghiệp vụ chính (Bãi đỗ, Lượt xe, Vé, Giá).\n'
    '• Data Access Layer: Giao diện trừu tượng hóa `ParkingDataRepository` đọc/ghi cơ sở dữ liệu.'
)
fmt(r, size=10, color=(30, 41, 59))

# Module Summary Table
tbl_mod = doc_target.add_table(rows=1, cols=4)
set_table_col_widths(tbl_mod, [1.5, 1.4, 2.4, 1.2])
headers = ['Mã Module', 'Tên Module', 'Các Lớp trực thuộc (Classes)', 'Tầng kiến trúc']
for c, h in zip(tbl_mod.rows[0].cells, headers):
    set_cell(c, h, bold=True, size=9, color=(255, 255, 255))
    shade_cell(c, '1E293B')

mod_rows = [
    ('MOD-001 Access', 'Module Xác thực & Quyền', 'CLS-001 (UserAccount), CLS-011 (AuthService)', 'Control & Entity'),
    ('MOD-002 Catalog', 'Module Danh mục Bãi đỗ', 'CLS-002 (ParkingArea), CLS-003 (ParkingSlot), CLS-004 (VehicleType), CLS-009 (MonthlyPass), CLS-012 (ParkingCatalogService)', 'Control & Entity'),
    ('MOD-003 Operation', 'Module Vận hành Xe vào/ra', 'CLS-005 (Vehicle), CLS-006 (ParkingTicket), CLS-007 (ParkingVisit), CLS-008 (PriceTable), CLS-013 (ParkingOperationService)', 'Control & Entity'),
    ('MOD-004 Report', 'Module Tra cứu & Báo cáo', 'CLS-010 (ParkingStatistics), CLS-014 (ParkingSearchService), CLS-015 (ReportingService)', 'Control & DTO'),
    ('MOD-005 AI Integration', 'Module Tích hợp AI', 'CLS-016 (AIAnalysisService), CLS-017 (PromptTemplate), CLS-018 (StatisticsContextProvider), CLS-019 (AIAdapter), CLS-020 (AIResponseValidator)', 'AI & Control'),
    ('Data Access Layer', 'Tầng Truy cập Dữ liệu', 'CLS-021 (ParkingDataRepository)', 'Data Access Abstraction')
]

for mcode, mname, mclasses, mlayer in mod_rows:
    row = tbl_mod.add_row()
    set_cell(row.cells[0], mcode, bold=True, size=8.5)
    set_cell(row.cells[1], mname, bold=False, size=8.5)
    set_cell(row.cells[2], mclasses, bold=False, size=8.5)
    set_cell(row.cells[3], mlayer, bold=False, size=8.5)

p_space2 = doc_target.add_paragraph()
p_space2.paragraph_format.space_after = Pt(12)

# Section 2: Visual Class Diagram
h1_2 = doc_target.add_heading(level=1)
r = h1_2.add_run('2. Mô hình Lớp tổng thể (UML 2.5 Class Diagram)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_cd = doc_target.add_paragraph()
p_cd.paragraph_format.space_after = Pt(8)
r = p_cd.add_run('Sơ đồ Lớp dưới đây thể hiện cấu trúc 21 Lớp thuộc 5 Module nghiệp vụ, các stereotype, thuộc tính, phương thức và mối quan hệ phụ thuộc/hiệp hội giữa các lớp.')
fmt(r, size=9.5, italic=True, color=(51, 65, 85))

# Generate Class Diagram Image
class_img_path = draw_class_diagram('class_diagram_v2.png')
doc_target.add_picture(class_img_path, width=Inches(6.5))

p_cap = doc_target.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.paragraph_format.space_before = Pt(4)
p_cap.paragraph_format.space_after = Pt(10)
r_cap = p_cap.add_run('Hình — 2.1: Sơ đồ Lớp tổng thể UML 2.5 (5 Modules & 21 Classes)')
fmt(r_cap, size=8.5, italic=True, color=(100, 116, 139))

# Mermaid Source Code Block
h2_m = doc_target.add_heading(level=2)
r = h2_m.add_run('Mã Mermaid Class Diagram (Nguồn gốc)')
fmt(r, size=11, bold=True, color=(30, 41, 59))

mermaid_code = """classDiagram
    class UserAccount {
        +accountId: TBD
        +role: Role
        +hasRole(role)
    }
    class AuthService {
        +authenticate()
        +authorize()
    }
    class ParkingArea {
        +areaId: TBD
        +capacity: int
        +exposeAvailableCount()
    }
    class ParkingSlot {
        +slotId: TBD
        +status: SlotStatus
        +updateStatus()
    }
    class Vehicle {
        +identifier: String
        +formatIdentifier()
    }
    class ParkingVisit {
        +visitId: TBD
        +entryTime: DateTime
        +exitTime: DateTime
        +closeVisit()
        +setFee()
    }
    class PriceTable {
        +priceRuleId: TBD
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
    AuthService --> ParkingDataRepository : uses
    ParkingOperationService --> ParkingDataRepository : uses
"""
add_code_block(doc_target, mermaid_code)

# Section 3: 21 Detailed Class Specification Tables
doc_target.add_page_break()
h1_3 = doc_target.add_heading(level=1)
r = h1_3.add_run('3. Bảng Đặc tả Chi tiết 21 Lớp (Class Specifications)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

for c_info in CLASSES_DATA:
    p_cname = doc_target.add_paragraph()
    p_cname.paragraph_format.space_before = Pt(8)
    p_cname.paragraph_format.space_after = Pt(2)
    r_c = p_cname.add_run(f"{c_info['code']} — {c_info['name']} (<<{c_info['type']}>>)")
    fmt(r_c, size=11, bold=True, color=(37, 99, 235))
    
    tbl_c = doc_target.add_table(rows=7, cols=2)
    set_table_col_widths(tbl_c, [1.8, 4.7])
    
    fields = [
        ('Mã Lớp & Tên Lớp', f"{c_info['code']} | {c_info['name']}"),
        ('Loại Lớp & Module', f"<<{c_info['type']}>> | Module: {c_info['module']}"),
        ('Trách nhiệm (Responsibility)', c_info['resp']),
        ('Thuộc tính (Attributes)', c_info['attrs']),
        ('Phương thức (Methods)', c_info['methods']),
        ('Lớp phụ thuộc (Dependencies)', c_info['deps']),
        ('Ánh xạ Yêu cầu & Use Case', c_info['related'])
    ]
    
    for row_i, (k, v) in enumerate(fields):
        row = tbl_c.rows[row_i]
        set_cell(row.cells[0], k, bold=True, size=8.5, color=(15, 23, 42))
        shade_cell(row.cells[0], 'F1F5F9')
        set_cell(row.cells[1], v, bold=False, size=8.5)
        
    p_space_c = doc_target.add_paragraph()
    p_space_c.paragraph_format.space_after = Pt(4)

# Section 4: Sequence Interaction Summaries
doc_target.add_page_break()
h1_4 = doc_target.add_heading(level=1)
r = h1_4.add_run('4. Chuỗi Tương tác Đối tượng (Sequence Summaries)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

seq_data = [
    ('SEQ-001 Đăng nhập & Xác thực', 'Actor -> Login Boundary -> AuthService -> ParkingDataRepository -> UserAccount -> Login Boundary. Nếu sai mật khẩu hoặc lỗi CSDL, AuthService trả về phản hồi từ chối.', 'UC-001, FR-001, SR-001'),
    ('SEQ-002 Xe ra & Tính phí gửi xe', 'Nhân viên -> Parking Boundary -> ParkingOperationService -> ParkingDataRepository / ParkingVisit -> PriceTable.calculateFor() -> ParkingDataRepository -> Boundary mở barie.', 'UC-004, FR-004, BR-001'),
    ('SEQ-003 AI Sinh báo cáo lưu lượng', 'Quản lý -> AI Boundary -> AIAnalysisService -> StatisticsContextProvider -> ReportingService / ParkingDataRepository -> PromptTemplate -> AIAdapter -> AIResponseValidator -> AI Boundary.', 'UC-009, AIR-001, NFR-003')
]

tbl_seq = doc_target.add_table(rows=1, cols=3)
set_table_col_widths(tbl_seq, [1.8, 3.5, 1.2])
for c, h in zip(tbl_seq.rows[0].cells, ['Kịch bản Sequence', 'Chuỗi tương tác các Lớp (Call Flow)', 'Ánh xạ']):
    set_cell(c, h, bold=True, size=9, color=(255, 255, 255))
    shade_cell(c, '1E293B')

for s_name, s_flow, s_map in seq_data:
    row = tbl_seq.add_row()
    set_cell(row.cells[0], s_name, bold=True, size=8.5)
    set_cell(row.cells[1], s_flow, bold=False, size=8.5)
    set_cell(row.cells[2], s_map, bold=False, size=8.5)

p_space4 = doc_target.add_paragraph()
p_space4.paragraph_format.space_after = Pt(12)

# Section 5: State Machine Diagram
h1_5 = doc_target.add_heading(level=1)
r = h1_5.add_run('5. Sơ đồ Chuyển trạng thái Vị trí đỗ (State Machine Diagram)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_std = doc_target.add_paragraph()
p_std.paragraph_format.space_after = Pt(8)
r = p_std.add_run('STD-001: Biểu diễn vòng đời chuyển trạng thái của đối tượng `ParkingSlot` giữa 2 trạng thái `Available` (Chỗ trống) và `Occupied` (Có xe đỗ).')
fmt(r, size=9.5, italic=True, color=(51, 65, 85))

# Generate State Machine Image
std_img_path = draw_state_machine_diagram('state_machine_v2.png')
doc_target.add_picture(std_img_path, width=Inches(6.5))

p_cap2 = doc_target.add_paragraph()
p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap2.paragraph_format.space_before = Pt(4)
p_cap2.paragraph_format.space_after = Pt(10)
r_cap2 = p_cap2.add_run('Hình — 5.1: Sơ đồ chuyển trạng thái STD-001 đối tượng ParkingSlot')
fmt(r_cap2, size=8.5, italic=True, color=(100, 116, 139))

# Section 6: Design Decisions & Assumptions
doc_target.add_page_break()
h1_6 = doc_target.add_heading(level=1)
r = h1_6.add_run('6. Các Quyết định Thiết kế (Design Decisions) & Giả định (DASM)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

dd_data = [
    ('DD-001', 'Tách 4 tầng Presentation / Application / Domain / Data Access', 'Giảm độ gắn kết (coupling), đảm bảo dịch vụ nghiệp vụ không phụ thuộc vào giao diện hay công cụ lưu trữ CSDL cụ thể.'),
    ('DD-002', 'Dùng ParkingVisit làm Aggregate Entity trung tâm', 'Tập hợp thông tin phương tiện, vé xe, vị trí đỗ và thời gian gửi; ngăn chặn việc dồn logic xe vào/ra quá tải vào Vehicle hoặc Ticket.'),
    ('DD-003', 'Áp dụng Adapter Pattern cho AI Integration (AIAdapter)', 'Cô lập nhà cung cấp AI engine (OpenAI/Gemini/Claude/Ollama), giảm tác động khi thay đổi mô hình hoặc cấu hình API key.'),
    ('DD-004', 'Tách biệt PromptTemplate, ContextProvider & ResponseValidator', 'Đảm bảo tuân thủ nghiêm ngặt guardrails chống bịa số liệu (BR-002, SR-003), xử lý fallback an toàn khi AI timeout/rate limit.')
]

tbl_dd = doc_target.add_table(rows=1, cols=3)
set_table_col_widths(tbl_dd, [1.0, 2.2, 3.3])
for c, h in zip(tbl_dd.rows[0].cells, ['Mã DD', 'Quyết định Thiết kế', 'Lý do & Lợi ích Kiến trúc']):
    set_cell(c, h, bold=True, size=9, color=(255, 255, 255))
    shade_cell(c, '1E293B')

for code, decision, rationale in dd_data:
    row = tbl_dd.add_row()
    set_cell(row.cells[0], code, bold=True, size=8.5)
    set_cell(row.cells[1], decision, bold=False, size=8.5)
    set_cell(row.cells[2], rationale, bold=False, size=8.5)

p_space6 = doc_target.add_paragraph()
p_space6.paragraph_format.space_after = Pt(12)

# Section 7: Design Traceability Matrix
h1_7 = doc_target.add_heading(level=1)
r = h1_7.add_run('7. Ma trận Truy vết Thiết kế (Design Traceability Matrix)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

trace_data = [
    ('FR-001 (Đăng nhập)', 'UC-001', 'CLS-001 (UserAccount), CLS-011 (AuthService), CLS-021 (Repository)', 'MOD-001 Access', 'SEQ-001'),
    ('FR-002 (Danh mục bãi đỗ)', 'UC-002', 'CLS-002 (Area), CLS-003 (Slot), CLS-004 (Type), CLS-012 (Service)', 'MOD-002 Catalog', 'ACTD-001'),
    ('FR-003 (Xe vào bãi)', 'UC-003', 'CLS-005 (Vehicle), CLS-006 (Ticket), CLS-007 (Visit), CLS-013 (Service)', 'MOD-003 Operation', 'ACTD-001'),
    ('FR-004 (Xe ra & phí)', 'UC-004', 'CLS-007 (Visit), CLS-008 (PriceTable), CLS-013 (OperationService)', 'MOD-003 Operation', 'SEQ-002'),
    ('FR-005 (Theo dõi chỗ)', 'UC-005', 'CLS-003 (ParkingSlot), CLS-013 (OperationService)', 'MOD-002 / MOD-003', 'STD-001'),
    ('FR-006 (Tra cứu lượt gửi)', 'UC-006', 'CLS-014 (ParkingSearchService), CLS-007 (Visit), CLS-021 (Repo)', 'MOD-004 Report', 'SEQ-002'),
    ('FR-007 (Vé tháng)', 'UC-007', 'CLS-009 (MonthlyPass), CLS-012 (ParkingCatalogService)', 'MOD-002 Catalog', 'ACTD-001'),
    ('FR-008 (Thống kê)', 'UC-008', 'CLS-010 (ParkingStatistics), CLS-015 (ReportingService)', 'MOD-004 Report', 'SEQ-003'),
    ('AIR-001..003 (AI)', 'UC-009..011', 'CLS-016 (AIService), CLS-017 (Prompt), CLS-018 (Context), CLS-019 (Adapter)', 'MOD-005 AI', 'SEQ-003')
]

tbl_tr = doc_target.add_table(rows=1, cols=5)
set_table_col_widths(tbl_tr, [1.4, 0.9, 2.2, 1.1, 0.9])
for c, h in zip(tbl_tr.rows[0].cells, ['Yêu cầu (FR/AIR)', 'Use Case', 'Các Lớp thiết kế (Classes)', 'Module', 'Sơ đồ tương tác']):
    set_cell(c, h, bold=True, size=8.5, color=(255, 255, 255))
    shade_cell(c, '1E293B')

for req, uc, cls_str, mod, seq in trace_data:
    row = tbl_tr.add_row()
    set_cell(row.cells[0], req, bold=True, size=8)
    set_cell(row.cells[1], uc, bold=False, size=8)
    set_cell(row.cells[2], cls_str, bold=False, size=8)
    set_cell(row.cells[3], mod, bold=False, size=8)
    set_cell(row.cells[4], seq, bold=False, size=8)

# Output Path
out_doc_path = Path('04_GenAI_SoftwareDevelopment_object-oriented-design_v2.0.docx')
try:
    doc_target.save(out_doc_path)
    print('====================================================')
    print(f'SUCCESS! File saved to: {out_doc_path.resolve()}')
    print('====================================================')
except PermissionError:
    alt_path = Path('04_GenAI_SoftwareDevelopment_object-oriented-design_v2.0_fixed.docx')
    doc_target.save(alt_path)
    print('====================================================')
    print(f'File đang mở trong Word! Đã lưu tạm sang: {alt_path.resolve()}')
    print('====================================================')

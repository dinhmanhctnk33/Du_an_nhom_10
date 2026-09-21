import sys
import os
import sqlite3
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

ASSETS_DIR = Path('csdl_assets')
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
# Image Generator: Visual ERD Engine
# ---------------------------------------------------------
def draw_erd_diagram(output_filename):
    width = 1600
    height = 1100
    
    img = Image.new('RGB', (width, height), 'white')
    d = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 24)
        font_entity = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 17)
        font_attr = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
        font_pk = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 14)
    except OSError:
        font_title = font_entity = font_attr = font_pk = ImageFont.load_default()
        
    # Title Box
    d.rounded_rectangle((20, 15, width - 20, 65), radius=8, fill='#F1F5F9', outline='#0F172A', width=2)
    d.text((35, 25), 'Sơ đồ Thực thể Liên kết (Entity-Relationship Diagram — ERD 11 Entities)', font=font_title, fill='#0F172A')
    
    # Helper to draw Entity Box
    def draw_entity_box(cx, cy, cw, ch, ename, attrs, bg_col='#EFF6FF', bd_col='#2563EB'):
        d.rectangle((cx, cy, cx + cw, cy + ch), fill='white', outline=bd_col, width=2)
        # Header
        header_h = 36
        d.rectangle((cx, cy, cx + cw, cy + header_h), fill=bg_col, outline=bd_col, width=1)
        d.text((cx + 10, cy + 8), ename, font=font_entity, fill='#0F172A')
        
        # Attributes
        curr_y = cy + header_h + 6
        for is_pk, is_fk, aname, atype in attrs:
            prefix = "[PK] " if is_pk else ("[FK] " if is_fk else " • ")
            f = font_pk if (is_pk or is_fk) else font_attr
            col = '#2563EB' if is_pk else ('#D97706' if is_fk else '#334155')
            d.text((cx + 8, curr_y), f"{prefix}{aname}: {atype}", font=f, fill=col)
            curr_y += 18

    # Row 1 Entities
    draw_entity_box(40, 85, 270, 160, 'VaiTro', [(True, False, 'MaVaiTro', 'INT'), (False, False, 'TenVaiTro', 'TEXT'), (False, False, 'MoTa', 'TEXT')], '#EFF6FF', '#2563EB')
    draw_entity_box(340, 85, 300, 180, 'NguoiDung', [(True, False, 'MaNguoiDung', 'INT'), (False, True, 'MaVaiTro', 'INT'), (False, False, 'TenDangNhap', 'TEXT'), (False, False, 'HoTen', 'TEXT')], '#EFF6FF', '#2563EB')
    draw_entity_box(670, 85, 270, 160, 'KhuVuc', [(True, False, 'MaKhuVuc', 'INT'), (False, False, 'TenKhuVuc', 'TEXT'), (False, False, 'SucChuaToiDa', 'INT')], '#F0FDF4', '#16A34A')
    draw_entity_box(970, 85, 270, 180, 'ViTriDo', [(True, False, 'MaViTri', 'INT'), (False, True, 'MaKhuVuc', 'INT'), (False, True, 'MaLoaiXe', 'INT'), (False, False, 'TrangThai', 'TEXT')], '#F0FDF4', '#16A34A')
    draw_entity_box(1270, 85, 280, 160, 'LoaiXe', [(True, False, 'MaLoaiXe', 'INT'), (False, False, 'TenLoaiXe', 'TEXT'), (False, False, 'MoTa', 'TEXT')], '#FFFBEB', '#D97706')

    # Row 2 Entities
    draw_entity_box(40, 390, 270, 180, 'TheXe', [(True, False, 'MaThe', 'INT'), (False, False, 'MaDinhDanhThe', 'TEXT'), (False, False, 'LoaiThe', 'TEXT'), (False, False, 'TrangThaiThe', 'TEXT')], '#FFFBEB', '#D97706')
    draw_entity_box(340, 340, 420, 270, 'LuotGuiXe (Junction)', [(True, False, 'MaLuotGui', 'INT'), (False, True, 'MaThe', 'INT'), (False, True, 'MaViTri', 'INT'), (False, True, 'MaPhuongTien', 'INT'), (False, False, 'BienSoXeKiemTra', 'TEXT'), (False, False, 'ThoiGianVao', 'DATETIME'), (False, False, 'ThoiGianRa', 'DATETIME'), (False, False, 'TongTienPhi', 'DECIMAL'), (False, False, 'TrangThaiLuot', 'TEXT')], '#FEF2F2', '#DC2626')
    draw_entity_box(790, 390, 320, 200, 'PhuongTien', [(True, False, 'MaPhuongTien', 'INT'), (False, True, 'MaLoaiXe', 'INT'), (False, False, 'BienSoXe', 'TEXT'), (False, False, 'MauXe', 'TEXT')], '#F5F3FF', '#7C3AED')
    draw_entity_box(1140, 390, 410, 200, 'VeThang', [(True, False, 'MaVeThang', 'INT'), (False, True, 'MaThe', 'INT'), (False, True, 'MaPhuongTien', 'INT'), (False, False, 'HoTenKhachHang', 'TEXT'), (False, False, 'NgayBatDau', 'DATE'), (False, False, 'NgayKetThuc', 'DATE')], '#F5F3FF', '#7C3AED')

    # Row 3 Entities
    draw_entity_box(340, 680, 420, 220, 'BangGia', [(True, False, 'MaBangGia', 'INT'), (False, True, 'MaLoaiXe', 'INT'), (False, False, 'LoaiApDung', 'TEXT'), (False, False, 'GiaCoBan', 'DECIMAL'), (False, False, 'GiaTangThem', 'DECIMAL'), (False, False, 'GiaBanDem', 'DECIMAL')], '#FFFBEB', '#D97706')
    draw_entity_box(790, 680, 420, 220, 'BaoCaoThongKe', [(True, False, 'MaBaoCao', 'INT'), (False, True, 'MaKhuVuc', 'INT'), (False, False, 'LoaiBaoCao', 'TEXT'), (False, False, 'TongLuotXe', 'INT'), (False, False, 'TongDoanhThu', 'DECIMAL'), (False, False, 'KhungGioCaoDiem', 'TEXT')], '#F8FAFC', '#475569')

    # Connecting Lines
    d.line((310, 140, 340, 140), fill='#2563EB', width=2) # VaiTro -> NguoiDung
    d.line((940, 140, 970, 140), fill='#16A34A', width=2) # KhuVuc -> ViTriDo
    d.line((1240, 140, 1270, 140), fill='#D97706', width=2) # ViTriDo -> LoaiXe
    d.line((175, 245, 175, 390), fill='#D97706', width=2) # NguoiDung -> LuotGuiXe
    d.line((550, 265, 550, 340), fill='#DC2626', width=2) # NguoiDung -> LuotGuiXe
    d.line((760, 475, 790, 475), fill='#7C3AED', width=2) # LuotGuiXe -> PhuongTien
    d.line((1110, 475, 1140, 475), fill='#7C3AED', width=2) # PhuongTien -> VeThang
    
    out_path = ASSETS_DIR / output_filename
    img.save(out_path)
    return str(out_path)

# ---------------------------------------------------------
# Test & Verify SQLite Schema DDL
# ---------------------------------------------------------
def test_sqlite_ddl():
    print('Testing SQLite DDL Schema in Python in-memory database...')
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    sql_script = """
    CREATE TABLE VaiTro (
        MaVaiTro INTEGER PRIMARY KEY AUTOINCREMENT,
        TenVaiTro VARCHAR(50) NOT NULL UNIQUE,
        MoTa VARCHAR(255)
    );

    CREATE TABLE NguoiDung (
        MaNguoiDung INTEGER PRIMARY KEY AUTOINCREMENT,
        TenDangNhap VARCHAR(50) NOT NULL UNIQUE,
        MatKhauMaHoa VARCHAR(255) NOT NULL,
        HoTen VARCHAR(100) NOT NULL,
        SoDienThoai VARCHAR(20),
        MaVaiTro INTEGER NOT NULL,
        TrangThai VARCHAR(20) DEFAULT 'HoatDong',
        NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (MaVaiTro) REFERENCES VaiTro(MaVaiTro)
    );

    CREATE TABLE KhuVuc (
        MaKhuVuc INTEGER PRIMARY KEY AUTOINCREMENT,
        TenKhuVuc VARCHAR(100) NOT NULL,
        SucChuaToiDa INTEGER NOT NULL CHECK (SucChuaToiDa > 0),
        MoTa VARCHAR(255)
    );

    CREATE TABLE LoaiXe (
        MaLoaiXe INTEGER PRIMARY KEY AUTOINCREMENT,
        TenLoaiXe VARCHAR(50) NOT NULL UNIQUE,
        MoTa VARCHAR(255)
    );

    CREATE TABLE ViTriDo (
        MaViTri INTEGER PRIMARY KEY AUTOINCREMENT,
        MaKhuVuc INTEGER NOT NULL,
        MaLoaiXe INTEGER,
        TenViTri VARCHAR(50) NOT NULL,
        TrangThai VARCHAR(20) NOT NULL DEFAULT 'Trong' CHECK (TrangThai IN ('Trong', 'DaDo', 'BaoTri')),
        FOREIGN KEY (MaKhuVuc) REFERENCES KhuVuc(MaKhuVuc),
        FOREIGN KEY (MaLoaiXe) REFERENCES LoaiXe(MaLoaiXe)
    );

    CREATE TABLE PhuongTien (
        MaPhuongTien INTEGER PRIMARY KEY AUTOINCREMENT,
        BienSoXe VARCHAR(20) NOT NULL,
        MaLoaiXe INTEGER NOT NULL,
        MauXe VARCHAR(50),
        MoTa VARCHAR(255),
        FOREIGN KEY (MaLoaiXe) REFERENCES LoaiXe(MaLoaiXe)
    );

    CREATE TABLE TheXe (
        MaThe INTEGER PRIMARY KEY AUTOINCREMENT,
        MaDinhDanhThe VARCHAR(50) NOT NULL UNIQUE,
        LoaiThe VARCHAR(20) NOT NULL CHECK (LoaiThe IN ('VeLuot', 'VeThang')),
        TrangThaiThe VARCHAR(20) NOT NULL DEFAULT 'SanSang' CHECK (TrangThaiThe IN ('SanSang', 'DangGui', 'BiKhoa', 'DaHuy'))
    );

    CREATE TABLE LuotGuiXe (
        MaLuotGui INTEGER PRIMARY KEY AUTOINCREMENT,
        MaThe INTEGER NOT NULL,
        MaPhuongTien INTEGER,
        BienSoXeKiemTra VARCHAR(20) NOT NULL,
        MaViTri INTEGER NOT NULL,
        ThoiGianVao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        ThoiGianRa DATETIME,
        MaNguoiDungVao INTEGER NOT NULL,
        MaNguoiDungRa INTEGER,
        TongTienPhi DECIMAL(12, 2) DEFAULT 0.00,
        TrangThaiLuot VARCHAR(20) NOT NULL DEFAULT 'DangGui' CHECK (TrangThaiLuot IN ('DangGui', 'DaHoanTat', 'BiSuCo')),
        FOREIGN KEY (MaThe) REFERENCES TheXe(MaThe),
        FOREIGN KEY (MaPhuongTien) REFERENCES PhuongTien(MaPhuongTien),
        FOREIGN KEY (MaViTri) REFERENCES ViTriDo(MaViTri),
        FOREIGN KEY (MaNguoiDungVao) REFERENCES NguoiDung(MaNguoiDung),
        FOREIGN KEY (MaNguoiDungRa) REFERENCES NguoiDung(MaNguoiDung),
        CHECK (ThoiGianRa IS NULL OR ThoiGianRa >= ThoiGianVao)
    );

    CREATE TABLE BangGia (
        MaBangGia INTEGER PRIMARY KEY AUTOINCREMENT,
        MaLoaiXe INTEGER NOT NULL,
        LoaiApDung VARCHAR(20) NOT NULL CHECK (LoaiApDung IN ('VeLuot', 'VeThang')),
        GiaCoBan DECIMAL(12, 2) NOT NULL CHECK (GiaCoBan >= 0),
        DonViThoiGianPhut INTEGER DEFAULT 60,
        GiaTangThem DECIMAL(12, 2) DEFAULT 0.00,
        GiaBanDem DECIMAL(12, 2) DEFAULT 0.00,
        NgayApDung DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (MaLoaiXe) REFERENCES LoaiXe(MaLoaiXe)
    );

    CREATE TABLE VeThang (
        MaVeThang INTEGER PRIMARY KEY AUTOINCREMENT,
        MaThe INTEGER NOT NULL,
        MaPhuongTien INTEGER NOT NULL,
        HoTenKhachHang VARCHAR(100) NOT NULL,
        SoDienThoai VARCHAR(20),
        NgayBatDau DATE NOT NULL,
        NgayKetThuc DATE NOT NULL,
        MoiGiaHan BOOLEAN DEFAULT 1,
        TrangThaiVe VARCHAR(20) DEFAULT 'HieuLuc' CHECK (TrangThaiVe IN ('HieuLuc', 'HetHan', 'Huy')),
        FOREIGN KEY (MaThe) REFERENCES TheXe(MaThe),
        FOREIGN KEY (MaPhuongTien) REFERENCES PhuongTien(MaPhuongTien)
    );

    CREATE TABLE BaoCaoThongKe (
        MaBaoCao INTEGER PRIMARY KEY AUTOINCREMENT,
        LoaiBaoCao VARCHAR(20) NOT NULL CHECK (LoaiBaoCao IN ('Ngay', 'Tuan', 'Thang')),
        NgayBatDau DATE NOT NULL,
        NgayKetThuc DATE NOT NULL,
        MaKhuVuc INTEGER,
        TongLuotXe INTEGER DEFAULT 0,
        TongDoanhThu DECIMAL(14, 2) DEFAULT 0.00,
        TyLeLapDayTrungBinh DECIMAL(5, 2) DEFAULT 0.00,
        KhungGioCaoDiem VARCHAR(255),
        NgayTao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (MaKhuVuc) REFERENCES KhuVuc(MaKhuVuc)
    );

    CREATE INDEX idx_luotgui_bienso ON LuotGuiXe(BienSoXeKiemTra);
    CREATE INDEX idx_luotgui_thoigian ON LuotGuiXe(ThoiGianVao, ThoiGianRa);
    CREATE INDEX idx_luotgui_trangthai ON LuotGuiXe(TrangThaiLuot);
    CREATE INDEX idx_vitrido_trangthai ON ViTriDo(MaKhuVuc, TrangThai);
    CREATE INDEX idx_thexe_madinhdanh ON TheXe(MaDinhDanhThe);
    CREATE INDEX idx_vethang_ngay ON VeThang(NgayBatDau, NgayKetThuc, TrangThaiVe);
    """
    
    cursor.executescript(sql_script)
    conn.commit()
    
    # Check tables created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cursor.fetchall() if r[0] != 'sqlite_sequence']
    print(f'SQLite Execution Successful! Total 11 Tables Created: {tables}')
    conn.close()
    return sql_script

# ---------------------------------------------------------
# Build CSDL_v1.0.docx
# ---------------------------------------------------------
print('Starting document assembly for CSDL_v1.0.docx...')
sql_script_full = test_sqlite_ddl()

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
r_sub = p_sub.add_run('THIẾT KẾ CƠ SỞ DỮ LIỆU TÍCH HỢP AI (CHAIN-OF-THOUGHT DATABASE DESIGN v1.0)')
fmt(r_sub, size=14, bold=True, color=(37, 99, 235))

p_sub2 = doc_target.add_paragraph()
r_sub2 = p_sub2.add_run('Đặc tả Lược đồ SQLite, ERD, Ràng buộc Toàn vẹn & Tối ưu hóa Chỉ mục Báo cáo')
fmt(r_sub2, size=10.5, italic=True, color=(71, 85, 105))

# Document Metadata Table
tbl_meta = doc_target.add_table(rows=4, cols=2)
set_table_col_widths(tbl_meta, [2.0, 4.5])
meta_data = [
    ('Nguồn tham chiếu', '02-CoT-Thiet-ke-CSDL.md, project.md & Đặc tả UC (Nhóm 10)'),
    ('Phương pháp thiết kế', 'Chain-of-Thought (CoT) 6 bước suy luận toàn diện'),
    ('Hệ quản trị CSDL', 'SQLite 3 (Tối ưu hóa cho phiên bản Demo & Triển khai nhẹ)'),
    ('Quy tắc an toàn AI', 'Không lưu API Key trong CSDL; Không đưa dữ liệu nhạy cảm vào AI Prompt')
]
for i, (k, v) in enumerate(meta_data):
    row = tbl_meta.rows[i]
    set_cell(row.cells[0], k, bold=True, size=9, color=(15, 23, 42))
    shade_cell(row.cells[0], 'F1F5F9')
    set_cell(row.cells[1], v, bold=False, size=9)

p_space = doc_target.add_paragraph()
p_space.paragraph_format.space_after = Pt(12)

# PART 1: ENTITIES & REASONING
h1_1 = doc_target.add_heading(level=1)
r = h1_1.add_run('Phần 1: Danh sách Thực thể (Entities) & Lý do Tồn tại')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_p1 = doc_target.add_paragraph()
p_p1.paragraph_format.line_spacing = 1.15
r = p_p1.add_run(
    'Dựa trên phương pháp Chain-of-Thought (CoT), hệ thống xác định 11 Thực thể (Entities) chính. '
    'Tất cả tên thực thể được đặt bằng Tiếng Việt rõ nghĩa nhằm đảm bảo sự nhất quán trong toàn bộ tài liệu thiết kế và lập trình.'
)
fmt(r, size=10, color=(30, 41, 59))

tbl_ent = doc_target.add_table(rows=1, cols=4)
set_table_col_widths(tbl_ent, [1.5, 1.4, 2.4, 1.2])
for c, h in zip(tbl_ent.rows[0].cells, ['Mã Thực thể', 'Tên Thực thể (Tiếng Việt)', 'Lý do Tồn tại & Vai trò Nghiệp vụ', 'Phân nhóm']):
    set_cell(c, h, bold=True, size=9, color=(255, 255, 255))
    shade_cell(c, '1E293B')

entities_info = [
    ('ENT-001', 'NguoiDung', 'Lưu trữ tài khoản, mật khẩu mã hóa hash và thông tin cá nhân của nhân viên/quản lý.', 'Hệ thống'),
    ('ENT-002', 'VaiTro', 'Định nghĩa danh mục vai trò người dùng (Quản lý, Nhân viên bãi xe) để phân quyền.', 'Phân quyền'),
    ('ENT-003', 'KhuVuc', 'Quản lý thông tin các khu vực đỗ xe trong bãi (Khu A, Khu B, Tầng 1, Tầng 2).', 'Danh mục'),
    ('ENT-004', 'ViTriDo', 'Quản lý vị trí đỗ xe cụ thể và trạng thái theo dõi chỗ trống (Trong, DaDo, BaoTri).', 'Danh mục'),
    ('ENT-005', 'LoaiXe', 'Phân loại phương tiện (Xe máy, Ô tô 4-7 chỗ, Xe điện...) phục vụ tính phí và xếp chỗ.', 'Danh mục'),
    ('ENT-006', 'PhuongTien', 'Lưu trữ định danh phương tiện gửi xe (Biển số xe, màu xe, mô tả).', 'Vận hành'),
    ('ENT-007', 'TheXe', 'Quản lý mã định danh thẻ/vé (RFID/QR), loại thẻ (Vé lượt, Vé tháng) và trạng thái.', 'Vận hành'),
    ('ENT-008', 'LuotGuiXe', 'Thực thể giao dịch trung tâm lưu lịch sử xe vào/ra, giờ vào/ra, vị trí và số tiền phí.', 'Giao dịch'),
    ('ENT-009', 'BangGia', 'Cung cấp quy tắc tính phí theo loại xe, khung giờ ban ngày/ban đêm và phí lũy tiến.', 'Cấu hình'),
    ('ENT-010', 'VeThang', 'Quản lý thông tin đăng ký vé tháng của khách quen và thời hạn hiệu lực.', 'Khách hàng'),
    ('ENT-011', 'BaoCaoThongKe', 'Đóng gói dữ liệu tổng hợp lưu lượng, doanh thu và khung giờ cao điểm cho AI.', 'Báo cáo & AI')
]

for ecode, ename, eresp, egroup in entities_info:
    row = tbl_ent.add_row()
    set_cell(row.cells[0], ecode, bold=True, size=8.5)
    set_cell(row.cells[1], ename, bold=True, size=8.5, color=(37, 99, 235))
    set_cell(row.cells[2], eresp, bold=False, size=8.5)
    set_cell(row.cells[3], egroup, bold=False, size=8.5)

p_space1 = doc_target.add_paragraph()
p_space1.paragraph_format.space_after = Pt(12)

# PART 2: DATABASE TABLES DESIGN & SQL DDL
doc_target.add_page_break()
h1_2 = doc_target.add_heading(level=1)
r = h1_2.add_run('Phần 2: Bảng Thiết kế CSDL Chi tiết & Lược đồ SQL DDL')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_p2 = doc_target.add_paragraph()
p_p2.paragraph_format.space_after = Pt(8)
r = p_p2.add_run('Dưới đây là đặc tả chi tiết 11 bảng CSDL bao gồm các thuộc tính tiếng Việt, kiểu dữ liệu SQLite, khóa chính (PK), khóa ngoại (FK) và các ràng buộc dữ liệu.')
fmt(r, size=9.5, italic=True, color=(51, 65, 85))

tables_detail = [
    ('Bảng 1: NguoiDung (Người dùng hệ thống)', [
        ('MaNguoiDung', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã người dùng duy nhất'),
        ('TenDangNhap', 'VARCHAR(50)', 'NOT NULL, UNIQUE', 'Tên tài khoản đăng nhập'),
        ('MatKhauMaHoa', 'VARCHAR(255)', 'NOT NULL', 'Mật khẩu đã mã hóa hash (Bcrypt)'),
        ('HoTen', 'VARCHAR(100)', 'NOT NULL', 'Họ và tên người dùng'),
        ('SoDienThoai', 'VARCHAR(20)', 'NULL', 'Số điện thoại liên hệ'),
        ('MaVaiTro', 'INTEGER', 'FK -> VaiTro(MaVaiTro)', 'Khóa ngoại liên kết vai trò'),
        ('TrangThai', 'VARCHAR(20)', "DEFAULT 'HoatDong'", 'Trạng thái tài khoản'),
        ('NgayTao', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Thời điểm tạo tài khoản')
    ]),
    ('Bảng 2: VaiTro (Danh mục vai trò)', [
        ('MaVaiTro', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã vai trò duy nhất'),
        ('TenVaiTro', 'VARCHAR(50)', 'NOT NULL, UNIQUE', 'Tên vai trò (QuanLy, NhanVien)'),
        ('MoTa', 'VARCHAR(255)', 'NULL', 'Mô tả quyền hạn vai trò')
    ]),
    ('Bảng 3: KhuVuc (Khu vực đỗ xe)', [
        ('MaKhuVuc', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã khu vực đỗ xe'),
        ('TenKhuVuc', 'VARCHAR(100)', 'NOT NULL', 'Tên khu vực (Khu A, Khu B...)'),
        ('SucChuaToiDa', 'INTEGER', 'NOT NULL, CHECK (>0)', 'Sức chứa tối đa của khu vực'),
        ('MoTa', 'VARCHAR(255)', 'NULL', 'Mô tả thêm về khu vực')
    ]),
    ('Bảng 4: ViTriDo (Vị trí đỗ xe)', [
        ('MaViTri', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã vị trí đỗ xe'),
        ('MaKhuVuc', 'INTEGER', 'FK -> KhuVuc(MaKhuVuc)', 'Thuộc khu vực nào'),
        ('MaLoaiXe', 'INTEGER', 'FK -> LoaiXe(MaLoaiXe), NULL', 'Loại xe ưu tiên cho vị trí này'),
        ('TenViTri', 'VARCHAR(50)', 'NOT NULL', 'Mã tên vị trí (A-01, A-02...)'),
        ('TrangThai', 'VARCHAR(20)', "DEFAULT 'Trong', CHECK", 'Trạng thái: Trong, DaDo, BaoTri')
    ]),
    ('Bảng 5: LoaiXe (Loại phương tiện)', [
        ('MaLoaiXe', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã loại xe duy nhất'),
        ('TenLoaiXe', 'VARCHAR(50)', 'NOT NULL, UNIQUE', 'Tên loại xe (XeMay, Ot4Cho...)'),
        ('MoTa', 'VARCHAR(255)', 'NULL', 'Mô tả chi tiết loại xe')
    ]),
    ('Bảng 6: PhuongTien (Thông tin xe gửi)', [
        ('MaPhuongTien', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã phương tiện duy nhất'),
        ('BienSoXe', 'VARCHAR(20)', 'NOT NULL', 'Biển số xe gửi'),
        ('MaLoaiXe', 'INTEGER', 'FK -> LoaiXe(MaLoaiXe)', 'Phân loại phương tiện'),
        ('MauXe', 'VARCHAR(50)', 'NULL', 'Màu sắc phương tiện'),
        ('MoTa', 'VARCHAR(255)', 'NULL', 'Đặc điểm nhận dạng thêm')
    ]),
    ('Bảng 7: TheXe (Thẻ/Vé xe)', [
        ('MaThe', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã thẻ xe hệ thống'),
        ('MaDinhDanhThe', 'VARCHAR(50)', 'NOT NULL, UNIQUE', 'Mã định danh thẻ (RFID/Mã vạch)'),
        ('LoaiThe', 'VARCHAR(20)', 'NOT NULL, CHECK', 'Loại thẻ: VeLuot, VeThang'),
        ('TrangThaiThe', 'VARCHAR(20)', "DEFAULT 'SanSang'", 'Trạng thái: SanSang, DangGui, BiKhoa')
    ]),
    ('Bảng 8: LuotGuiXe (Giao dịch xe vào/ra)', [
        ('MaLuotGui', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã lượt gửi xe duy nhất'),
        ('MaThe', 'INTEGER', 'FK -> TheXe(MaThe)', 'Mã thẻ xe sử dụng'),
        ('MaPhuongTien', 'INTEGER', 'FK -> PhuongTien, NULL', 'Mã phương tiện (nếu có trong CSDL)'),
        ('BienSoXeKiemTra', 'VARCHAR(20)', 'NOT NULL', 'Biển số xe nhận diện lúc vào'),
        ('MaViTri', 'INTEGER', 'FK -> ViTriDo(MaViTri)', 'Vị trí đỗ xe được phân bổ'),
        ('ThoiGianVao', 'DATETIME', 'NOT NULL, DEFAULT NOW', 'Thời điểm xe vào bãi'),
        ('ThoiGianRa', 'DATETIME', 'NULLABLE', 'Thời điểm xe ra khỏi bãi'),
        ('MaNguoiDungVao', 'INTEGER', 'FK -> NguoiDung', 'Nhân viên ghi nhận xe vào'),
        ('MaNguoiDungRa', 'INTEGER', 'FK -> NguoiDung, NULL', 'Nhân viên ghi nhận xe ra'),
        ('TongTienPhi', 'DECIMAL(12,2)', 'DEFAULT 0.00', 'Số tiền phí gửi xe đã tính'),
        ('TrangThaiLuot', 'VARCHAR(20)', "DEFAULT 'DangGui'", 'Trạng thái: DangGui, DaHoanTat, BiSuCo')
    ]),
    ('Bảng 9: BangGia (Bảng giá tính phí)', [
        ('MaBangGia', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã quy tắc bảng giá'),
        ('MaLoaiXe', 'INTEGER', 'FK -> LoaiXe(MaLoaiXe)', 'Áp dụng cho loại xe nào'),
        ('LoaiApDung', 'VARCHAR(20)', 'NOT NULL, CHECK', 'Loại áp dụng: VeLuot, VeThang'),
        ('GiaCoBan', 'DECIMAL(12,2)', 'NOT NULL, CHECK(>=0)', 'Giá khởi điểm / giá cơ bản'),
        ('DonViThoiGianPhut', 'INTEGER', 'DEFAULT 60', 'Đơn vị tính (số phút)'),
        ('GiaTangThem', 'DECIMAL(12,2)', 'DEFAULT 0.00', 'Phí lũy tiến tăng thêm theo đơn vị'),
        ('GiaBanDem', 'DECIMAL(12,2)', 'DEFAULT 0.00', 'Phụ phí ban đêm (nếu có)'),
        ('NgayApDung', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Thời điểm hiệu lực bảng giá')
    ]),
    ('Bảng 10: VeThang (Đăng ký vé tháng)', [
        ('MaVeThang', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã đăng ký vé tháng'),
        ('MaThe', 'INTEGER', 'FK -> TheXe(MaThe)', 'Thẻ xe gắn với vé tháng'),
        ('MaPhuongTien', 'INTEGER', 'FK -> PhuongTien', 'Phương tiện đăng ký vé tháng'),
        ('HoTenKhachHang', 'VARCHAR(100)', 'NOT NULL', 'Họ tên chủ phương tiện'),
        ('SoDienThoai', 'VARCHAR(20)', 'NULL', 'Số điện thoại khách hàng'),
        ('NgayBatDau', 'DATE', 'NOT NULL', 'Ngày bắt đầu hiệu lực vé'),
        ('NgayKetThuc', 'DATE', 'NOT NULL', 'Ngày hết hạn hiệu lực vé'),
        ('MoiGiaHan', 'BOOLEAN', 'DEFAULT TRUE', 'Trạng thái gia hạn thành công'),
        ('TrangThaiVe', 'VARCHAR(20)', "DEFAULT 'HieuLuc'", 'Trạng thái: HieuLuc, HetHan, Huy')
    ]),
    ('Bảng 11: BaoCaoThongKe (Dữ liệu thống kê & AI)', [
        ('MaBaoCao', 'INTEGER', 'PK, AUTOINCREMENT', 'Mã bản ghi báo cáo'),
        ('LoaiBaoCao', 'VARCHAR(20)', 'NOT NULL, CHECK', 'Loại báo cáo: Ngay, Tuan, Thang'),
        ('NgayBatDau', 'DATE', 'NOT NULL', 'Ngày bắt đầu kỳ báo cáo'),
        ('NgayKetThuc', 'DATE', 'NOT NULL', 'Ngày kết thúc kỳ báo cáo'),
        ('MaKhuVuc', 'INTEGER', 'FK -> KhuVuc, NULL', 'Thống kê theo khu vực (nếu có)'),
        ('TongLuotXe', 'INTEGER', 'DEFAULT 0', 'Tổng số lượt xe trong kỳ'),
        ('TongDoanhThu', 'DECIMAL(14,2)', 'DEFAULT 0.00', 'Tổng doanh thu ghi nhận'),
        ('TyLeLapDayTrungBinh', 'DECIMAL(5,2)', 'DEFAULT 0.00', 'Tỷ lệ lấp đầy bãi xe (%)'),
        ('KhungGioCaoDiem', 'VARCHAR(255)', 'NULL', 'Chuỗi tổng hợp các khung giờ cao điểm'),
        ('NgayTao', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Thời điểm tổng hợp báo cáo')
    ])
]

for ttitle, rows in tables_detail:
    p_tname = doc_target.add_paragraph()
    p_tname.paragraph_format.space_before = Pt(6)
    p_tname.paragraph_format.space_after = Pt(2)
    r_t = p_tname.add_run(ttitle)
    fmt(r_t, size=11, bold=True, color=(37, 99, 235))
    
    tbl_d = doc_target.add_table(rows=1, cols=4)
    set_table_col_widths(tbl_d, [1.6, 1.3, 1.8, 1.8])
    for c, h in zip(tbl_d.rows[0].cells, ['Tên thuộc tính (Tiếng Việt)', 'Kiểu dữ liệu', 'Ràng buộc (Constraints)', 'Mô tả thuộc tính']):
        set_cell(c, h, bold=True, size=8.5, color=(255, 255, 255))
        shade_cell(c, '1E293B')
        
    for cname, ctype, cconstr, cdesc in rows:
        row = tbl_d.add_row()
        set_cell(row.cells[0], cname, bold=True, size=8.5)
        set_cell(row.cells[1], ctype, bold=False, size=8.5)
        set_cell(row.cells[2], cconstr, bold=False, size=8.5, color=(217, 119, 6))
        set_cell(row.cells[3], cdesc, bold=False, size=8.5)
        
    p_space_t = doc_target.add_paragraph()
    p_space_t.paragraph_format.space_after = Pt(4)

# Full SQL DDL Code Block
h2_sql = doc_target.add_heading(level=2)
r = h2_sql.add_run('Lược đồ Mã nguồn SQL DDL (SQLite 3 Script hoàn chỉnh)')
fmt(r, size=11, bold=True, color=(30, 41, 59))
add_code_block(doc_target, sql_script_full)

# PART 3: RELATIONSHIPS & CONSTRAINTS
doc_target.add_page_break()
h1_3 = doc_target.add_heading(level=1)
r = h1_3.add_run('Phần 3: Mô tả Mối quan hệ & Ràng buộc Dữ liệu')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_rel = doc_target.add_paragraph()
p_rel.paragraph_format.line_spacing = 1.15
r = p_rel.add_run(
    '1. Mô tả Mối quan hệ giữa các Thực thể:\n'
    '• VaiTro (1) — (N) NguoiDung: Một vai trò được cấp cho nhiều tài khoản người dùng.\n'
    '• KhuVuc (1) — (N) ViTriDo: Một khu vực bãi xe chứa nhiều vị trí đỗ.\n'
    '• LoaiXe (1) — (N) ViTriDo: Loại xe phân định vị trí đỗ phù hợp.\n'
    '• LoaiXe (1) — (N) PhuongTien & BangGia: Một loại xe có nhiều phương tiện và nhiều quy định giá.\n'
    '• TheXe (1) — (N) LuotGuiXe: Một thẻ xe được sử dụng cho nhiều lượt xe vào/ra theo thời gian.\n'
    '• ViTriDo (1) — (N) LuotGuiXe: Một vị trí đỗ phục vụ nhiều lượt gửi xe.\n'
    '• PhuongTien (1) — (N) LuotGuiXe & VeThang: Một phương tiện tham gia nhiều lượt gửi và có thể đăng ký vé tháng.\n\n'
    '2. Ràng buộc Toàn vẹn & An toàn AI:\n'
    '• Ràng buộc đồng bộ trạng thái chỗ trống: Khi lượt xe vào được ghi nhận (`LuotGuiXe.TrangThaiLuot = \'DangGui\'`), vị trí đỗ tương ứng `ViTriDo.TrangThai` tự động chuyển sang `DaDo`. Khi xe ra, trạng thái quay về `Trong`.\n'
    '• Chống ghi nhận trùng: Thẻ xe đang có trạng thái `DangGui` không được cấp cho lượt xe vào thứ hai.\n'
    '• Ràng buộc thời gian: `CHECK (ThoiGianRa >= ThoiGianVao)` ngăn chặn sai sót thời gian.\n'
    '• An toàn bảo mật: Mật khẩu mã hóa hash, API Key lưu tại `.env`, dữ liệu cá nhân/thanh toán không truyền vào prompt AI.'
)
fmt(r, size=10, color=(30, 41, 59))

# PART 4: INDEXES OPTIMIZATION
p_space3 = doc_target.add_paragraph()
p_space3.paragraph_format.space_after = Pt(8)

h1_4 = doc_target.add_heading(level=1)
r = h1_4.add_run('Phần 4: Gợi ý Chỉ mục (Indexes) Tối ưu Truy vấn & Báo cáo')
fmt(r, size=14, bold=True, color=(15, 23, 42))

idx_data = [
    ('idx_luotgui_bienso', 'LuotGuiXe(BienSoXeKiemTra)', 'Tối ưu tra cứu nhanh lịch sử lượt gửi theo biển số xe (FR-006).'),
    ('idx_luotgui_thoigian', 'LuotGuiXe(ThoiGianVao, ThoiGianRa)', 'Tối ưu tốc độ lọc dữ liệu theo khoảng thời gian phục vụ báo cáo lưu lượng và doanh thu (FR-008).'),
    ('idx_luotgui_trangthai', 'LuotGuiXe(TrangThaiLuot)', 'Tối ưu truy vấn danh sách các xe đang gửi hiện tại trong bãi đỗ.'),
    ('idx_vitrido_trangthai', 'ViTriDo(MaKhuVuc, TrangThai)', 'Tối ưu tính toán tức thì số chỗ trống theo từng khu vực cho giao diện và AI Chatbot.'),
    ('idx_thexe_madinhdanh', 'TheXe(MaDinhDanhThe)', 'Tối ưu tốc độ quẹt thẻ xe vào/ra tại bãi gửi.'),
    ('idx_vethang_ngay', 'VeThang(NgayBatDau, NgayKetThuc, TrangThaiVe)', 'Tối ưu kiểm tra tự động hiệu lực vé tháng khi xe vào bãi.')
]

tbl_idx = doc_target.add_table(rows=1, cols=3)
set_table_col_widths(tbl_idx, [1.8, 2.3, 2.4])
for c, h in zip(tbl_idx.rows[0].cells, ['Tên Chỉ mục (Index Name)', 'Cột tạo Chỉ mục (Indexed Columns)', 'Mục đích Tối ưu hóa']):
    set_cell(c, h, bold=True, size=9, color=(255, 255, 255))
    shade_cell(c, '1E293B')

for iname, icols, idesc in idx_data:
    row = tbl_idx.add_row()
    set_cell(row.cells[0], iname, bold=True, size=8.5, color=(37, 99, 235))
    set_cell(row.cells[1], icols, bold=True, size=8.5)
    set_cell(row.cells[2], idesc, bold=False, size=8.5)

# PART 5: STARUML ERD & SOURCE CODE
doc_target.add_page_break()
h1_5 = doc_target.add_heading(level=1)
r = h1_5.add_run('Phần 5: Sơ đồ StarUML ERD & Mã nguồn Diagram (PlantUML / Mermaid)')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_erd_desc = doc_target.add_paragraph()
p_erd_desc.paragraph_format.space_after = Pt(8)
r = p_erd_desc.add_run('Hình ảnh Sơ đồ Thực thể Liên kết (ERD) hiển thị đầy đủ 11 thực thể, các khóa chính (PK), khóa ngoại (FK) và mối quan hệ giữa các bảng.')
fmt(r, size=9.5, italic=True, color=(51, 65, 85))

# Draw & Embed ERD Image
erd_img_path = draw_erd_diagram('erd_diagram_v1.png')
doc_target.add_picture(erd_img_path, width=Inches(6.5))

p_cap = doc_target.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.paragraph_format.space_before = Pt(4)
p_cap.paragraph_format.space_after = Pt(10)
r_cap = p_cap.add_run('Hình — 5.1: Sơ đồ Thực thể Liên kết ERD (11 Entities & Relationships)')
fmt(r_cap, size=8.5, italic=True, color=(100, 116, 139))

# PlantUML ERD Code Block
h2_puml = doc_target.add_heading(level=2)
r = h2_puml.add_run('Mã nguồn PlantUML ERD (Dùng nạp StarUML / PlantUML)')
fmt(r, size=11, bold=True, color=(30, 41, 59))

puml_erd_code = """@startuml
title Mô hình Sơ đồ Thực thể Liên kết ERD — Hệ thống Bãi xe Thông minh
skinparam classAttributeIconSize 0

entity "VaiTro" {
    *MaVaiTro : INT [PK]
    --
    TenVaiTro : TEXT
    MoTa : TEXT
}

entity "NguoiDung" {
    *MaNguoiDung : INT [PK]
    --
    MaVaiTro : INT [FK]
    TenDangNhap : TEXT
    MatKhauMaHoa : TEXT
    HoTen : TEXT
}

entity "KhuVuc" {
    *MaKhuVuc : INT [PK]
    --
    TenKhuVuc : TEXT
    SucChuaToiDa : INT
}

entity "ViTriDo" {
    *MaViTri : INT [PK]
    --
    MaKhuVuc : INT [FK]
    MaLoaiXe : INT [FK]
    TenViTri : TEXT
    TrangThai : TEXT
}

entity "LoaiXe" {
    *MaLoaiXe : INT [PK]
    --
    TenLoaiXe : TEXT
    MoTa : TEXT
}

entity "PhuongTien" {
    *MaPhuongTien : INT [PK]
    --
    MaLoaiXe : INT [FK]
    BienSoXe : TEXT
    MauXe : TEXT
}

entity "TheXe" {
    *MaThe : INT [PK]
    --
    MaDinhDanhThe : TEXT
    LoaiThe : TEXT
    TrangThaiThe : TEXT
}

entity "LuotGuiXe" {
    *MaLuotGui : INT [PK]
    --
    MaThe : INT [FK]
    MaViTri : INT [FK]
    MaPhuongTien : INT [FK]
    BienSoXeKiemTra : TEXT
    ThoiGianVao : DATETIME
    ThoiGianRa : DATETIME
    TongTienPhi : DECIMAL
    TrangThaiLuot : TEXT
}

entity "BangGia" {
    *MaBangGia : INT [PK]
    --
    MaLoaiXe : INT [FK]
    LoaiApDung : TEXT
    GiaCoBan : DECIMAL
}

entity "VeThang" {
    *MaVeThang : INT [PK]
    --
    MaThe : INT [FK]
    MaPhuongTien : INT [FK]
    HoTenKhachHang : TEXT
    NgayBatDau : DATE
    NgayKetThuc : DATE
}

entity "BaoCaoThongKe" {
    *MaBaoCao : INT [PK]
    --
    MaKhuVuc : INT [FK]
    LoaiBaoCao : TEXT
    TongLuotXe : INT
    TongDoanhThu : DECIMAL
}

VaiTro ||--o{ NguoiDung
KhuVuc ||--o{ ViTriDo
LoaiXe ||--o{ ViTriDo
LoaiXe ||--o{ PhuongTien
LoaiXe ||--o{ BangGia
TheXe ||--o{ LuotGuiXe
ViTriDo ||--o{ LuotGuiXe
PhuongTien ||--o{ LuotGuiXe
TheXe ||--o{ VeThang
PhuongTien ||--o{ VeThang
KhuVuc ||--o{ BaoCaoThongKe
@enduml"""

add_code_block(doc_target, puml_erd_code)

# Mermaid ERD Code Block
h2_mermaid = doc_target.add_heading(level=2)
r = h2_mermaid.add_run('Mã nguồn Mermaid ERD (Dùng nạp Mermaid Live Editor)')
fmt(r, size=11, bold=True, color=(30, 41, 59))

mermaid_erd_code = """erDiagram
    VAITRO ||--o{ NGUOIDUNG : has
    KHUVUC ||--o{ VITRIDO : contains
    LOAIXE ||--o{ VITRIDO : applies
    LOAIXE ||--o{ PHUONGTIEN : categorizes
    LOAIXE ||--o{ BANGGIA : defines
    THEXE ||--o{ LUOTGUIXE : usedIn
    VITRIDO ||--o{ LUOTGUIXE : receives
    PHUONGTIEN ||--o{ LUOTGUIXE : involves
    THEXE ||--o{ VETHANG : links
    PHUONGTIEN ||--o{ VETHANG : registers

    VAITRO {
        int MaVaiTro PK
        string TenVaiTro
    }
    NGUOIDUNG {
        int MaNguoiDung PK
        int MaVaiTro FK
        string TenDangNhap
    }
    KHUVUC {
        int MaKhuVuc PK
        string TenKhuVuc
    }
    VITRIDO {
        int MaViTri PK
        int MaKhuVuc FK
        string TrangThai
    }
    LUOTGUIXE {
        int MaLuotGui PK
        int MaThe FK
        int MaViTri FK
        string BienSoXeKiemTra
        datetime ThoiGianVao
        decimal TongTienPhi
    }"""

add_code_block(doc_target, mermaid_erd_code)

# Output File Path
out_doc_path = Path('CSDL_v1.0.docx')
try:
    doc_target.save(out_doc_path)
    print('====================================================')
    print(f'SUCCESS! File saved to: {out_doc_path.resolve()}')
    print('====================================================')
except PermissionError:
    alt_path = Path('CSDL_v1.0_fixed.docx')
    doc_target.save(alt_path)
    print('====================================================')
    print(f'CSDL_v1.0.docx đang mở trong Word! Đã lưu tạm sang: {alt_path.resolve()}')
    print('====================================================')

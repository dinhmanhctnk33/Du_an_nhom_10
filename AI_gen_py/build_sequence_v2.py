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

ASSETS_DIR = Path('v2_assets')
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
# Image Generator Engine using Pillow
# ---------------------------------------------------------
def draw_sequence_diagram(title, participants, steps, output_filename):
    width = 1600
    row_height = 76
    header_height = 140
    footer_height = 60
    
    y_coords = []
    current_y = header_height + 50
    
    prev_branch = None
    for i, step in enumerate(steps):
        branch = step[0]
        if branch != prev_branch:
            if prev_branch is not None:
                current_y += 35
            prev_branch = branch
        y_coords.append(current_y)
        current_y += row_height
        
    total_height = max(700, current_y + footer_height)
    
    img = Image.new('RGB', (width, total_height), 'white')
    d = ImageDraw.Draw(img)
    
    try:
        font_bold = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 24)
        font_small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
        font_title = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 26)
    except OSError:
        font_bold = font_small = font_title = ImageFont.load_default()
        
    # Title box
    d.rounded_rectangle((20, 15, width - 20, 65), radius=8, fill='#F1F5F9', outline='#0F172A', width=2)
    d.text((35, 25), f'Sơ đồ tuần tự UML 2.5: {title}', font=font_title, fill='#0F172A')
    
    # Participants
    n = len(participants)
    margin_x = 150
    xs = [margin_x + i * (width - 2 * margin_x) / (n - 1) if n > 1 else width / 2 for i in range(n)]
    
    top_y = 90
    lifeline_start_y = 140
    lifeline_end_y = total_height - 45
    
    # Draw Participant Headers & Lifelines
    for x, p_name in zip(xs, participants):
        bbox = d.textbbox((0, 0), p_name, font=font_bold)
        tw = bbox[2] - bbox[0]
        
        # Header box
        d.rounded_rectangle((x - tw/2 - 20, top_y, x + tw/2 + 20, top_y + 42), radius=8, fill='#EFF6FF', outline='#2563EB', width=2)
        d.text((x - tw/2, top_y + 8), p_name, font=font_bold, fill='#1D4ED8')
        
        # Dashed Lifeline
        for ly in range(lifeline_start_y, lifeline_end_y, 16):
            d.line((x, ly, x, min(ly + 8, lifeline_end_y)), fill='#94A3B8', width=2)
            
    # Group steps into Branch Frames (alt / else)
    branch_groups = []
    curr_b = None
    start_i = 0
    for i, st in enumerate(steps):
        b = st[0]
        if b != curr_b:
            if curr_b is not None:
                branch_groups.append((curr_b, start_i, i - 1))
            curr_b = b
            start_i = i
    if curr_b is not None:
        branch_groups.append((curr_b, start_i, len(steps) - 1))
        
    for b_name, s_idx, e_idx in branch_groups:
        frame_top = y_coords[s_idx] - 35
        frame_bottom = y_coords[e_idx] + 32
        
        if 'Main' in b_name or 'Chính' in b_name:
            bd_col = '#16A34A'
            tag_txt = 'alt [Luồng chính thành công]'
        elif 'E' in b_name or 'Ngoại lệ' in b_name:
            bd_col = '#DC2626'
            tag_txt = f'else [{b_name}]'
        else:
            bd_col = '#D97706'
            tag_txt = f'else [{b_name}]'
            
        frame_left = xs[0] - 50
        frame_right = xs[-1] + 50
        
        d.rectangle((frame_left, frame_top, frame_right, frame_bottom), fill=None, outline=bd_col, width=2)
        
        # Tag box top-left
        d.rectangle((frame_left, frame_top, frame_left + 340, frame_top + 26), fill=bd_col)
        d.text((frame_left + 10, frame_top + 4), tag_txt, font=font_small, fill='white')
        
    # Draw Message Arrows
    for i, (branch, src, dst, msg, is_return) in enumerate(steps):
        y = y_coords[i]
        src_x = xs[participants.index(src)]
        dst_x = xs[participants.index(dst)]
        
        if 'E' in branch or 'Ngoại lệ' in branch:
            msg_color = '#B91C1C'
        elif 'A' in branch or 'Thay thế' in branch:
            msg_color = '#B45309'
        else:
            msg_color = '#0F172A'
            
        arrow_color = msg_color
        direction = 1 if dst_x >= src_x else -1
        
        if src_x == dst_x: # Self call
            d.line((src_x, y, src_x + 40, y), fill=arrow_color, width=2)
            d.line((src_x + 40, y, src_x + 40, y + 25), fill=arrow_color, width=2)
            d.line((src_x + 40, y + 25, src_x, y + 25), fill=arrow_color, width=2)
            d.polygon([(src_x + 8, y + 20), (src_x, y + 25), (src_x + 8, y + 30)], fill=arrow_color)
            d.text((src_x + 48, y + 5), msg, font=font_small, fill=msg_color)
        else:
            if is_return:
                for lx in range(int(min(src_x, dst_x)), int(max(src_x, dst_x)), 12):
                    d.line((lx, y, min(lx + 6, max(src_x, dst_x)), y), fill=arrow_color, width=2)
                d.line((dst_x, y, dst_x - direction * 12, y - 6), fill=arrow_color, width=2)
                d.line((dst_x, y, dst_x - direction * 12, y + 6), fill=arrow_color, width=2)
            else:
                d.line((src_x, y, dst_x, y), fill=arrow_color, width=2)
                d.polygon([(dst_x, y), (dst_x - direction * 14, y - 7), (dst_x - direction * 14, y + 7)], fill=arrow_color)
                
            text_lines = textwrap.wrap(msg, width=34)
            lbl_text = '\n'.join(text_lines)
            bbox = d.multiline_textbbox((0, 0), lbl_text, font=font_small, spacing=2)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            
            mid_x = (src_x + dst_x) / 2
            lbl_x = mid_x - tw / 2
            lbl_y = y - th - 8
            
            d.rectangle((lbl_x - 6, lbl_y - 2, lbl_x + tw + 6, lbl_y + th + 2), fill='white')
            d.multiline_text((lbl_x, lbl_y), lbl_text, font=font_small, fill=msg_color, align='center', spacing=2)
            
    out_path = ASSETS_DIR / output_filename
    img.save(out_path)
    return str(out_path)

def generate_plantuml(title, code, participants, steps):
    out = [
        '@startuml',
        f'title {code} — {title}',
        'hide footbox',
        'skinparam sequenceMessageAlign center',
        'skinparam responseMessageBelowArrow true'
    ]
    aliases = {}
    for i, p in enumerate(participants):
        aliases[p] = f'P{i+1}'
        out.append(f'participant "{p}" as P{i+1}')
        
    curr_branch = None
    for branch, src, dst, msg, is_return in steps:
        if branch != curr_branch:
            if curr_branch is None:
                out.append(f'alt {branch}')
            else:
                out.append(f'else {branch}')
            curr_branch = branch
            
        arrow = '--->' if is_return else '->'
        out.append(f'{aliases[src]} {arrow} {aliases[dst]} : {msg}')
        
    out.append('end')
    out.append('@enduml')
    return '\n'.join(out)


# ---------------------------------------------------------
# Define all 12 Use Cases complete datasets
# ---------------------------------------------------------
USE_CASES = [
    {
        'code': 'SEQ-001',
        'uc_id': 'UC-001',
        'title': 'Đăng nhập và phân quyền',
        'purpose': 'Mục đích: Xác thực người dùng, cấp phiên làm việc và áp dụng menu/quyền truy cập theo vai trò. Thể hiện luồng chính, luồng từ chối (A1), từ chối quyền (A2) và ngoại lệ CSDL (E1).',
        'participants': ['Actor', 'Giao diện', 'Dịch vụ xác thực', 'Kho tài khoản'],
        'steps': [
            ('Luồng chính thành công', 'Actor', 'Giao diện', '1. Gửi thông tin đăng nhập', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ xác thực', '2. Yêu cầu xác thực', False),
            ('Luồng chính thành công', 'Dịch vụ xác thực', 'Kho tài khoản', '3. Đối chiếu thông tin tài khoản', False),
            ('Luồng chính thành công', 'Kho tài khoản', 'Dịch vụ xác thực', '4. Trả về thông tin vai trò & quyền', True),
            ('Luồng chính thành công', 'Dịch vụ xác thực', 'Giao diện', '5. Tạo phiên & cấp quyền thành công', True),
            ('Luồng chính thành công', 'Giao diện', 'Actor', '6. Thông báo thành công & cấp menu vai trò', True),
            
            ('Luồng thay thế A1 — Thông tin không hợp lệ', 'Dịch vụ xác thực', 'Giao diện', 'A1.1: Từ chối xác thực (sai tài khoản/mật khẩu)', True),
            ('Luồng thay thế A1 — Thông tin không hợp lệ', 'Giao diện', 'Actor', 'A1.2: Thông báo không thể xác thực; kết thúc UC', True),
            
            ('Luồng thay thế A2 — Không có quyền chức năng', 'Giao diện', 'Actor', 'A2.1: Từ chối truy cập chức năng vượt quyền', True),
            
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Kho tài khoản', 'Dịch vụ xác thực', 'E1.1: Lỗi kết nối CSDL / truy xuất dữ liệu', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Dịch vụ xác thực', 'Giao diện', 'E1.2: Báo lỗi hệ thống, không tạo phiên', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Giao diện', 'Actor', 'E1.3: Thông báo lỗi hệ thống, yêu cầu thử lại', True),
        ]
    },
    {
        'code': 'SEQ-002',
        'uc_id': 'UC-002',
        'title': 'Quản lý tài khoản và phân quyền',
        'purpose': 'Mục đích: Cập nhật thông tin tài khoản hoặc phân quyền người dùng. Xử lý các luồng từ chối do dữ liệu không hợp lệ (A1), không đủ quyền (A2) và lỗi lưu CSDL (E1).',
        'participants': ['Quản lý', 'Giao diện', 'Dịch vụ tài khoản', 'Kho tài khoản'],
        'steps': [
            ('Luồng chính thành công', 'Quản lý', 'Giao diện', '1. Chọn thao tác & gửi thay đổi tài khoản', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ tài khoản', '2. Yêu cầu cập nhật tài khoản/quyền', False),
            ('Luồng chính thành công', 'Dịch vụ tài khoản', 'Kho tài khoản', '3. Kiểm tra quyền Quản lý & dữ liệu', False),
            ('Luồng chính thành công', 'Kho tài khoản', 'Dịch vụ tài khoản', '4. Xác nhận hợp lệ & đủ quyền', True),
            ('Luồng chính thành công', 'Dịch vụ tài khoản', 'Kho tài khoản', '5. Lưu thay đổi tài khoản/quyền', False),
            ('Luồng chính thành công', 'Kho tài khoản', 'Dịch vụ tài khoản', '6. Kết quả lưu thành công', True),
            ('Luồng chính thành công', 'Dịch vụ tài khoản', 'Giao diện', '7. Trạng thái cập nhật thành công', True),
            ('Luồng chính thành công', 'Giao diện', 'Quản lý', '8. Thông báo cập nhật tài khoản thành công', True),
            
            ('Luồng thay thế A1 — Dữ liệu không hợp lệ', 'Dịch vụ tài khoản', 'Giao diện', 'A1.1: Báo lỗi dữ liệu không hợp lệ', True),
            ('Luồng thay thế A1 — Dữ liệu không hợp lệ', 'Giao diện', 'Quản lý', 'A1.2: Yêu cầu điều chỉnh lại dữ liệu', True),
            
            ('Luồng thay thế A2 — Actor không có quyền', 'Dịch vụ tài khoản', 'Giao diện', 'A2.1: Từ chối thao tác (Không đủ quyền)', True),
            ('Luồng thay thế A2 — Actor không có quyền', 'Giao diện', 'Quản lý', 'A2.2: Thông báo không có quyền thực hiện', True),
            
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Kho tài khoản', 'Dịch vụ tài khoản', 'E1.1: Lỗi không thể lưu CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Dịch vụ tài khoản', 'Giao diện', 'E1.2: Báo lỗi hệ thống, không xác nhận cập nhật', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Giao diện', 'Quản lý', 'E1.3: Hiển thị thông báo lỗi lưu dữ liệu', True),
        ]
    },
    {
        'code': 'SEQ-003',
        'uc_id': 'UC-003',
        'title': 'Quản lý khu vực, vị trí đỗ và loại xe',
        'purpose': 'Mục đích: Thiết lập và duy trì danh mục bãi xe. Bao gồm luồng chính thành công, luồng báo lỗi dữ liệu danh mục không hợp lệ (A1) và ngoại lệ lỗi CSDL (E1).',
        'participants': ['Quản lý', 'Giao diện', 'Dịch vụ danh mục', 'Kho dữ liệu'],
        'steps': [
            ('Luồng chính thành công', 'Quản lý', 'Giao diện', '1. Chọn chức năng & nhập dữ liệu danh mục', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ danh mục', '2. Yêu cầu cập nhật danh mục', False),
            ('Luồng chính thành công', 'Dịch vụ danh mục', 'Kho dữ liệu', '3. Kiểm tra dữ liệu & lưu danh mục', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ danh mục', '4. Lưu dữ liệu danh mục thành công', True),
            ('Luồng chính thành công', 'Dịch vụ danh mục', 'Giao diện', '5. Trả kết quả cập nhật thành công', True),
            ('Luồng chính thành công', 'Giao diện', 'Quản lý', '6. Hiển thị danh mục mới & thông báo thành công', True),
            
            ('Luồng thay thế A1 — Dữ liệu không hợp lệ', 'Dịch vụ danh mục', 'Giao diện', 'A1.1: Báo lỗi dữ liệu trùng hoặc không hợp lệ', True),
            ('Luồng thay thế A1 — Dữ liệu không hợp lệ', 'Giao diện', 'Quản lý', 'A1.2: Yêu cầu điều chỉnh thông tin danh mục', True),
            
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Kho dữ liệu', 'Dịch vụ danh mục', 'E1.1: Lỗi kết nối / lưu CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Dịch vụ danh mục', 'Giao diện', 'E1.2: Báo không thể hoàn tất lưu trữ', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Giao diện', 'Quản lý', 'E1.3: Thông báo lỗi hệ thống', True),
        ]
    },
    {
        'code': 'SEQ-004',
        'uc_id': 'UC-004',
        'title': 'Ghi nhận xe vào',
        'purpose': 'Mục đích: Ghi nhận xe vào bãi, cấp vé/thẻ và gán vị trí đỗ. Xử lý trường hợp hết chỗ đỗ (A1), thẻ không hợp lệ (A2) và lỗi lưu CSDL (E1).',
        'participants': ['Nhân viên bãi xe', 'Giao diện', 'Dịch vụ bãi xe', 'Kho dữ liệu'],
        'steps': [
            ('Luồng chính thành công', 'Nhân viên bãi xe', 'Giao diện', '1. Nhập thông tin xe vào / quét thẻ', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ bãi xe', '2. Yêu cầu ghi nhận xe vào', False),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Kho dữ liệu', '3. Kiểm tra trạng thái thẻ & vị trí đỗ', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ bãi xe', '4. Xác nhận thẻ hợp lệ & còn chỗ trống', True),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Kho dữ liệu', '5. Ghi nhận lượt xe vào & cập nhật chỗ đỗ', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ bãi xe', '6. Lưu lượt xe vào thành công', True),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Giao diện', '7. Kết quả ghi nhận xe vào thành công', True),
            ('Luồng chính thành công', 'Giao diện', 'Nhân viên bãi xe', '8. Thông báo thành công & in vé/mở barie', True),
            
            ('Luồng thay thế A1 — Hết chỗ đỗ', 'Kho dữ liệu', 'Dịch vụ bãi xe', 'A1.1: Báo bãi đỗ đã hết chỗ', True),
            ('Luồng thay thế A1 — Hết chỗ đỗ', 'Dịch vụ bãi xe', 'Giao diện', 'A1.2: Từ chối ghi nhận xe vào', True),
            ('Luồng thay thế A1 — Hết chỗ đỗ', 'Giao diện', 'Nhân viên bãi xe', 'A1.3: Thông báo bãi xe đã hết chỗ đỗ', True),
            
            ('Luồng thay thế A2 — Thẻ không hợp lệ', 'Kho dữ liệu', 'Dịch vụ bãi xe', 'A2.1: Thẻ bị khóa hoặc đang gửi xe khác', True),
            ('Luồng thay thế A2 — Thẻ không hợp lệ', 'Dịch vụ bãi xe', 'Giao diện', 'A2.2: Từ chối sử dụng thẻ', True),
            ('Luồng thay thế A2 — Thẻ không hợp lệ', 'Giao diện', 'Nhân viên bãi xe', 'A2.3: Thông báo thẻ không hợp lệ/đã dùng', True),
            
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Kho dữ liệu', 'Dịch vụ bãi xe', 'E1.1: Lỗi CSDL không thể lưu lượt vào', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Dịch vụ bãi xe', 'Giao diện', 'E1.2: Báo lỗi hệ thống', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Giao diện', 'Nhân viên bãi xe', 'E1.3: Báo lỗi hệ thống, không xác nhận lượt vào', True),
        ]
    },
    {
        'code': 'SEQ-005',
        'uc_id': 'UC-005',
        'title': 'Ghi nhận xe ra và tính phí',
        'purpose': 'Mục đích: Đối chiếu xe vào, gọi Bảng giá tính phí, thu tiền và giải phóng vị trí. Mô tả đầy đủ luồng không tìm thấy lượt vào (A1), sai thời gian (A2), lỗi giá (A3) và lỗi CSDL (E1).',
        'participants': ['Nhân viên bãi xe', 'Giao diện', 'Dịch vụ bãi xe', 'Kho dữ liệu', 'Bảng giá'],
        'steps': [
            ('Luồng chính thành công', 'Nhân viên bãi xe', 'Giao diện', '1. Quét thẻ / nhập thông tin xe ra', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ bãi xe', '2. Yêu cầu ghi nhận xe ra', False),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Kho dữ liệu', '3. Tìm lượt gửi xe tương ứng', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ bãi xe', '4. Trả về thông tin lượt gửi & giờ vào', True),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Bảng giá', '5. Yêu cầu tính phí theo loại xe & thời gian', False),
            ('Luồng chính thành công', 'Bảng giá', 'Dịch vụ bãi xe', '6. Trả về số tiền phí gửi xe', True),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Giao diện', '7. Hiển thị số tiền phí cho Nhân viên', True),
            ('Luồng chính thành công', 'Nhân viên bãi xe', 'Giao diện', '8. Xác nhận đã thu tiền thanh toán', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ bãi xe', '9. Gửi xác nhận thanh toán thành công', False),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Kho dữ liệu', '10. Ghi nhận xe ra & giải phóng vị trí đỗ', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ bãi xe', '11. Lưu hoàn tất lượt gửi thành công', True),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Giao diện', '12. Trả về kết quả hoàn tất', True),
            ('Luồng chính thành công', 'Giao diện', 'Nhân viên bãi xe', '13. Thông báo hoàn tất & mở barie xe ra', True),
            
            ('Luồng thay thế A1 — Không tìm thấy lượt gửi', 'Kho dữ liệu', 'Dịch vụ bãi xe', 'A1.1: Không tìm thấy thông tin xe vào', True),
            ('Luồng thay thế A1 — Không tìm thấy lượt gửi', 'Dịch vụ bãi xe', 'Giao diện', 'A1.2: Báo không tìm thấy lượt gửi', True),
            ('Luồng thay thế A1 — Không tìm thấy lượt gửi', 'Giao diện', 'Nhân viên bãi xe', 'A1.3: Báo không tìm thấy; yêu cầu xử lý thủ công', True),
            
            ('Luồng thay thế A2 — Sai lệch thời gian', 'Dịch vụ bãi xe', 'Giao diện', 'A2.1: Báo sai lệch thời gian ra/vào', True),
            ('Luồng thay thế A2 — Sai lệch thời gian', 'Giao diện', 'Nhân viên bãi xe', 'A2.2: Không tính phí, yêu cầu kiểm tra lại', True),
            
            ('Luồng thay thế A3 — Không tính được phí', 'Bảng giá', 'Dịch vụ bãi xe', 'A3.1: Không có quy định mức phí phù hợp', True),
            ('Luồng thay thế A3 — Không tính được phí', 'Dịch vụ bãi xe', 'Giao diện', 'A3.2: Báo lỗi bảng giá không tính được phí', True),
            ('Luồng thay thế A3 — Không tính được phí', 'Giao diện', 'Nhân viên bãi xe', 'A3.3: Thông báo không thể hoàn tất lượt gửi', True),
            
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Kho dữ liệu', 'Dịch vụ bãi xe', 'E1.1: Lỗi lưu kết quả xe ra vào CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Dịch vụ bãi xe', 'Giao diện', 'E1.2: Báo lỗi lưu dữ liệu', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Giao diện', 'Nhân viên bãi xe', 'E1.3: Thông báo lỗi hệ thống, chưa hoàn tất xe ra', True),
        ]
    },
    {
        'code': 'SEQ-006',
        'uc_id': 'UC-006',
        'title': 'Theo dõi chỗ trống theo khu vực',
        'purpose': 'Mục đích: Truy xuất và tổng hợp tình trạng chỗ trống bãi đỗ. Mô tả luồng thành công, không có dữ liệu (A1), trạng thái chưa rõ (A2) và lỗi kết nối CSDL (E1).',
        'participants': ['Actor', 'Giao diện', 'Dịch vụ bãi xe', 'Kho dữ liệu'],
        'steps': [
            ('Luồng chính thành công', 'Actor', 'Giao diện', '1. Chọn xem tình trạng chỗ trống khu vực', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ bãi xe', '2. Yêu cầu lấy thông tin chỗ đỗ', False),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Kho dữ liệu', '3. Truy xuất trạng thái các vị trí đỗ', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ bãi xe', '4. Trả về danh sách vị trí & trạng thái', True),
            ('Luồng chính thành công', 'Dịch vụ bãi xe', 'Giao diện', '5. Tổng hợp số chỗ trống từng khu vực', True),
            ('Luồng chính thành công', 'Giao diện', 'Actor', '6. Hiển thị sơ đồ & số chỗ trống', True),
            
            ('Luồng thay thế A1 — Không có dữ liệu', 'Kho dữ liệu', 'Dịch vụ bãi xe', 'A1.1: Danh sách vị trí rỗng', True),
            ('Luồng thay thế A1 — Không có dữ liệu', 'Dịch vụ bãi xe', 'Giao diện', 'A1.2: Báo không có dữ liệu khu vực', True),
            ('Luồng thay thế A1 — Không có dữ liệu', 'Giao diện', 'Actor', 'A1.3: Thông báo không có dữ liệu phù hợp', True),
            
            ('Luồng thay thế A2 — Trạng thái chưa rõ', 'Dịch vụ bãi xe', 'Giao diện', 'A2.1: Chỉ hiển thị các vị trí xác định được', True),
            ('Luồng thay thế A2 — Trạng thái chưa rõ', 'Giao diện', 'Actor', 'A2.2: Hiển thị kết quả kèm cảnh báo dữ liệu thiếu', True),
            
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Kho dữ liệu', 'Dịch vụ bãi xe', 'E1.1: Lỗi truy xuất dữ liệu CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Dịch vụ bãi xe', 'Giao diện', 'E1.2: Báo lỗi kết nối CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Giao diện', 'Actor', 'E1.3: Thông báo lỗi không tải được dữ liệu', True),
        ]
    },
    {
        'code': 'SEQ-007',
        'uc_id': 'UC-007',
        'title': 'Tra cứu lượt gửi xe',
        'purpose': 'Mục đích: Tìm kiếm thông tin lượt gửi theo biển số hoặc thời gian. Thể hiện luồng thành công, tiêu chí nhập sai (A1), không tìm thấy kết quả (A2) và lỗi CSDL (E1).',
        'participants': ['Actor', 'Giao diện', 'Dịch vụ tra cứu', 'Kho dữ liệu'],
        'steps': [
            ('Luồng chính thành công', 'Actor', 'Giao diện', '1. Nhập tiêu chí tra cứu (biển số/thời gian)', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ tra cứu', '2. Gửi yêu cầu tra cứu lượt gửi', False),
            ('Luồng chính thành công', 'Dịch vụ tra cứu', 'Kho dữ liệu', '3. Kiểm tra tiêu chí & truy xuất lượt gửi', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ tra cứu', '4. Trả về danh sách lượt gửi phù hợp', True),
            ('Luồng chính thành công', 'Dịch vụ tra cứu', 'Giao diện', '5. Trả kết quả danh sách tra cứu', True),
            ('Luồng chính thành công', 'Giao diện', 'Actor', '6. Hiển thị bảng danh sách lượt gửi xe', True),
            
            ('Luồng thay thế A1 — Tiêu chí không hợp lệ', 'Dịch vụ tra cứu', 'Giao diện', 'A1.1: Báo tiêu chí tra cứu nhập sai định dạng', True),
            ('Luồng thay thế A1 — Tiêu chí không hợp lệ', 'Giao diện', 'Actor', 'A1.2: Yêu cầu nhập lại tiêu chí tìm kiếm', True),
            
            ('Luồng thay thế A2 — Không tìm thấy kết quả', 'Kho dữ liệu', 'Dịch vụ tra cứu', 'A2.1: Trả về danh sách rỗng', True),
            ('Luồng thay thế A2 — Không tìm thấy kết quả', 'Dịch vụ tra cứu', 'Giao diện', 'A2.2: Báo không tìm thấy kết quả', True),
            ('Luồng thay thế A2 — Không tìm thấy kết quả', 'Giao diện', 'Actor', 'A2.3: Thông báo không tìm thấy lượt gửi phù hợp', True),
            
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Kho dữ liệu', 'Dịch vụ tra cứu', 'E1.1: Lỗi truy xuất CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Dịch vụ tra cứu', 'Giao diện', 'E1.2: Báo lỗi kết nối CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Giao diện', 'Actor', 'E1.3: Thông báo lỗi hệ thống không thể tra cứu', True),
        ]
    },
    {
        'code': 'SEQ-008',
        'uc_id': 'UC-008',
        'title': 'Quản lý vé tháng hoặc khách quen',
        'purpose': 'Mục đích: Thêm, sửa, gia hạn vé tháng hoặc thông tin khách quen. Xử lý luồng thành công, thông tin không hợp lệ (A1), vé không tồn tại (A2) và lỗi lưu CSDL (E1).',
        'participants': ['Quản lý', 'Giao diện', 'Dịch vụ vé', 'Kho dữ liệu'],
        'steps': [
            ('Luồng chính thành công', 'Quản lý', 'Giao diện', '1. Nhập/chỉnh sửa thông tin vé tháng', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ vé', '2. Yêu cầu cập nhật dữ liệu vé/khách', False),
            ('Luồng chính thành công', 'Dịch vụ vé', 'Kho dữ liệu', '3. Đối chiếu quy tắc & lưu thông tin vé', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ vé', '4. Lưu thông tin vé thành công', True),
            ('Luồng chính thành công', 'Dịch vụ vé', 'Giao diện', '5. Trả kết quả cập nhật thành công', True),
            ('Luồng chính thành công', 'Giao diện', 'Quản lý', '6. Hiển thị thông báo cập nhật thành công', True),
            
            ('Luồng thay thế A1 — Dữ liệu không hợp lệ', 'Dịch vụ vé', 'Giao diện', 'A1.1: Báo thông tin vé không hợp lệ hoặc bị trùng', True),
            ('Luồng thay thế A1 — Dữ liệu không hợp lệ', 'Giao diện', 'Quản lý', 'A1.2: Yêu cầu kiểm tra & điều chỉnh lại dữ liệu', True),
            
            ('Luồng thay thế A2 — Dữ liệu không tồn tại', 'Kho dữ liệu', 'Dịch vụ vé', 'A2.1: Không tìm thấy vé hoặc vé đã hết hạn', True),
            ('Luồng thay thế A2 — Dữ liệu không tồn tại', 'Dịch vụ vé', 'Giao diện', 'A2.2: Từ chối thao tác gia hạn/sửa vé', True),
            ('Luồng thay thế A2 — Dữ liệu không tồn tại', 'Giao diện', 'Quản lý', 'A2.3: Thông báo dữ liệu vé không tồn tại', True),
            
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Kho dữ liệu', 'Dịch vụ vé', 'E1.1: Lỗi kết nối / lưu CSDL', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Dịch vụ vé', 'Giao diện', 'E1.2: Báo lỗi lưu dữ liệu', True),
            ('Luồng ngoại lệ E1 — Lỗi lưu CSDL', 'Giao diện', 'Quản lý', 'E1.3: Thông báo lỗi hệ thống không thể lưu', True),
        ]
    },
    {
        'code': 'SEQ-009',
        'uc_id': 'UC-009',
        'title': 'Xem thống kê vận hành',
        'purpose': 'Mục đích: Báo cáo tổng hợp lưu lượng, doanh thu và khung giờ cao điểm. Thể hiện luồng thành công, không đủ dữ liệu (A1), tiêu chí sai (A2) và lỗi tổng hợp CSDL (E1).',
        'participants': ['Quản lý', 'Giao diện', 'Dịch vụ thống kê', 'Kho dữ liệu'],
        'steps': [
            ('Luồng chính thành công', 'Quản lý', 'Giao diện', '1. Chọn khoảng thời gian & bộ lọc thống kê', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ thống kê', '2. Gửi yêu cầu tổng hợp thống kê', False),
            ('Luồng chính thành công', 'Dịch vụ thống kê', 'Kho dữ liệu', '3. Truy xuất lượt gửi xe & doanh thu', False),
            ('Luồng chính thành công', 'Kho dữ liệu', 'Dịch vụ thống kê', '4. Trả về dữ liệu chi tiết', True),
            ('Luồng chính thành công', 'Dịch vụ thống kê', 'Giao diện', '5. Tổng hợp lưu lượng, doanh thu, cao điểm', True),
            ('Luồng chính thành công', 'Giao diện', 'Quản lý', '6. Hiển thị báo cáo thống kê vận hành', True),
            
            ('Luồng thay thế A1 — Dữ liệu rỗng', 'Kho dữ liệu', 'Dịch vụ thống kê', 'A1.1: Trả về dữ liệu rỗng trong khoảng chọn', True),
            ('Luồng thay thế A1 — Dữ liệu rỗng', 'Dịch vụ thống kê', 'Giao diện', 'A1.2: Báo dữ liệu rỗng không đủ tổng hợp', True),
            ('Luồng thay thế A1 — Dữ liệu rỗng', 'Giao diện', 'Quản lý', 'A1.3: Thông báo không đủ dữ liệu thống kê', True),
            
            ('Luồng thay thế A2 — Tiêu chí không hợp lệ', 'Dịch vụ thống kê', 'Giao diện', 'A2.1: Báo mốc thời gian chọn không hợp lệ', True),
            ('Luồng thay thế A2 — Tiêu chí không hợp lệ', 'Giao diện', 'Quản lý', 'A2.2: Yêu cầu chọn lại khoảng thời gian', True),
            
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Kho dữ liệu', 'Dịch vụ thống kê', 'E1.1: Lỗi CSDL / không thể tổng hợp', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Dịch vụ thống kê', 'Giao diện', 'E1.2: Báo lỗi hệ thống', True),
            ('Luồng ngoại lệ E1 — Lỗi CSDL', 'Giao diện', 'Quản lý', 'E1.3: Hiển thị thông báo lỗi truy xuất CSDL', True),
        ]
    },
    {
        'code': 'SEQ-010',
        'uc_id': 'UC-010',
        'title': 'AI sinh báo cáo lưu lượng',
        'purpose': 'Mục đích: Tự động phân tích và tạo báo cáo lưu lượng ngày/tuần bằng AI. Bao gồm luồng thành công, không đủ dữ liệu (A1), sai phạm vi (A2), AI timeout (E1) và AI sai định dạng (E2).',
        'participants': ['Quản lý', 'Giao diện', 'Dịch vụ AI', 'Dịch vụ thống kê', 'Nhà cung cấp AI'],
        'steps': [
            ('Luồng chính thành công', 'Quản lý', 'Giao diện', '1. Yêu cầu tạo báo cáo AI (ngày/tuần)', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ AI', '2. Gửi yêu cầu sinh báo cáo', False),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Dịch vụ thống kê', '3. Lấy dữ liệu lưu lượng & khung giờ', False),
            ('Luồng chính thành công', 'Dịch vụ thống kê', 'Dịch vụ AI', '4. Trả về dữ liệu thống kê hợp lệ', True),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Nhà cung cấp AI', '5. Gửi prompt + ràng buộc không bịa số liệu', False),
            ('Luồng chính thành công', 'Nhà cung cấp AI', 'Dịch vụ AI', '6. Trả về nội dung văn bản báo cáo AI', True),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Giao diện', '7. Kiểm tra định dạng & đính kèm cảnh báo', True),
            ('Luồng chính thành công', 'Giao diện', 'Quản lý', '8. Hiển thị báo cáo AI kèm lưu ý kiểm chứng', True),
            
            ('Luồng thay thế A1 — Dữ liệu không đủ', 'Dịch vụ thống kê', 'Dịch vụ AI', 'A1.1: Báo không đủ dữ liệu thống kê', True),
            ('Luồng thay thế A1 — Dữ liệu không đủ', 'Dịch vụ AI', 'Giao diện', 'A1.2: Từ chối gọi AI, báo không đủ dữ liệu', True),
            ('Luồng thay thế A1 — Dữ liệu không đủ', 'Giao diện', 'Quản lý', 'A1.3: Thông báo không thể tạo báo cáo AI', True),
            
            ('Luồng thay thế A2 — Sai phạm vi ngày/tuần', 'Dịch vụ AI', 'Giao diện', 'A2.1: Báo phạm vi báo cáo không hỗ trợ', True),
            ('Luồng thay thế A2 — Sai phạm vi ngày/tuần', 'Giao diện', 'Quản lý', 'A2.2: Yêu cầu chọn phạm vi ngày hoặc tuần', True),
            
            ('Luồng ngoại lệ E1 — AI timeout/error', 'Nhà cung cấp AI', 'Dịch vụ AI', 'E1.1: Lỗi timeout / rate limit / 503', True),
            ('Luồng ngoại lệ E1 — AI timeout/error', 'Dịch vụ AI', 'Giao diện', 'E1.2: Fallback báo lỗi AI, không bịa nội dung', True),
            ('Luồng ngoại lệ E1 — AI timeout/error', 'Giao diện', 'Quản lý', 'E1.3: Báo lỗi AI không khả dụng, không tạo báo cáo', True),
            
            ('Luồng ngoại lệ E2 — Response AI rỗng/sai', 'Nhà cung cấp AI', 'Dịch vụ AI', 'E2.1: Response rỗng hoặc sai cấu trúc text', True),
            ('Luồng ngoại lệ E2 — Response AI rỗng/sai', 'Dịch vụ AI', 'Giao diện', 'E2.2: Từ chối kết quả không hợp lệ', True),
            ('Luồng ngoại lệ E2 — Response AI rỗng/sai', 'Giao diện', 'Quản lý', 'E2.3: Thông báo kết quả AI không hợp lệ', True),
        ]
    },
    {
        'code': 'SEQ-011',
        'uc_id': 'UC-011',
        'title': 'AI hỏi đáp dữ liệu bãi xe',
        'purpose': 'Mục đích: Giải đáp các câu hỏi phân tích dữ liệu quản trị bãi xe bằng AI. Xử lý luồng thành công, không có dữ liệu câu hỏi (A1), vượt phân quyền (A2) và AI không khả dụng (E1).',
        'participants': ['Quản lý', 'Giao diện', 'Dịch vụ AI', 'Dịch vụ thống kê', 'Nhà cung cấp AI'],
        'steps': [
            ('Luồng chính thành công', 'Quản lý', 'Giao diện', '1. Nhập câu hỏi phân tích dữ liệu bãi xe', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ AI', '2. Gửi câu hỏi yêu cầu giải đáp', False),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Dịch vụ thống kê', '3. Kiểm tra quyền & lấy dữ liệu ngữ cảnh', False),
            ('Luồng chính thành công', 'Dịch vụ thống kê', 'Dịch vụ AI', '4. Trả về dữ liệu ngữ cảnh hợp lệ', True),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Nhà cung cấp AI', '5. Gửi context + câu hỏi + guardrails', False),
            ('Luồng chính thành công', 'Nhà cung cấp AI', 'Dịch vụ AI', '6. Trả câu trả lời phân tích AI', True),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Giao diện', '7. Kiểm tra & đính kèm khuyến cáo kiểm chứng', True),
            ('Luồng chính thành công', 'Giao diện', 'Quản lý', '8. Hiển thị câu trả lời AI kèm cảnh báo', True),
            
            ('Luồng thay thế A1 — Không có dữ liệu', 'Dịch vụ thống kê', 'Dịch vụ AI', 'A1.1: Không tìm thấy dữ liệu liên quan', True),
            ('Luồng thay thế A1 — Không có dữ liệu', 'Dịch vụ AI', 'Giao diện', 'A1.2: Báo không đủ dữ liệu giải đáp', True),
            ('Luồng thay thế A1 — Không có dữ liệu', 'Giao diện', 'Quản lý', 'A1.3: Thông báo không đủ dữ liệu để trả lời', True),
            
            ('Luồng thay thế A2 — Dữ liệu vượt quyền', 'Dịch vụ AI', 'Giao diện', 'A2.1: Phát hiện thông tin ngoài thẩm quyền', True),
            ('Luồng thay thế A2 — Dữ liệu vượt quyền', 'Giao diện', 'Quản lý', 'A2.2: Từ chối cung cấp dữ liệu vượt quyền', True),
            
            ('Luồng ngoại lệ E1 — AI không khả dụng', 'Nhà cung cấp AI', 'Dịch vụ AI', 'E1.1: Lỗi service AI / response rỗng', True),
            ('Luồng ngoại lệ E1 — AI không khả dụng', 'Dịch vụ AI', 'Giao diện', 'E1.2: Fallback báo lỗi, không tự tạo câu trả lời', True),
            ('Luồng ngoại lệ E1 — AI không khả dụng', 'Giao diện', 'Quản lý', 'E1.3: Thông báo lỗi dịch vụ AI không khả dụng', True),
        ]
    },
    {
        'code': 'SEQ-012',
        'uc_id': 'UC-012',
        'title': 'AI gợi ý bố trí nhân sự',
        'purpose': 'Mục đích: Đưa ra phương án gợi ý phân bổ ca nhân sự dựa trên dữ liệu cao điểm. Thể hiện luồng thành công, thiếu dữ liệu cao điểm (A1), gợi ý rỗng (A2) và AI timeout/rate limit (E1).',
        'participants': ['Quản lý', 'Giao diện', 'Dịch vụ AI', 'Dịch vụ thống kê', 'Nhà cung cấp AI'],
        'steps': [
            ('Luồng chính thành công', 'Quản lý', 'Giao diện', '1. Yêu cầu gợi ý phương án bố trí nhân sự', False),
            ('Luồng chính thành công', 'Giao diện', 'Dịch vụ AI', '2. Gửi yêu cầu gợi ý nhân sự', False),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Dịch vụ thống kê', '3. Lấy dữ liệu khung giờ cao điểm', False),
            ('Luồng chính thành công', 'Dịch vụ thống kê', 'Dịch vụ AI', '4. Trả về dữ liệu khung giờ cao điểm', True),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Nhà cung cấp AI', '5. Gửi dữ liệu + prompt gợi ý nhân sự', False),
            ('Luồng chính thành công', 'Nhà cung cấp AI', 'Dịch vụ AI', '6. Trả về gợi ý phương án phân bổ ca', True),
            ('Luồng chính thành công', 'Dịch vụ AI', 'Giao diện', '7. Trả về gợi ý kèm lưu ý tham khảo', True),
            ('Luồng chính thành công', 'Giao diện', 'Quản lý', '8. Hiển thị gợi ý cho Quản lý tự quyết định', True),
            
            ('Luồng thay thế A1 — Thiếu dữ liệu cao điểm', 'Dịch vụ thống kê', 'Dịch vụ AI', 'A1.1: Báo dữ liệu cao điểm chưa đủ', True),
            ('Luồng thay thế A1 — Thiếu dữ liệu cao điểm', 'Dịch vụ AI', 'Giao diện', 'A1.2: Báo không đủ cơ sở phân tích', True),
            ('Luồng thay thế A1 — Thiếu dữ liệu cao điểm', 'Giao diện', 'Quản lý', 'A1.3: Thông báo chưa đủ dữ liệu cao điểm', True),
            
            ('Luồng thay thế A2 — Gợi ý AI rỗng/lỗi', 'Dịch vụ AI', 'Giao diện', 'A2.1: Kiểm tra kết quả AI không đạt chất lượng', True),
            ('Luồng thay thế A2 — Gợi ý AI rỗng/lỗi', 'Giao diện', 'Quản lý', 'A2.2: Thông báo không thể đưa ra gợi ý', True),
            
            ('Luồng ngoại lệ E1 — AI timeout/error', 'Nhà cung cấp AI', 'Dịch vụ AI', 'E1.1: Lỗi kết nối / timeout / rate limit', True),
            ('Luồng ngoại lệ E1 — AI timeout/error', 'Dịch vụ AI', 'Giao diện', 'E1.2: Báo lỗi dịch vụ AI', True),
            ('Luồng ngoại lệ E1 — AI timeout/error', 'Giao diện', 'Quản lý', 'E1.3: Báo lỗi AI; không tự động đổi vận hành', True),
        ]
    }
]

# ---------------------------------------------------------
# Build Sơ_đồ_tuần_tự_v_2.0.docx
# ---------------------------------------------------------
print('Starting document assembly for Sơ_đồ_tuần_tự_v_2.0.docx...')
src_doc_path = Path('Sơ_đồ_tuần_tự.docx')
doc = Document(src_doc_path)

# Clear existing paragraphs and tables after header section
# We keep Table 0 (Document Metadata) and modify Table 1 (Diagram List)
print(f'Original paragraph count: {len(doc.paragraphs)}')
print(f'Original table count: {len(doc.tables)}')

# Create fresh Document based on original styles
new_doc = Document('Sơ_đồ_tuần_tự.docx')

# Remove content after paragraph 7 to re-build cleanly with v2.0 format
body = new_doc._body._element
for child in list(body):
    # Keep initial document title / intro if needed, or re-generate standard template
    pass

# We will construct a clean, beautiful Word document from scratch using new_doc styles
doc_target = Document()

# Set standard margins (1 inch = 72 pt)
sections = doc_target.sections
for s in sections:
    s.top_margin = Inches(1)
    s.bottom_margin = Inches(1)
    s.left_margin = Inches(1)
    s.right_margin = Inches(1)

# Title
p_title = doc_target.add_paragraph()
r_title = p_title.add_run('HỆ THỐNG QUẢN LÝ BÃI XE THÔNG MINH')
fmt(r_title, size=18, bold=True, color=(15, 23, 42))
p_sub = doc_target.add_paragraph()
r_sub = p_sub.add_run('TÀI LIỆU SƠ ĐỒ TUẦN TỰ (SEQUENCE DIAGRAMS v2.0)')
fmt(r_sub, size=14, bold=True, color=(37, 99, 235))
p_sub2 = doc_target.add_paragraph()
r_sub2 = p_sub2.add_run('Bổ sung đầy đủ Luồng sự kiện chính, Luồng thay thế (Alt) và Luồng ngoại lệ (Except) theo chuẩn UML 2.5')
fmt(r_sub2, size=10.5, italic=True, color=(71, 85, 105))

# Document Metadata Table
tbl_meta = doc_target.add_table(rows=4, cols=2)
set_table_col_widths(tbl_meta, [2.0, 4.5])
meta_data = [
    ('Nguồn đặc tả', 'Đặc tả UC_done.docx (Nhóm 10 — Đinh Tiến Mạnh, Tạ Văn Đức)'),
    ('Phạm vi hệ thống', '12 Use Case tiêu chuẩn (UC-001 đến UC-012)'),
    ('Quy ước sơ đồ', 'Sequence Diagram chuẩn UML 2.5 với các khối phân nhánh alt / else (StarUML / PlantUML)'),
    ('Phiên bản tài liệu', 'v2.0 — Cập nhật biểu diễn đầy đủ Luồng sự kiện chính & Luồng ngoại lệ/thay thế')
]
for i, (k, v) in enumerate(meta_data):
    row = tbl_meta.rows[i]
    set_cell(row.cells[0], k, bold=True, size=9, color=(15, 23, 42))
    shade_cell(row.cells[0], 'F1F5F9')
    set_cell(row.cells[1], v, bold=False, size=9)

p_space = doc_target.add_paragraph()
p_space.paragraph_format.space_after = Pt(12)

# Section 1: Conventions
h1_1 = doc_target.add_heading(level=1)
r = h1_1.add_run('1. Quy ước thiết kế Sơ đồ tuần tự v2.0')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_conv = doc_target.add_paragraph()
p_conv.paragraph_format.line_spacing = 1.15
r = p_conv.add_run(
    'Mỗi sơ đồ tuần tự trong phiên bản v2.0 được tổng hợp hoàn chỉnh dựa trên đặc tả Use Case tại file "Đặc tả UC_done.docx". '
    'Để đáp ứng tiêu chuẩn phân tích và thiết kế phần mềm chuyên nghiệp (UML 2.5):\n'
    '• Khối phân nhánh `alt` biểu diễn Luồng sự kiện chính (Thành công).\n'
    '• Các khối phân nhánh `else` biểu diễn Luồng sự kiện thay thế (A1, A2...) và Luồng ngoại lệ (E1, E2...).\n'
    '• Các đường mũi tên nét liền đại diện cho thông điệp gọi (Call message), nét đứt đại diện cho thông điệp phản hồi (Return message).\n'
    '• Mỗi Use Case đi kèm hình ảnh sơ đồ UML 2.5 trực quan, Bảng chuỗi thông điệp chi tiết và Mã PlantUML sẵn sàng cho StarUML.'
)
fmt(r, size=10, color=(30, 41, 59))

# Section 2: Summary Table
h1_2 = doc_target.add_heading(level=1)
r = h1_2.add_run('2. Danh mục Sơ đồ tuần tự 12 Use Case')
fmt(r, size=14, bold=True, color=(15, 23, 42))

tbl_sum = doc_target.add_table(rows=1, cols=4)
set_table_col_widths(tbl_sum, [1.0, 2.5, 1.2, 1.8])
headers = ['Mã sơ đồ', 'Tên Use Case', 'Số Participant', 'Phạm vi luồng']
for c, h in zip(tbl_sum.rows[0].cells, headers):
    set_cell(c, h, bold=True, size=9, color=(255, 255, 255))
    shade_cell(c, '1E293B')

for uc in USE_CASES:
    row = tbl_sum.add_row()
    set_cell(row.cells[0], uc['code'], bold=True, size=8.5)
    set_cell(row.cells[1], uc['title'], bold=False, size=8.5)
    set_cell(row.cells[2], str(len(uc['participants'])), bold=False, size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell(row.cells[3], 'Chính + Alt (A1,A2) + Except (E1)', bold=False, size=8.5)

p_space2 = doc_target.add_paragraph()
p_space2.paragraph_format.space_after = Pt(12)

# Section 3+: Detailed Use Cases
for idx, uc in enumerate(USE_CASES, start=1):
    print(f"[{idx}/12] Generating sequence diagram & content for {uc['code']} — {uc['title']}...")
    doc_target.add_page_break()
    
    # Heading 1
    h_uc = doc_target.add_heading(level=1)
    r = h_uc.add_run(f"{uc['code']} — {uc['uc_id']} — {uc['title']}")
    fmt(r, size=13, bold=True, color=(15, 23, 42))
    
    # Purpose & Participants
    p_p = doc_target.add_paragraph()
    p_p.paragraph_format.space_after = Pt(4)
    r = p_p.add_run(uc['purpose'])
    fmt(r, size=9.5, italic=True, color=(51, 65, 85))
    
    p_parts = doc_target.add_paragraph()
    p_parts.paragraph_format.space_after = Pt(8)
    r_lbl = p_parts.add_run('Thành phần (Participants): ')
    fmt(r_lbl, size=9.5, bold=True, color=(30, 41, 59))
    r_val = p_parts.add_run(', '.join(uc['participants']))
    fmt(r_val, size=9.5, bold=False, color=(30, 41, 59))
    
    # Generate Diagram Image
    img_filename = f"{uc['code']}_v2.png"
    img_path = draw_sequence_diagram(f"{uc['uc_id']} — {uc['title']}", uc['participants'], uc['steps'], img_filename)
    
    # Add Image
    doc_target.add_picture(img_path, width=Inches(6.5))
    
    # Caption
    p_cap = doc_target.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run(f"Hình — {uc['code']}: Sơ đồ tuần tự tổng hợp {uc['uc_id']} (Luồng chính & Luồng ngoại lệ)")
    fmt(r_cap, size=8.5, italic=True, color=(100, 116, 139))
    
    # Heading 2: Message Sequence Table
    h2_msg = doc_target.add_heading(level=2)
    r = h2_msg.add_run('Chuỗi thông điệp chi tiết (Luồng chính, Luồng thay thế & Ngoại lệ)')
    fmt(r, size=11, bold=True, color=(30, 41, 59))
    
    # Create Table
    tbl_msg = doc_target.add_table(rows=1, cols=5)
    set_table_col_widths(tbl_msg, [0.45, 1.85, 1.1, 1.1, 2.0])
    msg_headers = ['#', 'Phân nhánh / Điều kiện', 'Từ', 'Đến', 'Thông điệp / Hành vi']
    for c, h in zip(tbl_msg.rows[0].cells, msg_headers):
        set_cell(c, h, bold=True, size=8.5, color=(255, 255, 255))
        shade_cell(c, '334155')
        
    for st_idx, (branch, src, dst, msg, is_ret) in enumerate(uc['steps'], start=1):
        row = tbl_msg.add_row()
        set_cell(row.cells[0], str(st_idx), bold=False, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
        
        # Shade branch column
        set_cell(row.cells[1], branch, bold=True, size=7.5)
        if 'Main' in branch or 'Chính' in branch:
            shade_cell(row.cells[1], 'F0FDF4')
        elif 'E' in branch or 'Ngoại lệ' in branch:
            shade_cell(row.cells[1], 'FEF2F2')
        else:
            shade_cell(row.cells[1], 'FFFBEB')
            
        set_cell(row.cells[2], src, bold=False, size=8)
        set_cell(row.cells[3], dst, bold=False, size=8)
        
        msg_fmt = f"{msg} (Return)" if is_ret else msg
        set_cell(row.cells[4], msg_fmt, bold=False, size=8)
        
    p_sp = doc_target.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(6)
    
    # Heading 2: PlantUML Code Block
    h2_puml = doc_target.add_heading(level=2)
    r = h2_puml.add_run('Mã PlantUML (Đã tích hợp alt / else / end cho StarUML)')
    fmt(r, size=11, bold=True, color=(30, 41, 59))
    
    puml_str = generate_plantuml(uc['title'], uc['code'], uc['participants'], uc['steps'])
    add_code_block(doc_target, puml_str)

# Section Final: Audit Notes
doc_target.add_page_break()
h1_end = doc_target.add_heading(level=1)
r = h1_end.add_run('Ghi chú kiểm chứng & Nguyên tắc xử lý ngoại lệ v2.0')
fmt(r, size=14, bold=True, color=(15, 23, 42))

p_end = doc_target.add_paragraph()
p_end.paragraph_format.line_spacing = 1.15
r = p_end.add_run(
    '1. Các sơ đồ tuần tự v2.0 tuân thủ nguyên tắc không tự sinh nghiệp vụ mới ngoài phạm vi được quy định trong tài liệu "Đặc tả UC_done.docx".\n'
    '2. Nhánh ngoại lệ (E1, E2) tập trung biểu diễn việc gián đoạn luồng chính, thông báo lỗi hệ thống/CSDL/API và hủy bỏ phiên thao tác để bảo toàn tính nhất quán dữ liệu.\n'
    '3. Nhánh thay thế (A1, A2, A3) biểu diễn các phản hồi điều hướng của hệ thống khi dữ liệu đầu vào không hợp lệ hoặc người dùng không đủ quyền thao tác.\n'
    '4. Đối với các UC tích hợp AI (UC-010, UC-011, UC-012), các xử lý fallback khi AI timeout, rate limit hoặc response sai định dạng được biểu diễn rõ ràng nhằm đảm bảo hệ thống không bịa số liệu và không tự động áp đặt quyết định vận hành.'
)
fmt(r, size=10, color=(30, 41, 59))

output_doc_path = Path('Sơ_đồ_tuần_tự_v_2.0.docx')
try:
    doc_target.save(output_doc_path)
    print('====================================================')
    print(f'SUCCESS! File saved to: {output_doc_path.resolve()}')
    print('====================================================')
except PermissionError:
    alt_path = Path('Sơ_đồ_tuần_tự_v_2.0_fixed.docx')
    doc_target.save(alt_path)
    print('====================================================')
    print(f'Sơ_đồ_tuần_tự_v_2.0.docx đang mở trong Word! Đã lưu tạm sang: {alt_path.resolve()}')
    print('Vui lòng đóng file Word và chạy lại script hoặc đổi tên!')
    print('====================================================')


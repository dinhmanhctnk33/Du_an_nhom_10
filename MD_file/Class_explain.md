@startuml

title Mô hình lớp tổng thể — Hệ thống Quản lý Bãi xe Thông minh

left to right direction
skinparam classAttributeIconSize 0
skinparam packageStyle rectangle
skinparam shadowing false
skinparam linetype ortho

' =========================================================
' MODULE 001 — QUẢN LÝ TRUY CẬP
' =========================================================

package "MOD-001 Quản lý truy cập" {

    class TaiKhoanNguoiDung <<thực thể>> {
        -maTaiKhoan: String
        -tenDangNhap: String
        -hoTen: String
        -soDienThoai: String
        -vaiTro: VaiTro
        -trangThai: String
        +coVaiTro(vaiTro): boolean
    }

    class VaiTro <<thực thể>> {
        -maVaiTro: String
        -tenVaiTro: String
    }

    class DichVuXacThuc <<dịch vụ>> {
        +xacThuc(tenDangNhap, matKhau)
        +phanQuyen(taiKhoan, vaiTro)
    }
}

' =========================================================
' MODULE 002 — DANH MỤC BÃI XE
' =========================================================

package "MOD-002 Danh mục bãi xe" {

    class KhuVuc <<thực thể>> {
        -maKhuVuc: String
        -tenKhuVuc: String
        -sucChua: int
        +laySoViTriTrong(): int
    }

    class ViTriDoXe <<suy diễn>> {
        -maViTri: String
        -trangThai: TrangThaiViTri
        +capNhatTrangThai(trangThai): void
    }

    class LoaiXe <<thực thể>> {
        -maLoaiXe: String
        -tenLoaiXe: String
        +phuHopVoi(xe): boolean
    }

    class VeThang <<thực thể>> {
        -maVeThang: String
        -tenKhachHang: String
        -soDienThoai: String
        -ngayBatDau: Date
        -ngayKetThuc: Date
        -tuDongGiaHan: boolean
        -trangThai: String
        +conHieuLucTai(thoiDiem): boolean
    }
}

' =========================================================
' MODULE 003 — VẬN HÀNH BÃI XE
' =========================================================

package "MOD-003 Vận hành bãi xe" {

    class Xe <<thực thể>> {
        -maNhanDien: String
        -mauXe: String
        +dinhDangBienSo(): String
    }

    class VeGuiXe <<thực thể>> {
        -maVe: String
        -loaiVe: String
        -trangThai: String
        +hopLe(): boolean
    }

    class LuotGuiXe <<thực thể>> {
        -maLuotGui: String
        -thoiGianVao: DateTime
        -thoiGianRa: DateTime
        -bienSoKiemTra: String
        -tongPhi: BigDecimal
        -trangThai: String
        +ketThucLuotGui(thoiGianRa)
        +ganPhi(soTien)
    }

    class BangGia <<thực thể>> {
        -maQuyTacGia: String
        -kieuApDung: String
        -giaCoBan: BigDecimal
        -donViThoiGianPhut: int
        -giaBoSung: BigDecimal
        -phuPhiBanDem: BigDecimal
        -thoiDiemHieuLuc: DateTime
        +tinhPhi(thoiLuong): BigDecimal
    }
}

' =========================================================
' MODULE 004 — TRA CỨU VÀ BÁO CÁO
' =========================================================

package "MOD-004 Tra cứu và báo cáo" {

    class ThongKeBaiXe <<DTO>> {
        -loaiBaoCao: String
        -ngayBatDau: Date
        -ngayKetThuc: Date
        -tongLuotGui: int
        -tongDoanhThu: BigDecimal
        -tyLeLapDayTrungBinh: double
        -khungGioCaoDiem: String
        -thoiDiemTao: DateTime
        +tongHop(): DTO
    }

    class DichVuTraCuuBaiXe <<dịch vụ>> {
        +timTheoXe(xe)
    }

    class DichVuBaoCao <<dịch vụ>> {
        +lapThongKe(kyBaoCao)
    }
}

' =========================================================
' MODULE 005 — TÍCH HỢP AI
' =========================================================

package "MOD-005 Tích hợp AI" {

    class DichVuPhanTichAI <<dịch vụ>> {
        +sinhBaoCao()
        +traLoiCauHoi()
    }

    class MauLenhAI <<thành phần>> {
        +taoLenh(nguCanh)
    }

    class BoCungCapNguCanhThongKe <<thành phần>> {
        +cungCapNguCanh(vaiTro)
    }

    class BoKetNoiAI <<thành phần>> {
        +yeuCauPhanTich(lenh)
    }

    class BoKiemTraPhanHoiAI <<thành phần>> {
        +kiemTra(phanHoiTho)
    }
}

' =========================================================
' TẦNG TRUY CẬP DỮ LIỆU
' =========================================================

package "Tầng truy cập dữ liệu" {

    class KhoDuLieuBaiXe <<repository>> {
        +luu(doiTuong)
        +timTheoMa(ma)
    }
}

' =========================================================
' QUAN HỆ — QUẢN LÝ TRUY CẬP
' =========================================================

TaiKhoanNguoiDung "*" --> "1" VaiTro : đượcGán

DichVuXacThuc ..> TaiKhoanNguoiDung : xácThực
DichVuXacThuc ..> VaiTro : phânQuyền
DichVuXacThuc ..> KhoDuLieuBaiXe : sửDụng

' =========================================================
' QUAN HỆ — DANH MỤC BÃI XE
' =========================================================

KhuVuc "1" --> "0..*" ViTriDoXe : cungCấp

KhuVuc "*" --> "1" LoaiXe : dànhCho

Xe "*" --> "1" LoaiXe : thuộcLoại

VeThang "*" --> "1" Xe : đượcCấpCho

' =========================================================
' QUAN HỆ — VẬN HÀNH BÃI XE
' =========================================================

LuotGuiXe "*" --> "1" Xe : ghiNhận

LuotGuiXe "*" --> "1" VeGuiXe : sửDụng

LuotGuiXe "*" --> "1" KhuVuc : diễnRaTại

LuotGuiXe "*" --> "0..1" ViTriDoXe : chiếmDụng

LuotGuiXe "*" --> "1" BangGia : đượcTínhTheo

LuotGuiXe "*" --> "1" TaiKhoanNguoiDung : nhânViênVào

LuotGuiXe "*" --> "0..1" TaiKhoanNguoiDung : nhânViênRa

BangGia "*" --> "1" LoaiXe : ápDụngCho

' =========================================================
' QUAN HỆ — TRA CỨU VÀ BÁO CÁO
' =========================================================

DichVuTraCuuBaiXe ..> Xe : traCứuTheo

DichVuTraCuuBaiXe ..> LuotGuiXe : trảVề

DichVuBaoCao ..> LuotGuiXe : tổngHợp

DichVuBaoCao ..> ThongKeBaiXe : xâyDựng

ThongKeBaiXe "*" --> "1" KhuVuc : thốngKêCho

' =========================================================
' QUAN HỆ — TÍCH HỢP AI
' =========================================================

DichVuPhanTichAI --> MauLenhAI : sửDụng

DichVuPhanTichAI --> BoCungCapNguCanhThongKe : lấyNguCanh

DichVuPhanTichAI --> BoKetNoiAI : ủyQuyền

DichVuPhanTichAI --> BoKiemTraPhanHoiAI : kiểmTra

BoCungCapNguCanhThongKe ..> ThongKeBaiXe : đọcDữLiệu

DichVuPhanTichAI ..> DichVuBaoCao : yêuCầuThốngKê

' =========================================================
' QUAN HỆ — TẦNG TRUY CẬP DỮ LIỆU
' =========================================================

DichVuTraCuuBaiXe ..> KhoDuLieuBaiXe : đọcDữLiệu

DichVuBaoCao ..> KhoDuLieuBaiXe : đọcDữLiệu

KhoDuLieuBaiXe ..> LuotGuiXe : lưuTrữ

KhoDuLieuBaiXe ..> Xe : lưuTrữ

KhoDuLieuBaiXe ..> VeGuiXe : lưuTrữ

KhoDuLieuBaiXe ..> TaiKhoanNguoiDung : lưuTrữ

' =========================================================
' GHI CHÚ THIẾT KẾ
' =========================================================

note right of ViTriDoXe

    <<suy diễn>>

    Vị trí đỗ xe không phải là
    thực thể được lưu trực tiếp
    trong CSDL.

    Số vị trí trống được suy diễn
    từ sức chứa của KhuVuc và
    các LuotGuiXe đang hoạt động.

end note

note bottom of KhoDuLieuBaiXe

    Kho truy cập dữ liệu dùng chung.

    Khi triển khai thực tế có thể
    tách thành các Repository
    chuyên biệt theo từng thực thể.

end note

@enduml
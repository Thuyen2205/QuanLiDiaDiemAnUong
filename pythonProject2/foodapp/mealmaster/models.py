from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django import forms
# Create your models here.


class LoaiTaiKhoan(models.Model):
    ten_loai_tai_khoan = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.ten_loai_tai_khoan


class KiemDuyet(models.Model):
    ten_loai_kiem_duyet = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.ten_loai_kiem_duyet


class TaiKhoan(AbstractUser):
    ten_nguoi_dung = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    ngay_sinh = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    dia_chi = models.CharField(max_length=50, null=True, blank=True)
    sdt = models.CharField(max_length=50, null=True, blank=True)
    avatar = CloudinaryField('avatar',null=True)
    kinh_do = models.FloatField(null=True, blank=True, default=0)
    vi_do = models.FloatField(null=True, blank=True, default=0)
    gioi_tinh = models.BooleanField(default=False, null=True, blank=True)
    loai_tai_khoan = models.ForeignKey(LoaiTaiKhoan, on_delete=models.PROTECT, null=True, blank=True)
    kiem_duyet = models.ForeignKey(KiemDuyet, on_delete=models.PROTECT, null=True, blank=True)
    thoi_gian_mo_cua = models.DateTimeField(null=True, blank=True)
    thoi_gian_dong_cua = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class LoaiDiaChi(models.Model):
    ten_loai_dia_chi = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.ten_loai_dia_chi


class ThongTinGiaoHang(models.Model):
    dia_chi = models.CharField(max_length=50, null=False, blank=False)
    loai_dia_chi = models.ForeignKey(LoaiDiaChi, on_delete=models.PROTECT, null=False, blank=False)
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.PROTECT, null=False, blank=False)
    ten_nguoi_nhan = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.ten_nguoi_nhan


class TimKiem(models.Model):
    ten_mon = models.CharField(max_length=50, null=False, blank=False)
    ten_loai_thuc_an = models.CharField(max_length=50, null=False, blank=False)
    ten_cua_hang = models.CharField(max_length=50, null=False, blank=False)
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.ten_loai_thuc_an


class BinhLuan(models.Model):
    noi_dung = models.CharField(max_length=50, null=False, blank=False)
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=False, blank=False)
    binh_luan_cha = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # hinh_anh = models.ImageField(upload_to='binhluanimg', null=True, blank=True)
    Img = models.ImageField(upload_to='binhluanimg', null=True, blank=True)
    mon_an_binh_luan = models.ForeignKey('MonAn', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.noi_dung


class Menu(models.Model):
    ngay_tao = models.DateTimeField(auto_now_add=True)
    tieu_de = models.CharField(max_length=50, null=True, blank=True)
    mon_an = models.ManyToManyField('MonAn', through='ChiTietMenu', related_name='menus')
    trang_thai = models.BooleanField(default=True)
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=True, blank=True)
    hinh_anh= CloudinaryField('avatar',null=True)

    def __str__(self):
        return self.tieu_de


class ChiTietMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False, blank=False)
    mon_an = models.ForeignKey('MonAn', on_delete=models.CASCADE, null=False, blank=False)
    so_luong = models.IntegerField(null=False, blank=False, default=0)


class LoaiThucAn(models.Model):
    ten_loai_thuc_an = models.CharField(max_length=50, null=False, blank=False)
    hinh_anh = CloudinaryField('hinh_anh',null=True)

    def __str__(self):
        return self.ten_loai_thuc_an


class ThoiDiem(models.Model):
    ten_buoi = models.CharField(max_length=50, null=True, blank=True)
    thoi_gian_bat_dau = models.TimeField()
    thoi_gian_ket_thuc = models.TimeField()
    mon_an = models.ManyToManyField('MonAn', through='ThoiGianBan', related_name='thoidiems')

    def __str__(self):
        return self.ten_buoi


class ThoiGianBan(models.Model):
    thoi_diem = models.ForeignKey(ThoiDiem, on_delete=models.CASCADE, null=False, blank=False)
    mon_an = models.ForeignKey('MonAn', on_delete=models.CASCADE, null=True, blank=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return self.thoi_diem


class HoaDon(models.Model):
    ngay_tao = models.DateTimeField(auto_now_add=True)
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=False, blank=False)
    mon_an = models.ManyToManyField('MonAn', through='ChiTietHoaDon', related_name='hoadons')

    def __str__(self):
        return self.ngay_tao


class ChiTietHoaDon(models.Model):
    hoa_don = models.ForeignKey(HoaDon, on_delete=models.CASCADE, null=False, blank=False)
    mon_an = models.ForeignKey('MonAn', on_delete=models.CASCADE, null=False, blank=False)
    so_luong = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.hoa_don


class MonAn(models.Model):
    ten_mon_an = models.CharField(max_length=50, null=True, blank=True)
    gia_mon_an = models.IntegerField(null=True, blank=True)
    mo_ta = models.CharField(max_length=50, null=True, blank=True)
    loai_thuc_an = models.ForeignKey(LoaiThucAn, on_delete=models.CASCADE, null=True, blank=True)
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=True, blank=True)
    trang_thai = models.BooleanField(default=True)
    hinh_anh = CloudinaryField('hinh_anh',null=True)
    so_luong = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.ten_mon_an


class Follow(models.Model):
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=False, blank=False,
                                   related_name='nguoi_dung_follow')
    cua_hang = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=False, blank=False,
                                 related_name='cua_hang_follow')

    def __str__(self):
        return self.nguoi_dung


class DanhGia(models.Model):
    nguoi_dung = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=False, blank=False,
                                   related_name='nguoi_dung_danh_gia')
    cua_hang = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='cua_hang_danh_gia')
    mon_an = models.ForeignKey(MonAn, on_delete=models.CASCADE, null=True, blank=True)
    diem_so = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.nguoi_dung


class Voucher(models.Model):
    ten_voucher = models.CharField(max_length=50, null=False, blank=False)
    ti_so = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.ten_voucher

class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)
    userId=forms.IntegerField()
    cartItemIds = forms.CharField(widget=forms.HiddenInput(), required=False)

class Payment_VNPay(models.Model):
    order_id = models.BigIntegerField(default=0, null=True, blank=True)
    amount=models.FloatField(default=0.0,null=True,blank=True)
    order_desc=models.CharField(max_length=200,null=True,blank=True)
    vnp_TransactionNo=models.CharField(max_length=200,null=True,blank=True)
    vnp_ResponseCode=models.CharField(max_length=200,null=True, blank=True)
    khach_hang=models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=True, blank=True)
    # mon_an=models.ForeignKey(MonAn,on_delete=models.CASCADE,null=True,blank=True)
    mon_an = models.ManyToManyField('MonAn', through='ChiTietHoaDonVNPay', related_name='hoadon_vnpay')
    cartItemIds = models.CharField(max_length=200, null=True, blank=True)


class ChiTietHoaDonVNPay(models.Model):
    hoa_don = models.ForeignKey(Payment_VNPay, on_delete=models.CASCADE, null=False, blank=False)
    mon_an = models.ForeignKey('MonAn', on_delete=models.CASCADE, null=False, blank=False)




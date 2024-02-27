from django.db.models import Count,F

from .models import TaiKhoan,LoaiTaiKhoan

def count_khachhang():
    count = TaiKhoan.objects.filter(loai_tai_khoan=1).count()
    return count

def count_cuahang():
    count = TaiKhoan.objects.filter(loai_tai_khoan=2).count()
    return count
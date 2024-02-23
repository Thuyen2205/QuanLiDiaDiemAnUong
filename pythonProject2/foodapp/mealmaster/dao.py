from django.db.models import Count,F

from .models import TaiKhoan,LoaiTaiKhoan

def count_taikhoan():
    return TaiKhoan.objects.count()



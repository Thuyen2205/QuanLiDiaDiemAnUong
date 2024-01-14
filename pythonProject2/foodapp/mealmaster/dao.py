from django.db.models import Count,F

from .models import TaiKhoan,LoaiTaiKhoan

def count_taikhoan():

    return TaiKhoan.objects.filter(kiem_duyet=1).annotate(tong_so_luong=Count('id')).values('id', 'ten_nguoi_dung', 'loai_tai_khoan_id')



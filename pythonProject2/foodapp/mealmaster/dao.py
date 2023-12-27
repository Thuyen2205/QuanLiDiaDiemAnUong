from django.db.models import Count

from .models import TaiKhoan,LoaiTaiKhoan

def count_taikhoan():

    return TaiKhoan.objects.annotate(Count('id')).values('id','ten_nguoi_dung','loai_tai_khoan_id').all()



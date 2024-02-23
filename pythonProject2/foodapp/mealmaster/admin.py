from django.contrib import admin
from django.template.response import TemplateResponse

from .models import (TaiKhoan,LoaiTaiKhoan,KiemDuyet,LoaiThucAn,LoaiDiaChi,
                     MonAn,HoaDon,Menu,ChiTietMenu,ChiTietHoaDon,ThoiDiem)
# Register your models here.
from django.urls import path
from . import dao


class TaiKhoanAdminSite(admin.AdminSite):
    site_header = 'Thong Kê Tài Khoản'

    def get_urls(self):
        return [
            path('taikhoan-stats/',self.stats_view)
        ] +super().get_urls()

    def stats_view(self,request):
        return TemplateResponse(request,'admin/stats.html',{
            'count':dao.count_taikhoan()
        })



admin_site=TaiKhoanAdminSite(name='Tai Khoan')



class TaiKhoanAdmin(admin.ModelAdmin):
    list_display = ["id","ten_nguoi_dung","username","ngay_sinh","loai_tai_khoan"]
    search_fields = ["ten_nguoi_dung","loai_tai_khoan__ten_loai_tai_khoan"]
    list_filter = ["ten_nguoi_dung","username","ngay_sinh"]
    class Media:
        css={
            'all': ('/static/css/style.css',)
        }

admin_site.register(TaiKhoan,TaiKhoanAdmin)
admin_site.register(LoaiTaiKhoan)
admin_site.register(KiemDuyet)
admin_site.register(LoaiThucAn)
admin_site.register(MonAn)
admin_site.register(Menu)
admin_site.register(ChiTietMenu)
admin_site.register(ThoiDiem)
admin_site.register(LoaiDiaChi)
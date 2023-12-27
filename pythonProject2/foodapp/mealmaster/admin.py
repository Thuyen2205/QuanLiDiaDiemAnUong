from django.contrib import admin
from django.template.response import TemplateResponse

from .models import (TaiKhoan,LoaiTaiKhoan,KiemDuyet,LoaiThucAn,LoaiDiaChi,
                     MonAn,HoaDon,Menu,ChiTietMenu,ChiTietHoaDon)
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
            'stats':dao.count_taikhoan()
        })



admin_site=TaiKhoanAdminSite(name='Tai Khoan')



class TaiKhoanAdmin(admin.ModelAdmin):


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
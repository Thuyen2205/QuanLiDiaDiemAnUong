from django.contrib import admin
from django.template.response import TemplateResponse
from django import forms

from .models import (TaiKhoan, LoaiTaiKhoan, KiemDuyet, LoaiThucAn, LoaiDiaChi,
                     MonAn, HoaDon, Menu, ChiTietMenu, ChiTietHoaDon, ThoiDiem)
# Register your models here.
from django.urls import path
from . import dao


class YearForm(forms.Form):
    year_choices = [(str(year), str(year)) for year in range(2015, 2026)]
    year = forms.ChoiceField(choices=year_choices, label='Chọn năm')
    # month_choices = [(str(month), str(month)) for month in range(1, 13)]
    # month = forms.ChoiceField(choices=month_choices, label='Chọn tháng')


class MonthYearForm(forms.Form):
    year_choices = [(str(year), str(year)) for year in range(2020, 2030)]
    month_choices = [(str(month), str(month)) for month in range(1, 13)]

    year = forms.ChoiceField(choices=year_choices, label='Chọn năm')
    month = forms.ChoiceField(choices=month_choices, label='Chọn tháng')


class QuarterYearForm(forms.Form):
    year = forms.IntegerField(label='Năm', min_value=1900, max_value=2100)
    quarter = forms.IntegerField(label='Quý', min_value=1, max_value=4)



class TaiKhoanAdminSite(admin.AdminSite):
    site_header = 'Thong Kê Tài Khoản'

    def get_urls(self):
        return [
                   path('taikhoan-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'count_khachhang': dao.count_khachhang(), 'count_cuahang': dao.count_cuahang(),

        })


class KhachHangAdminSite(admin.AdminSite):
    site_header = 'Thong Kê Khach Hang'

    def get_urls(self):
        return [
                   path('khachhang-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats_khachhang.html', {

            'total_amount_by_customer': dao.count_tong_tien_mua,

        })


class CuaHangAdminSite(admin.AdminSite):
    site_header = 'Thong Kê Cưa Hang'

    def get_urls(self):
        return [
                   path('cuahang-stats/', self.stats_view, name='cuahang_stats'),
                   path('cuahang-stats-by-year/', self.stats_by_year_view, name='cuahang_stats_by_year'),
                   path('cuahang-stats-by-month/', self.stats_by_month_view, name='cuahang_stats_by_month'),
                   path('cuahang-stats-by-quarter/', self.stats_by_quarter_view, name='cuahang_stats_by_quarter'),

               ] + super().get_urls()

    def stats_view(self, request):
        year_form = YearForm(request.GET)

        if year_form.is_valid():
            year = year_form.cleaned_data['year']
            users_with_amount_by_year = dao.total_amount_by_year(year)
        else:
            users_with_amount_by_year = []

        users_with_amount = dao.users_with_total_amount()

        return TemplateResponse(request, 'admin/stats_cuahang.html', {
            'users_with_amount': users_with_amount,

        })

    def stats_by_year_view(self, request):
        year_form = YearForm(request.GET)

        if year_form.is_valid():
            year = year_form.cleaned_data['year']
            users_with_amount_by_year = dao.total_amount_by_year(year)
        else:
            users_with_amount_by_year = []

        return TemplateResponse(request, 'admin/stats_cuahang_year.html', {
            'users_with_amount_by_year': users_with_amount_by_year,
            'year_form': year_form,
        })

    def stats_by_month_view(self, request):
        form = MonthYearForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            users_with_amount_by_month = dao.total_amount_by_month(year, month)
        else:
            users_with_amount_by_month = []
        return TemplateResponse(request, 'admin/stats_cuahang_month.html', {
            'users_with_amount_by_month': users_with_amount_by_month,
            'year_month_form': form,

        })

    def stats_by_quarter_view(self, request):
        form = QuarterYearForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data['year']
            quarter = form.cleaned_data['quarter']

            users_with_amount_by_quarter = dao.total_amount_by_quarter(year, quarter)
        else:
            users_with_amount_by_quarter = []

        return TemplateResponse(request, 'admin/stats_cuahang_quarter.html', {
            'users_with_amount_by_quarter': users_with_amount_by_quarter,
            'quarter_year_form': form,
        })


admin_site = TaiKhoanAdminSite(name='Tai Khoan')
khachhang_site = KhachHangAdminSite(name='Khach Hang')
cuahang_site = CuaHangAdminSite(name='cuahang_admin')


class TaiKhoanAdmin(admin.ModelAdmin):
    list_display = ["id", "ten_nguoi_dung", "username", "ngay_sinh", "loai_tai_khoan"]
    search_fields = ["ten_nguoi_dung", "loai_tai_khoan__ten_loai_tai_khoan"]
    list_filter = ["ten_nguoi_dung", "username", "ngay_sinh"]

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }


cuahang_site.register(TaiKhoan, TaiKhoanAdmin)
khachhang_site.register(TaiKhoan, TaiKhoanAdmin)


admin_site.register(TaiKhoan, TaiKhoanAdmin)
admin_site.register(LoaiTaiKhoan)
admin_site.register(KiemDuyet)
admin_site.register(LoaiThucAn)
admin_site.register(MonAn)
admin_site.register(Menu)
admin_site.register(ChiTietMenu)
admin_site.register(ThoiDiem)
admin_site.register(LoaiDiaChi)

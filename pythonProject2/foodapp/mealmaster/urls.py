from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path,include
from .admin import admin_site



router = DefaultRouter()
router.register('taikhoans',views.TaiKhoanViewSet)
router.register('monan',views.MonAnViewSet, basename="them")
router.register('menu',views.MenuViewSet)
router.register('loaitaikhoan',views.LoaiTaiKhoanViewSet)
router.register('themmonan',views.ThemMonAnViewSet)
router.register('binhluan',views.BinhLuanViewSet, basename="binhluan")
router.register('traloibinhluan',views.TraLoiBinhLuanViewSet, basename="traloibinhluan")
router.register('loaithucan',views.LoaiThucAnViewSet)
router.register('chitietmenu',views.ChiTietMenuViewSet)
router.register('hoadon',views.HoaDonViewSet,basename="hoadon")
router.register('chitiethoadon',views.ChiTietHoaDonViewset, basename="chitiethoadon")
router.register('follow',views.FollowViewSet)
router.register('danhgia',views.DanhGiaViewSet)
router.register('thongtingiaohang',views.ThongTinGiaoHangView)
router.register('taikhoandangnhap',views.ThongTinTaiKhoanView, basename="taikhoangdangnhap")











#/taikhoan/ - Get

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
]


from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from .admin import admin_site,khachhang_site,cuahang_site
from .views import SearchMonAnViewSet
# from .views import create_payment

router = DefaultRouter()
router.register('taikhoans', views.TaiKhoanViewSet)
router.register('monan', views.MonAnViewSet, basename="them")
router.register('menu', views.MenuViewSet)
router.register('loaitaikhoan', views.LoaiTaiKhoanViewSet)
router.register('themmonan', views.ThemMonAnViewSet)
router.register('binhluan', views.BinhLuanViewSet, basename="binhluan")
router.register('traloibinhluan', views.TraLoiBinhLuanViewSet, basename="traloibinhluan")
router.register('loaithucan', views.LoaiThucAnViewSet)
router.register('chitietmenu', views.ChiTietMenuViewSet)
router.register('hoadon', views.HoaDonViewSet, basename="hoadon")
router.register('chitiethoadon', views.ChiTietHoaDonViewset, basename="chitiethoadon")
router.register('follow', views.FollowViewSet)
router.register('danhgia', views.DanhGiaViewSet)
router.register('thongtingiaohang', views.ThongTinGiaoHangView)
router.register('taikhoandangnhap', views.ThongTinTaiKhoanView, basename="taikhoangdangnhap")
router.register('thoidiem', views.ThoiDiemView)
router.register('thoigianban', views.ThoiGianBanView)
router.register('monanhientai', views.MonAnHienTaiViewSet)
router.register('menuhientai', views.MenuHienTaiViewSet, basename="menuhientai")
router.register(r'searchmonan', SearchMonAnViewSet, basename='searchmonan')
router.register('chitiethoadonvnpay', views.ChiTietHoaDonVNPayViewSet, basename="chitiethoadonvnpay")
router.register('payment_vnpay', views.Payment_VNPayViewSet, basename="payment_vnpay")



urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls, name='admin'),
    path('khachhang-admin/', khachhang_site.urls, name='khachhang_admin'),
    path('cuahang-admin/', cuahang_site.urls, name='cuahang_admin'),

    path('api/search-mon-an/<str:ten_mon_an>/', SearchMonAnViewSet.as_view({'get': 'list'}),
         name='search_mon_an'),
    # path('payment-request/', create_payment, name='create-payment'),
    path('pay', views.index, name='index'),
    path('payment', views.payment, name='payment'),
    path('payment_ipn', views.payment_ipn, name='payment_ipn'),
    path('payment_return', views.payment_return, name='payment_return'),
    path('query',views.query, name='query'),
    path('refund', views.refund, name='refund'),
    # path('admin/', admin.site.urls),

]

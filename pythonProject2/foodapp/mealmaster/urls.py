from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path,include
from .admin import admin_site
from .views import LoginViewSet



router = DefaultRouter()
router.register('taikhoans',views.TaiKhoanViewSet)
router.register('monan',views.MonAnViewSet, basename="them")
router.register('menu',views.MenuViewSet)
router.register('loaitaikhoan',views.LoaiTaiKhoanViewSet)
router.register('themmonan',views.ThemMonAnViewSet)
router.register('binhluan',views.BinhLuanViewSet, basename="binhluan")
router.register('traloibinhluan',views.TraLoiBinhLuanViewSet, basename="traloibinhluan")
router.register('loaithucan',views.LoaiThucAnViewSet)


#/taikhoan/ - Get

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('api/login/', LoginViewSet.as_view(),name='user-login')
]


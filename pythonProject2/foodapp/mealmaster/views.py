from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import authentication
from oauthlib.uri_validate import query
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import TaiKhoan, MonAn, Menu, LoaiTaiKhoan, BinhLuan, LoaiThucAn, ChiTietMenu, HoaDon, ChiTietHoaDon, \
    Follow, DanhGia, ThongTinGiaoHang, ThoiDiem, ThoiGianBan
from .serializers import (TaiKhoanSerializer, MonAnSerializer,
                          MenuSerializer, LoaiTaiKhoanSerializer, ThemMonAnSerializer,
                          BinhLuanSerializer, TraLoiBinhLuanSerializer, LoaiThucAnSerializer,
                          ChiTietMenuSerializer, HoaDonSerializer, ChiTietHoaDonSerializer,
                          FollowSerializer, DanhGiaSerializer, ThongTinGiaoHangSerializer,
                          ThongTinTaiKhoanSerializer, ThoiDiemSerializer, ThoiGianBanSerializer)
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils import timezone


class MonAnHienTaiViewSet(viewsets.ModelViewSet):
    queryset = MonAn.objects.all()
    serializer_class = MonAnSerializer

    def list(self, request, *args, **kwargs):
        # Lấy thời điểm hiện tại
        current_time = timezone.localtime(timezone.now())
        current_hour = current_time.hour

        print("Giờ hiện tại là:", current_hour)
        current_thoi_gian_bans = ThoiGianBan.objects.filter(thoi_diem__thoi_gian_bat_dau__lte=current_time, thoi_diem__thoi_gian_ket_thuc__gte=current_time)

        mon_an_ids = current_thoi_gian_bans.values_list('mon_an', flat=True)
        queryset = MonAn.objects.filter(id__in=mon_an_ids)

        serializer = MonAnSerializer(queryset, many=True)
        serialized_data = serializer.data

        return Response(serialized_data)


class ThongTinTaiKhoanView(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all()
    serializer_class = ThongTinTaiKhoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaiKhoan.objects.filter(id=self.request.user.id)


class ThoiDiemView(viewsets.ModelViewSet):
    queryset = ThoiDiem.objects.all()
    serializer_class = ThoiDiemSerializer
    # permission_classes = [IsAuthenticated]


class ThoiGianBanView(viewsets.ModelViewSet):
    queryset = ThoiGianBan.objects.all()
    serializer_class = ThoiGianBanSerializer


class ThongTinGiaoHangView(viewsets.ModelViewSet):
    queryset = ThongTinGiaoHang.objects.all()
    serializer_class = ThongTinGiaoHangSerializer


# Create your views here.
class DanhGiaViewSet(viewsets.ModelViewSet):
    queryset = DanhGia.objects.all()
    serializer_class = DanhGiaSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class ChiTietMenuViewSet(viewsets.ModelViewSet):
    queryset = ChiTietMenu.objects.all()
    serializer_class = ChiTietMenuSerializer


class LoaiThucAnViewSet(viewsets.ModelViewSet):
    queryset = LoaiThucAn.objects.all()
    serializer_class = LoaiThucAnSerializer


class MonAnViewSet(viewsets.ModelViewSet):
    queryset = MonAn.objects.all()
    serializer_class = MonAnSerializer




class MenuHienTaiViewSet(viewsets.ModelViewSet):
    queryset=Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        # Lấy thời điểm hiện tại
        current_time = timezone.localtime(timezone.now())
        current_hour = current_time.hour

        print("Giờ hiện tại là:", current_hour)
        current_thoi_gian_bans = ThoiGianBan.objects.filter(thoi_diem__thoi_gian_bat_dau__lte=current_time,
                                                            thoi_diem__thoi_gian_ket_thuc__gte=current_time)

        menu_ids = current_thoi_gian_bans.values_list('menu', flat=True)
        queryset = Menu.objects.filter(id__in=menu_ids)

        serializer = MenuSerializer(queryset, many=True)
        serialized_data = serializer.data

        return Response(serialized_data)



class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


    @action(methods=['post'], detail=True, url_path='active-menu', url_name='active-menu')
    def hide_menu(self, request, pk):
        try:
            mn = Menu.objects.get(pk=pk)
            mn.trang_thai = not mn.trang_thai
            mn.save()
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=MenuSerializer(mn, context={'request': request}).data, status=status.HTTP_200_OK)


    @action(methods=['get'], detail=True, url_path='list-monan', url_name='list-monan')
    def list_monan(self, request, pk):
        # Lấy đối tượng Menu hoặc trả về 404 nếu không tìm thấy
        menu = get_object_or_404(Menu, pk=pk)

        # Lấy danh sách ChiTietMenu của Menu
        chitiet_menu_list = ChiTietMenu.objects.filter(menu=menu)

        monan_list = [chitiet.mon_an for chitiet in chitiet_menu_list]

        # Serialize danh sách MonAn
        serializer = MonAnSerializer(monan_list, many=True, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class TaiKhoanViewSet(viewsets.ViewSet,
                      generics.ListAPIView,
                      generics.CreateAPIView,
                      generics.RetrieveAPIView):
    queryset = TaiKhoan.objects.all()
    serializer_class = TaiKhoanSerializer

    @action(methods=['get'], detail=True, url_path='monans', url_name='monans')
    def list_MonAn_of_TaiKhoan(self, request, *args, **kwargs):
        tai_khoan_id = kwargs.get('pk')

        try:
            tai_khoan = TaiKhoan.objects.get(pk=tai_khoan_id)
            monans = MonAn.objects.filter(nguoi_dung=tai_khoan)
            serializer = MonAnSerializer(monans, many=True)
            return Response(serializer.data)
        except TaiKhoan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='menus', url_name='menus')
    def list_Menu_of_TaiKhoan(self, request, *args, **kwargs):
        tai_khoan_id = kwargs.get('pk')
        try:
            tai_khoan = TaiKhoan.objects.get(pk=tai_khoan_id)
            menus = Menu.objects.filter(nguoi_dung=tai_khoan)
            serializer = MenuSerializer(menus, many=True)
            return Response(serializer.data)
        except TaiKhoan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LoaiTaiKhoanViewSet(viewsets.ModelViewSet):
    queryset = LoaiTaiKhoan.objects.all()
    serializer_class = LoaiTaiKhoanSerializer


class ThemMonAnViewSet(viewsets.ModelViewSet):
    queryset = MonAn.objects.all()
    serializer_class = ThemMonAnSerializer


class BinhLuanViewSet(viewsets.ModelViewSet):
    queryset = BinhLuan.objects.all()
    serializer_class = BinhLuanSerializer


class TraLoiBinhLuanViewSet(viewsets.ModelViewSet):
    queryset = BinhLuan.objects.all()
    serializer_class = TraLoiBinhLuanSerializer


class HoaDonViewSet(viewsets.ModelViewSet):
    queryset = HoaDon.objects.all()
    serializer_class = HoaDonSerializer


class ChiTietHoaDonViewset(viewsets.ModelViewSet):
    queryset = ChiTietHoaDon.objects.all()
    serializer_class = ChiTietHoaDonSerializer

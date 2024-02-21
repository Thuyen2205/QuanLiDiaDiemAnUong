from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import authentication
from oauthlib.uri_validate import query
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

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
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class MonAnHienTaiViewSet(viewsets.ModelViewSet):
    queryset = MonAn.objects.all()
    serializer_class = MonAnSerializer

    def list(self, request, *args, **kwargs):
        # Lấy thời điểm hiện tại
        current_time = timezone.localtime(timezone.now())
        current_hour = current_time.hour

        print("Giờ hiện tại là:", current_hour)
        current_thoi_gian_bans = ThoiGianBan.objects.filter(thoi_diem__thoi_gian_bat_dau__lte=current_time,
                                                            thoi_diem__thoi_gian_ket_thuc__gte=current_time)

        mon_an_ids = current_thoi_gian_bans.values_list('mon_an', flat=True)
        queryset = MonAn.objects.filter(id__in=mon_an_ids)

        serializer = MonAnSerializer(queryset, many=True)
        serialized_data = serializer.data

        return Response(serialized_data)


class ThongTinTaiKhoanView(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all()
    serializer_class = ThongTinTaiKhoanSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaiKhoan.objects.filter(id=self.request.user.id)

    @action(methods=['get'], detail=False, url_path='get-cua-hang', url_name='get-cua-hang')
    def get_cua_hang(self, request):
        try:
            # Lấy thông tin của tài khoản đang đăng nhập
            tai_khoan_dang_nhap = TaiKhoan.objects.get(id=self.request.user.id)

            # Lấy danh sách tất cả các tài khoản (không bao gồm tài khoản đang đăng nhập)
            tai_khoan_khac = TaiKhoan.objects.exclude(id=tai_khoan_dang_nhap.id)

            # Chuyển đổi địa chỉ thành tọa độ và tính toán khoảng cách
            geolocator = Nominatim(user_agent="my_geocoder")
            tai_khoan_khac = [
                {
                    **tk,
                    'location': geolocator.geocode(tk['dia_chi']),
                    'distance': geodesic(
                        (tai_khoan_dang_nhap.vi_do, tai_khoan_dang_nhap.kinh_do),
                        (tk['location'].latitude, tk['location'].longitude)
                    ).meters
                }
                for tk in tai_khoan_khac.values()
            ]

            # Lọc danh sách tài khoản gần nhất (ví dụ: lấy 5 tài khoản đầu tiên)
            tai_khoan_nearby = sorted(tai_khoan_khac, key=lambda x: x['distance'])[:5]

            # Chuyển danh sách tài khoản thành dạng JSON
            tai_khoan_nearby_data = [
                {
                    'id': tk['id'],
                    'ten_nguoi_dung': tk['ten_nguoi_dung'],
                    'sdt': tk['sdt'],
                    'dia_chi': tk['dia_chi'],
                    'kinh_do': tk['kinh_do'],
                    'vi_do': tk['vi_do'],
                    'distance': tk['distance'],
                }
                for tk in tai_khoan_nearby
            ]

            return Response(tai_khoan_nearby_data, status=status.HTTP_200_OK)

        except TaiKhoan.DoesNotExist:
            return Response({'error': 'TaiKhoan not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class SearchMonAnViewSet(viewsets.ModelViewSet):
    serializer_class = MonAnSerializer

    def get_queryset(self):
        ten_mon_an = self.kwargs.get('ten_mon_an', None)

        # Lấy thời điểm hiện tại
        current_time = timezone.localtime(timezone.now())

        # Lấy danh sách các món ăn có thời gian bán hiện tại
        current_thoi_gian_bans = ThoiGianBan.objects.filter(
            thoi_diem__thoi_gian_bat_dau__lte=current_time,
            thoi_diem__thoi_gian_ket_thuc__gte=current_time
        )

        mon_an_ids = current_thoi_gian_bans.values_list('mon_an', flat=True)

        # Lọc danh sách món ăn theo tên và thời gian bán hiện tại
        queryset = MonAn.objects.filter(
            Q(ten_mon_an__icontains=ten_mon_an) if ten_mon_an else Q(),
            id__in=mon_an_ids
        )

        return queryset


class MenuHienTaiViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
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

            # Lấy thời điểm hiện tại
            current_time = timezone.localtime(timezone.now())

            # Lấy danh sách các món ăn có thời gian bán hiện tại cho tài khoản
            current_thoi_gian_bans = ThoiGianBan.objects.filter(
                thoi_diem__thoi_gian_bat_dau__lte=current_time,
                thoi_diem__thoi_gian_ket_thuc__gte=current_time,
                mon_an__nguoi_dung=tai_khoan
            )

            mon_an_ids = current_thoi_gian_bans.values_list('mon_an', flat=True)
            queryset = MonAn.objects.filter(id__in=mon_an_ids)

            serializer = MonAnSerializer(queryset, many=True)
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

    @action(methods=['get'], detail=False, url_path='loai-tai-khoan-2', url_name='loai-tai-khoan-2')
    def list_TaiKhoan_with_loai_tai_khoan_2(self, request, *args, **kwargs):
        try:
            tai_khoans = TaiKhoan.objects.filter(loai_tai_khoan=2)
            serializer = TaiKhoanSerializer(tai_khoans, many=True)
            return Response(serializer.data)
        except TaiKhoan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='loai-tai-khoan-1', url_name='loai-tai-khoan-1')
    def list_TaiKhoan_with_loai_tai_khoan_1(self, request, *args, **kwargs):
        try:
            tai_khoans = TaiKhoan.objects.filter(loai_tai_khoan=1)
            serializer = TaiKhoanSerializer(tai_khoans, many=True)
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

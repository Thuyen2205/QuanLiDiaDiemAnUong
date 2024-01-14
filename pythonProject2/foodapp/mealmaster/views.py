from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import authentication
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from .models import TaiKhoan, MonAn, Menu, LoaiTaiKhoan, BinhLuan, LoaiThucAn, ChiTietMenu, HoaDon, ChiTietHoaDon, \
    Follow, DanhGia, ThongTinGiaoHang
from .serializers import (TaiKhoanSerializer, MonAnSerializer,
                          MenuSerializer, LoaiTaiKhoanSerializer, ThemMonAnSerializer,
                          BinhLuanSerializer, TraLoiBinhLuanSerializer, LoaiThucAnSerializer,
                          ChiTietMenuSerializer, HoaDonSerializer, ChiTietHoaDonSerializer,
                          FollowSerializer, DanhGiaSerializer, ThongTinGiaoHangSerializer,
                          ThongTinTaiKhoanSerializer)
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class ThongTinTaiKhoanView(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all()
    serializer_class =ThongTinTaiKhoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Chỉ trả về thông tin của tài khoản đăng nhập hiện tại
        return TaiKhoan.objects.filter(id=self.request.user.id)


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


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    # Tạo ra một api mới có đường dẫn /menu/{id}/hide-menu
    @action(methods=['post'], detail=True, url_path='hide-menu', url_name='hide-menu')
    def hide_menu(self, request, pk):
        try:
            mn = Menu.objects.get(pk=pk)
            mn.trang_thai = False
            mn.save()
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=MenuSerializer(mn, context={'request': request}).data, status=status.HTTP_200_OK)


class TaiKhoanViewSet(viewsets.ViewSet,
                      generics.ListAPIView,
                      generics.CreateAPIView,
                      generics.RetrieveAPIView):
    queryset = TaiKhoan.objects.all()
    serializer_class = TaiKhoanSerializer
    # parser_classes = [MultiPartParser, ]


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

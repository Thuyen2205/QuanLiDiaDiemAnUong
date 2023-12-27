from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import authentication
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from .models import TaiKhoan, MonAn, Menu, LoaiTaiKhoan, BinhLuan, LoaiThucAn
from .serializers import (TaiKhoanSerializer, MonAnSerializer,
                          MenuSerializer, LoaiTaiKhoanSerializer, ThemMonAnSerializer,
                          BinhLuanSerializer, TraLoiBinhLuanSerializer, LoaiThucAnSerializer, LoginSerializer)
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.


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
    parser_classes = [MultiPartParser, ]


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


class LoginViewSet(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Tên đăng nhập hoặc mật khẩu không chính xác'},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

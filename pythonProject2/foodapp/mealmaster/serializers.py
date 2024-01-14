from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import (TaiKhoan, MonAn, Menu, LoaiTaiKhoan, KiemDuyet, LoaiThucAn, BinhLuan,
                     Follow, ChiTietMenu, HoaDon, ChiTietHoaDon, DanhGia, ThongTinGiaoHang, LoaiDiaChi)
from django.contrib.auth.hashers import make_password


class ThongTinTaiKhoanSerializer(ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = ["id", "username","sdt","loai_tai_khoan","ten_nguoi_dung"]


class ThongTinGiaoHangSerializer(ModelSerializer):
    loai_dia_chi = serializers.PrimaryKeyRelatedField(queryset=LoaiDiaChi.objects.all())

    class Meta:
        model = ThongTinGiaoHang
        fields = ["id", "dia_chi", "ten_nguoi_nhan", "loai_dia_chi", "nguoi_dung"]


class TaiKhoanSerializer(ModelSerializer):
    loai_tai_khoan = serializers.PrimaryKeyRelatedField(queryset=LoaiTaiKhoan.objects.all())

    gioi_tinh_select = (
        (0, 'Nam'),
        (1, 'Nữ')
    )

    gioi_tinh = serializers.ChoiceField(choices=gioi_tinh_select)

    class Meta:
        model = TaiKhoan
        fields = ['id', 'ten_nguoi_dung', 'email', 'sdt', 'username', 'password', 'avatar',
                  'gioi_tinh',
                  'ngay_sinh',
                  'ngay_sinh',
                  'kiem_duyet_id',
                  'loai_tai_khoan']
        # read_only_fields = ['gio_hang_id']

    def create(self, validated_data):
        kiem_duyet_default = KiemDuyet.objects.get(pk=1)
        validated_data['kiem_duyet_id'] = kiem_duyet_default.id

        password = validated_data.pop('password', None)

        tai_khoan = TaiKhoan.objects.create(**validated_data)
        if password:
            tai_khoan.password = make_password(password)
            tai_khoan.save()
        return tai_khoan


class CuaHangSerializer(ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = ['ten_nguoi_dung', 'email', 'sdt', 'avatar', 'gioi_tinh', 'kinh_do',
                  'vi_do', 'gioi_tinh']


class MonAnSerializer(ModelSerializer):
    class Meta:
        model = MonAn
        fields = ["id", "ten_mon_an", "gia_mon_an", "hinh_anh", "mo_ta", "nguoi_dung"]


class LoaiThucAnSerializer(ModelSerializer):
    class Meta:
        model = LoaiThucAn
        fields = ["id", "ten_loai_thuc_an"]


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "tieu_de", "trang_thai", "nguoi_dung"]


class LoaiTaiKhoanSerializer(ModelSerializer):
    taikhoan_set = TaiKhoanSerializer(many=True)

    class Meta:
        model = LoaiTaiKhoan
        fields = ["id", "ten_loai_tai_khoan", "taikhoan_set"]


class ThemMonAnSerializer(ModelSerializer):
    loai_thuc_an = serializers.PrimaryKeyRelatedField(queryset=LoaiThucAn.objects.all())

    class Meta:
        model = MonAn
        fields = ["ten_mon_an", "gia_mon_an", "mo_ta", "hinh_anh",
                  "so_luong", "loai_thuc_an"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                tai_khoan = TaiKhoan.objects.get(username=request.user.username)
                validated_data['nguoi_dung_id'] = tai_khoan.id
                mon_an = MonAn.objects.create(**validated_data)
                return mon_an
            except TaiKhoan.DoesNotExist:
                raise serializers.ValidationError("Không thể tạo món ăn")

        raise serializers.ValidationError("Vui lòng đăng nhập để thêm món ăn")


class BinhLuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinhLuan
        fields = ["noi_dung"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                tai_khoan = TaiKhoan.objects.get(username=request.user.username)

                validated_data['nguoi_dung_id'] = tai_khoan.id
                binh_luan = BinhLuan.objects.create(**validated_data)
                return binh_luan
            except TaiKhoan.DoesNotExist:
                raise serializers.ValidationError("Không the viết bình luận ")

        raise serializers.ValidationError("Vui lòng đăng nhập để viết bình luận")


class TraLoiBinhLuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinhLuan
        fields = ["noi_dung"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                binh_luan_cha = BinhLuan.objects.all()
                validated_data['binh_luan_cha_id'] = binh_luan_cha
                binh_luan = BinhLuan.objects.create(**validated_data)
                return binh_luan
            except BinhLuan.DoesNotExist:
                raise serializers.ValidationError("Không the viết bình luận ")

        raise serializers.ValidationError("Vui lòng đăng nhập để sử dụng")


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)


class ChiTietMenuSerializer(serializers.ModelSerializer):
    mon_an = serializers.PrimaryKeyRelatedField(queryset=MonAn.objects.all())

    class Meta:
        model = ChiTietMenu
        fields = ["id", "menu", "mon_an", "so_luong"]


class HoaDonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoaDon
        fields = ["id", "nguoi_dung", "ngay_tao"]


class ChiTietHoaDonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiTietHoaDon
        fields = ["id", "hoa_don", "mon_an"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "cua_hang", "nguoi_dung"]


class DanhGiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGia
        fields = ["id", "diem_so", "cua_hang", "mon_an", "nguoi_dung"]

from builtins import print

from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import authentication
from oauthlib.uri_validate import query
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from email.mime.text import MIMEText
import smtplib
from django.views.decorators.csrf import csrf_exempt
import requests
import hashlib
import json
import time
from datetime import datetime

# vnpay
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from six import u

# from django.utils.http import urlquote

from .models import PaymentForm
from .vnpay import vnpay

from .models import TaiKhoan, MonAn, Menu, LoaiTaiKhoan, BinhLuan, LoaiThucAn, ChiTietMenu, HoaDon, ChiTietHoaDon, \
    Follow, DanhGia, ThongTinGiaoHang, ThoiDiem, ThoiGianBan, Payment_VNPay, ChiTietHoaDonVNPay
from .serializers import (TaiKhoanSerializer, MonAnSerializer,
                          MenuSerializer, LoaiTaiKhoanSerializer, ThemMonAnSerializer,
                          BinhLuanSerializer, TraLoiBinhLuanSerializer, LoaiThucAnSerializer,
                          ChiTietMenuSerializer, HoaDonSerializer, ChiTietHoaDonSerializer,
                          FollowSerializer, DanhGiaSerializer, ThongTinGiaoHangSerializer,
                          ThongTinTaiKhoanSerializer, ThoiDiemSerializer, ThoiGianBanSerializer,
                          ChiTietHoaDonVNPaySerializer,
                          Payment_VNPaySerializer)
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils import timezone
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def index(request):
    return render(request, "payment/index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        userId = request.POST.get('userId')
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            userId = form.cleaned_data['userId']
            request.session['userId'] = userId
            cartItemIds = form.cleaned_data.get('cartItemIds')
            request.session['cartItemIds'] = cartItemIds
            request.session.save()

            # print(cartItemIds)
            ipaddr = get_client_ip(request)

            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL

            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)

            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "payment/payment.html", {"title": "Thanh toán"})


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        vnp_userId = inputData['vnp_userId']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    userId = request.session.get('userId')
    cartItemIds = request.session.get('cartItemIds')
    print(cartItemIds)
    # print(userId)

    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                tai_khoan = TaiKhoan.objects.get(id=userId)

                payment = Payment_VNPay.objects.create(
                    order_id=order_id,
                    amount=amount,
                    vnp_TransactionNo=vnp_TransactionNo,
                    order_desc=order_desc,
                    vnp_ResponseCode=vnp_ResponseCode,
                    khach_hang=tai_khoan,
                    ngay_thanh_toan=timezone.now(),
                )
                cart_item_ids_list = [int(item) for item in cartItemIds.split(',')]
                mon_an_list = MonAn.objects.filter(id__in=cart_item_ids_list)

                menu_list = Menu.objects.filter(id__in=cart_item_ids_list)

                for mon_an in mon_an_list:
                    ChiTietHoaDonVNPay.objects.create(
                        hoa_don=payment,
                        mon_an=mon_an,
                    )

                for menu in menu_list:
                    ChiTietHoaDonVNPay.objects.create(
                        hoa_don=payment,
                        menu=menu,
                    )
                return render(request, "payment/payment_return.html", {"title": "Kết quả thanh toán",
                                                                       "result": "Thành công", "order_id": order_id,
                                                                       "amount": amount,
                                                                       "order_desc": order_desc,
                                                                       "vnp_TransactionNo": vnp_TransactionNo,
                                                                       "vnp_ResponseCode": vnp_ResponseCode,
                                                                       "userId": userId

                                                                       })
            else:
                return render(request, "payment/payment_return.html", {"title": "Kết quả thanh toán",
                                                                       "result": "Lỗi", "order_id": order_id,
                                                                       "amount": amount,
                                                                       "order_desc": order_desc,
                                                                       "vnp_TransactionNo": vnp_TransactionNo,
                                                                       "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "payment/payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "payment/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


n = random.randint(10 ** 11, 10 ** 12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


def query(request):
    if request.method == 'GET':
        return render(request, "payment/query.html", {"title": "Kiểm tra kết quả giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_Version = '2.1.0'

    vnp_RequestId = n_str
    vnp_Command = 'querydr'
    vnp_TxnRef = request.POST['order_id']
    vnp_OrderInfo = 'kiem tra gd'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode,
        vnp_TxnRef, vnp_TransactionDate, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "payment/query.html",
                  {"title": "Kiểm tra kết quả giao dịch", "response_json": response_json})


def refund(request):
    if request.method == 'GET':
        return render(request, "payment/refund.html", {"title": "Hoàn tiền giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_RequestId = n_str
    vnp_Version = '2.1.0'
    vnp_Command = 'refund'
    vnp_TransactionType = request.POST['TransactionType']
    vnp_TxnRef = request.POST['order_id']
    vnp_Amount = request.POST['amount']
    vnp_OrderInfo = request.POST['order_desc']
    vnp_TransactionNo = '0'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_CreateBy = 'user01'
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode, vnp_TransactionType, vnp_TxnRef,
        vnp_Amount, vnp_TransactionNo, vnp_TransactionDate, vnp_CreateBy, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_Amount": vnp_Amount,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_TransactionType": vnp_TransactionType,
        "vnp_TransactionNo": vnp_TransactionNo,
        "vnp_CreateBy": vnp_CreateBy,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "payment/refund.html",
                  {"title": "Kết quả hoàn tiền giao dịch", "response_json": response_json})


class ChiTietHoaDonVNPayViewSet(viewsets.ModelViewSet):
    queryset = ChiTietHoaDonVNPay.objects.all()
    serializer_class = ChiTietHoaDonVNPaySerializer


class Payment_VNPayViewSet(viewsets.ModelViewSet):
    queryset = Payment_VNPay.objects.all()
    serializer_class = Payment_VNPaySerializer


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

    @action(detail=False, methods=['post'])
    def send_email_to_nguoi_dung_cuahang(self, request):
        nguoi_dung_cuahang_id = request.data.get('nguoi_dung_cuahang_id')
        id_cua_hang = request.data.get('id_cua_hang')
        cua_hang = TaiKhoan.objects.get(id=id_cua_hang)
        nguoi_dung_cuahang = TaiKhoan.objects.get(id=nguoi_dung_cuahang_id)

        if hasattr(cua_hang, 'email') and cua_hang.email:
            sender_email = cua_hang.email
            recipient_email = nguoi_dung_cuahang.email
            print(sender_email)
            subject = f"{cua_hang.ten_nguoi_dung} có món ăn mới"
            message = 'Mời bạn vào app xem món ăn mới'

            # Thiết lập kết nối SMTP và gửi email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                msg = MIMEText(message)
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = recipient_email

                server.sendmail(sender_email, [recipient_email], msg.as_string())

            return Response({'message': 'Email đã được gửi thành công'})
        else:
            return Response({'error': 'Không thể sử dụng địa chỉ email của cua_hang'})


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

    @action(methods=['get'], detail=True, url_path='monanAll', url_name='monans')
    def list_MonAnALl_of_TaiKhoan(self, request, *args, **kwargs):
        tai_khoan_id = kwargs.get('pk')

        try:
            tai_khoan = TaiKhoan.objects.get(pk=tai_khoan_id)

            mon_an_queryset = MonAn.objects.filter(nguoi_dung=tai_khoan)

            serializer = MonAnSerializer(mon_an_queryset, many=True)
            return Response(serializer.data)
        except TaiKhoan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='monans', url_name='monans')
    def list_MonAn_of_TaiKhoan(self, request, *args, **kwargs):
        tai_khoan_id = kwargs.get('pk')

        try:
            tai_khoan = TaiKhoan.objects.get(pk=tai_khoan_id)

            # Lấy thời điểm hiện tại
            current_time = timezone.localtime(timezone.now())
            print(current_time)
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

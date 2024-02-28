from django.db.models import Count, F, Sum
from datetime import datetime, timezone

from .models import TaiKhoan, LoaiTaiKhoan, Payment_VNPay, ChiTietHoaDonVNPay, MonAn


def count_khachhang():
    count = TaiKhoan.objects.filter(loai_tai_khoan=1).count()
    return count


def count_cuahang():
    count = TaiKhoan.objects.filter(loai_tai_khoan=2).count()
    return count


def count_tong_tien_mua():
    query_result = Payment_VNPay.objects.values('khach_hang').annotate(tong_tien=Sum('amount'))

    tong_tien_dict = {item['khach_hang']: item['tong_tien'] for item in query_result}

    tai_khoan_list = TaiKhoan.objects.all()
    for tai_khoan in tai_khoan_list:
        tai_khoan.tong_tien_mua = tong_tien_dict.get(tai_khoan.pk, 0.0)

    return tai_khoan_list


def users_with_total_amount():
    users_with_amount = MonAn.objects.filter(
        chitiethoadonvnpay__isnull=False
    ).values(
        'nguoi_dung__id', 'nguoi_dung__ten_nguoi_dung'
    ).annotate(
        total_amount=Sum('chitiethoadonvnpay__hoa_don__amount')
    )

    return users_with_amount


# def get_year_from_order_desc(order_desc):
#     colon_index = order_desc.find(':')
#
#     time_part = order_desc[colon_index + 2:]
#
#     datetime_object = datetime.strptime(time_part, '%Y-%m-%d %H:%M:%S')
#     return datetime_object.year


def total_amount_by_year(year):
    payments_by_year = MonAn.objects.filter(
        chitiethoadonvnpay__isnull=False,
        chitiethoadonvnpay__hoa_don__ngay_thanh_toan__year=year
    ).values(
        'nguoi_dung__id', 'nguoi_dung__ten_nguoi_dung'
    ).annotate(
        total_amount=Sum('chitiethoadonvnpay__hoa_don__amount')
    )
    return payments_by_year


def total_amount_by_month(year, month):
    if not year.isdigit() or not month.isdigit():
        raise ValueError("Invalid year or month format")

    start_date = datetime(int(year), int(month), 1, 0, 0, 0, tzinfo=timezone.utc)
    end_date = start_date.replace(month=start_date.month + 1)

    payments_by_year_and_month = MonAn.objects.filter(
        chitiethoadonvnpay__isnull=False,
        chitiethoadonvnpay__hoa_don__ngay_thanh_toan__range=[start_date, end_date]
    ).values(
        'nguoi_dung__id', 'nguoi_dung__ten_nguoi_dung'
    ).annotate(
        total_amount=Sum('chitiethoadonvnpay__hoa_don__amount')
    )

    return payments_by_year_and_month

def total_amount_by_quarter(year, quarter):
    start_month = (int(quarter) - 1) * 3 + 1
    end_month = start_month + 3

    if end_month > 12:
        end_month = 12

    start_date = datetime(int(year), start_month, 1, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(int(year), end_month, 1, 0, 0, 0, tzinfo=timezone.utc)
    print(start_date)
    print(end_date)
    payments_by_year_and_quarter = MonAn.objects.filter(
        chitiethoadonvnpay__isnull=False,
        chitiethoadonvnpay__hoa_don__ngay_thanh_toan__range=[start_date, end_date]
    ).values(
        'nguoi_dung__id', 'nguoi_dung__ten_nguoi_dung'
    ).annotate(
        total_amount=Sum('chitiethoadonvnpay__hoa_don__amount')
    )

    return payments_by_year_and_quarter


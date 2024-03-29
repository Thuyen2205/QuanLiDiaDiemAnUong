# Generated by Django 5.0.1 on 2024-01-16 03:12

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='KiemDuyet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_loai_kiem_duyet', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LoaiDiaChi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_loai_dia_chi', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LoaiTaiKhoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_loai_tai_khoan', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LoaiThucAn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_loai_thuc_an', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ThoiDiem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_buoi', models.CharField(blank=True, max_length=50, null=True)),
                ('thoi_gian_bat_dau', models.DateTimeField()),
                ('thoi_gian_ket_thuc', models.DateTimeField()),
            ],
        ),
        # migrations.CreateModel(
        #     name='Voucher',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('ten_voucher', models.CharField(max_length=50)),
        #         ('ti_so', models.DecimalField(decimal_places=2, max_digits=5)),
        #     ],
        # ),
        migrations.CreateModel(
            name='TaiKhoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('ten_nguoi_dung', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('ngay_sinh', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('sdt', models.CharField(blank=True, max_length=50, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/%Y/%m/%d/')),
                ('kinh_do', models.FloatField(blank=True, default=0, null=True)),
                ('vi_do', models.FloatField(blank=True, default=0, null=True)),
                ('gioi_tinh', models.BooleanField(blank=True, default=False, null=True)),
                ('thoi_gian_mo_cua', models.DateTimeField(blank=True, null=True)),
                ('thoi_gian_dong_cua', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('kiem_duyet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mealmaster.kiemduyet')),
                ('loai_tai_khoan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mealmaster.loaitaikhoan')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cua_hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cua_hang_follow', to=settings.AUTH_USER_MODEL)),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nguoi_dung_follow', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HoaDon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChiTietHoaDon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoa_don', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealmaster.hoadon')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('tieu_de', models.CharField(blank=True, max_length=50, null=True)),
                ('trang_thai', models.BooleanField(default=False)),
                ('nguoi_dung', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChiTietMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong', models.IntegerField(default=0)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealmaster.menu')),
            ],
        ),
        migrations.CreateModel(
            name='MonAn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_mon_an', models.CharField(max_length=50)),
                ('gia_mon_an', models.IntegerField()),
                ('mo_ta', models.CharField(max_length=50)),
                ('trang_thai', models.BooleanField(default=False)),
                ('hinh_anh', models.ImageField(upload_to='monan/%y/%m/%d/')),
                ('so_luong', models.IntegerField()),
                ('loai_thuc_an', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealmaster.loaithucan')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='mon_an',
            field=models.ManyToManyField(related_name='menus', through='mealmaster.ChiTietMenu', to='mealmaster.monan'),
        ),
        migrations.AddField(
            model_name='hoadon',
            name='mon_an',
            field=models.ManyToManyField(related_name='hoadons', through='mealmaster.ChiTietHoaDon', to='mealmaster.monan'),
        ),
        migrations.CreateModel(
            name='DanhGia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diem_so', models.IntegerField()),
                ('cua_hang', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cua_hang_danh_gia', to=settings.AUTH_USER_MODEL)),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nguoi_dung_danh_gia', to=settings.AUTH_USER_MODEL)),
                ('mon_an', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mealmaster.monan')),
            ],
        ),
        migrations.AddField(
            model_name='chitietmenu',
            name='mon_an',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealmaster.monan'),
        ),
        migrations.AddField(
            model_name='chitiethoadon',
            name='mon_an',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealmaster.monan'),
        ),
        migrations.CreateModel(
            name='BinhLuan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noi_dung', models.CharField(max_length=50)),
                ('Img', models.ImageField(blank=True, null=True, upload_to='binhluanimg')),
                ('binh_luan_cha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mealmaster.binhluan')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                # ('mon_an_binh_luan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mealmaster.monan')),
            ],
        ),
        migrations.CreateModel(
            name='ThoiGianBan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mon_an', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealmaster.monan')),
                ('thoi_diem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealmaster.thoidiem')),
            ],
        ),
        migrations.AddField(
            model_name='thoidiem',
            name='mon_an',
            field=models.ManyToManyField(related_name='thoidiems', through='mealmaster.ThoiGianBan', to='mealmaster.monan'),
        ),
        migrations.CreateModel(
            name='ThongTinGiaoHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_chi', models.CharField(max_length=50)),
                ('ten_nguoi_nhan', models.CharField(max_length=50)),
                ('loai_dia_chi', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mealmaster.loaidiachi')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimKiem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_mon', models.CharField(max_length=50)),
                ('ten_loai_thuc_an', models.CharField(max_length=50)),
                ('ten_cua_hang', models.CharField(max_length=50)),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

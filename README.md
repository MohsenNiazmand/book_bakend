# Quran / Books Backend

یک بک‌اند Django REST Framework برای مدیریت کتاب‌ها و محتوای قرآن با پشتیبانی از **Multitenancy** (چند مستأجری).

## ویژگی‌ها

- ✅ **Multitenancy**: پشتیبانی کامل از چند مستأجری با ایزولاسیون کامل داده‌ها
- ✅ **JWT Authentication**: احراز هویت با JWT tokens
- ✅ **RESTful API**: API کامل برای مدیریت کتاب‌ها، فصل‌ها، آیات، قاری‌ها و فایل‌های صوتی
- ✅ **User Management**: مدیریت کاربران با پشتیبانی از یادداشت‌ها، بوکمارک‌ها و تاریخچه پخش
- ✅ **Admin Panel**: پنل ادمین Django برای مدیریت کامل
- ✅ **PostgreSQL**: استفاده از PostgreSQL به عنوان پایگاه داده
- ✅ **File Upload**: پشتیبانی از آپلود فایل‌های صوتی و تصاویر

## نیازمندی‌ها

- Python 3.12+
- PostgreSQL 12+
- Poetry (برای مدیریت dependencies)

## نصب و راه‌اندازی

### 1. کلون کردن ریپازیتوری

```bash
git clone https://github.com/MohsenNiazmand/book_bakend.git
cd book_backend
```

### 2. نصب Dependencies

```bash
# نصب Poetry (در صورت نیاز)
curl -sSL https://install.python-poetry.org | python3 -

# نصب dependencies
poetry install

# فعال‌سازی virtual environment
poetry shell
```

### 3. تنظیمات پایگاه داده

ایجاد دیتابیس PostgreSQL:

```bash
sudo -u postgres psql
CREATE DATABASE book_backend;
CREATE USER your_db_user WITH PASSWORD 'your_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE book_backend TO your_db_user;
\q
```

### 4. تنظیمات Environment Variables

ایجاد فایل `.env` در root پروژه:

```env
# Database
DB_NAME=book_backend
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: برای production
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

**تولید SECRET_KEY:**
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. اجرای Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. ساخت Superuser

```bash
python manage.py createsuperuser
```

### 7. اجرای سرور

```bash
python manage.py runserver
```

سرور در `http://localhost:8000` در دسترس خواهد بود.

## ساختار پروژه

```
book_backend/
├── accounts/          # احراز هویت (register, login, token)
├── audio/            # مدل‌ها و APIهای مربوط به صوت (Reciter, ChapterAudio, AudioTimestamp)
├── books/            # مدل‌ها و APIهای مربوط به کتاب (Book, Chapter, Verse)
├── core/             # مدل‌ها و middleware مربوط به Tenant
├── notes/             # یادداشت‌ها، بوکمارک‌ها و تاریخچه پخش
├── users/             # مدل User سفارشی
└── book_backend/      # تنظیمات اصلی Django
```

## استفاده از API

### شناسایی Tenant

تمام درخواست‌های API باید tenant را مشخص کنند از طریق یکی از روش‌های زیر:

1. **Header `X-Tenant-ID`**: شناسه عددی tenant
2. **Header `X-Tenant-Domain`**: دامنه tenant (مثلاً "default")
3. **Subdomain**: در صورت استفاده از subdomain (مثلاً tenant1.example.com)
4. **Query Parameter**: `?tenant=domain` (برای تست)

### مثال‌های استفاده

#### ایجاد Tenant

```bash
# از طریق management command
python manage.py create_tenant "Tenant Name" domain_name

# یا از طریق Admin Panel: /admin/core/tenant/
```

#### ثبت‌نام کاربر

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "X-Tenant-Domain: domain_name" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### دریافت Token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "X-Tenant-Domain: domain_name" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

#### دریافت لیست کتاب‌ها

```bash
curl -X GET http://localhost:8000/api/v1/books/ \
  -H "X-Tenant-Domain: domain_name" \
  -H "Authorization: Bearer <access_token>"
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - ثبت‌نام کاربر جدید
- `POST /api/auth/login/` - دریافت JWT token
- `POST /api/auth/refresh/` - رفرش token

### Books
- `GET /api/v1/books/` - لیست کتاب‌ها
- `POST /api/v1/books/` - ایجاد کتاب جدید
- `GET /api/v1/books/{id}/` - جزئیات کتاب
- `PATCH /api/v1/books/{id}/` - ویرایش کتاب
- `DELETE /api/v1/books/{id}/` - حذف کتاب

### Chapters
- `GET /api/v1/chapters/` - لیست فصل‌ها
- `POST /api/v1/chapters/` - ایجاد فصل جدید
- `GET /api/v1/chapters/{id}/` - جزئیات فصل
- `PATCH /api/v1/chapters/{id}/` - ویرایش فصل
- `DELETE /api/v1/chapters/{id}/` - حذف فصل

### Verses
- `GET /api/v1/verses/` - لیست آیات
- `POST /api/v1/verses/` - ایجاد آیه جدید
- `GET /api/v1/verses/{id}/` - جزئیات آیه
- `PATCH /api/v1/verses/{id}/` - ویرایش آیه
- `DELETE /api/v1/verses/{id}/` - حذف آیه

### Audio
- `GET /api/v1/audio/reciters/` - لیست قاری‌ها
- `POST /api/v1/audio/reciters/` - ایجاد قاری جدید
- `GET /api/v1/audio/chapter-audios/` - لیست صوت‌های فصل
- `POST /api/v1/audio/chapter-audios/` - آپلود صوت
- `GET /api/v1/audio/timestamps/` - لیست timestamps

### Notes & Bookmarks
- `GET /api/v1/notes/notes/` - لیست یادداشت‌ها
- `POST /api/v1/notes/notes/` - ایجاد یادداشت
- `GET /api/v1/notes/bookmarks/` - لیست بوکمارک‌ها
- `POST /api/v1/notes/bookmarks/` - ایجاد بوکمارک
- `GET /api/v1/notes/history/` - تاریخچه پخش

**نکته**: تمام endpointها نیاز به header `X-Tenant-ID` یا `X-Tenant-Domain` دارند.

## Admin Panel

دسترسی به پنل ادمین: `http://localhost:8000/admin/`

از پنل ادمین می‌توانید:
- مدیریت Tenantها
- مدیریت Users
- مدیریت Books, Chapters, Verses
- مدیریت Reciters و Audios
- مشاهده Notes, Bookmarks, PlayHistory

## تست‌ها

### اجرای تست‌ها

```bash
# اجرای تمام تست‌ها
python manage.py test

# اجرای تست‌های یک app خاص
python manage.py test books

# اجرای یک تست خاص
python manage.py test books.tests.TestBookModel
```

### با Coverage

```bash
# نصب coverage
pip install coverage

# اجرای تست‌ها با coverage
coverage run --source='.' manage.py test

# مشاهده گزارش
coverage report
coverage html  # برای گزارش HTML
```

## دیپلوی

### Environment Variables برای Production

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_NAME=book_backend_prod
DB_USER=your_prod_user
DB_PASSWORD=your_prod_password
DB_HOST=your-db-host
DB_PORT=5432
```

### مراحل دیپلوی

1. جمع‌آوری static files:
```bash
python manage.py collectstatic --noinput
```

2. اجرای migrations:
```bash
python manage.py migrate
```

3. راه‌اندازی با Gunicorn (مثال):
```bash
gunicorn book_backend.wsgi:application --bind 0.0.0.0:8000
```

## معماری Multitenancy

این پروژه از **Row-Level Multitenancy** استفاده می‌کند:
- یک دیتابیس واحد (PostgreSQL)
- یک schema واحد
- ایزولاسیون داده‌ها با ForeignKey به Tenant
- فیلتر خودکار در تمام queryها

هر tenant دارای:
- داده‌های جداگانه (Books, Users, Notes, etc.)
- کاربران جداگانه
- ایزولاسیون کامل از tenantهای دیگر

## مستندات

برای سناریوها و معیارهای پذیرش، به فایل [SCENARIOS.md](./SCENARIOS.md) مراجعه کنید.

## توسعه

### ساخت Migration جدید

```bash
python manage.py makemigrations
python manage.py migrate
```

### ساخت Management Command جدید

```bash
python manage.py create_tenant "Name" domain
```

## مجوز (License)

[مشخص کنید]

## نویسنده

Mohsen Niazmand - it.mohsen.niazmand@gmail.com

## پشتیبانی

برای گزارش باگ یا پیشنهاد ویژگی جدید، لطفاً issue ایجاد کنید.


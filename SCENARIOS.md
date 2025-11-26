# SCENARIOS — Quran / Books Backend

این سند مجموعهٔ سناریوها (Use Cases) و معیارهای پذیرش را برای پروژهٔ مدیریت کتاب‌ها و محتوای قرآن فراهم می‌کند. هدف آن ایجاد منبعی مرجع برای نوشتن تست‌ها و توسعهٔ رابط‌های API و رفتارهای کلاینتی است.

---

## 1. بازیگران (Actors)
- Tenant: سازمان/شرکت/نهاد که داده‌های خود را به صورت جداگانه نگهداری می‌کند. هر tenant دارای دامنه یا شناسه منحصر به فرد است.
- User: کاربر ثبت‌نام‌شده که به یک tenant تعلق دارد و می‌تواند یادداشت، بوکمارک و تاریخچه پخش ایجاد/مشاهده/حذف کند.
- Anonymous: بازدیدکننده بدون احراز هویت — دسترسی محدود به خواندن محتوای عمومی (نیاز به شناسایی tenant).
- Admin: کاربر مدیریتی که می‌تواند کتاب/فصل/آیه/قاری و فایل‌های صوتی را ایجاد، ویرایش و حذف کند (در محدوده tenant خود).
- System: پردازش‌های پس‌زمینه مانند Celery برای پردازش فایل‌ها یا همگام‌سازی با S3.

## 2. احراز هویت و مجوزها
- روش احراز هویت: JWT (djangorestframework-simplejwt).
- شناسایی Tenant: تمام درخواست‌ها باید tenant را مشخص کنند از طریق:
  - Header `X-Tenant-ID`: شناسه عددی tenant
  - Header `X-Tenant-Domain`: دامنه tenant (مثلاً "default")
  - Subdomain: در صورت استفاده از subdomain (مثلاً tenant1.example.com)
  - Query Parameter `?tenant=domain`: برای تست و توسعه
- قواعد کلی:
  - **همه درخواست‌ها نیاز به شناسایی tenant دارند** — در صورت عدم شناسایی tenant، پاسخ خالی برمی‌گردد.
  - خواندن عمومی (فهرست/جزییات) برای Books/Chapters/Verses/Reciters/Audios در محدوده tenant خود قابل دسترسی است.
  - عملیات نوشتن/حذف: نیاز به `IsAuthenticated` و برای عملیات مدیریتی باید نقش admin بررسی شود.
  - یادداشت/بوکمارک/تاریخچه پخش: نیاز به احراز هویت `IsAuthenticated` و فیلتر خودکار بر اساس tenant.
  - **ایزولاسیون داده‌ها**: هر tenant فقط به داده‌های خود دسترسی دارد.

## 3. نگاشت منابع مهم و مسیرهای API پیشنهادی
(مسیرها قابل تغییر بر اساس viewsets فعلی؛ این سند یک مرجع برای تست‌هاست.)

**نکته مهم**: تمام درخواست‌ها باید header `X-Tenant-ID` یا `X-Tenant-Domain` داشته باشند.

- Tenants (مدیریت از طریق Django Admin)
  - دسترسی به Admin: `/admin/` (نیاز به superuser)
  - ساخت superuser: `python manage.py createsuperuser`
  - ایجاد/ویرایش/حذف tenant از طریق `/admin/core/tenant/`
  - یا استفاده از management command: `python manage.py create_tenant "Name" domain`

- Books
  - GET `/api/books/` — فهرست کتاب‌های tenant جاری (فیلتر: `language`, `search`). **نیاز به tenant header**
  - POST `/api/books/` — ایجاد کتاب برای tenant جاری (admin). **نیاز به tenant header**
  - GET `/api/books/{id}/` — جزئیات کتاب شامل فصل‌ها (فقط اگر متعلق به tenant جاری باشد). **نیاز به tenant header**
  - PATCH/PUT/DELETE `/api/books/{id}/` — مدیریت (admin، فقط در محدوده tenant). **نیاز به tenant header**

- Chapters
  - GET `/api/chapters/` — فهرست فصل‌های tenant جاری (فیلتر از طریق book__tenant). **نیاز به tenant header**
  - POST `/api/chapters/` — ایجاد فصل (admin، book باید متعلق به tenant جاری باشد). **نیاز به tenant header**
  - GET `/api/chapters/{id}/` — جزئیات فصل (آیات، audios metadata، فقط اگر متعلق به tenant جاری باشد). **نیاز به tenant header**
  - PATCH/DELETE `/api/chapters/{id}/` — مدیریت (admin، فقط در محدوده tenant). **نیاز به tenant header**

- Verses
  - GET `/api/verses/` — لیست آیات tenant جاری (فیلتر از طریق book__tenant). **نیاز به tenant header**
  - POST `/api/verses/` — ایجاد آیه (admin، book و chapter باید متعلق به tenant جاری باشند). **نیاز به tenant header**
  - GET `/api/verses/{id}/` — جزئیات آیه (text, translation, page_number, audio links، فقط اگر متعلق به tenant جاری باشد). **نیاز به tenant header**
  - PATCH/DELETE `/api/verses/{id}/` — مدیریت (admin، فقط در محدوده tenant). **نیاز به tenant header**

- Reciters
  - GET `/api/audio/reciters/` — فهرست قاری‌های tenant جاری. **نیاز به tenant header**
  - POST `/api/audio/reciters/` — ایجاد قاری برای tenant جاری (admin). **نیاز به tenant header**
  - GET `/api/audio/reciters/{id}/` — جزئیات قاری (فقط اگر متعلق به tenant جاری باشد). **نیاز به tenant header**

- ChapterAudio
  - GET `/api/audio/chapter-audios/` — فهرست صوت‌های tenant جاری (فیلتر از طریق chapter__book__tenant). **نیاز به tenant header**
  - POST `/api/audio/chapter-audios/` — ثبت صوت برای tenant جاری (admin): body شامل `reciter_id`, `chapter_id`, `file` (multipart) یا `external_url`, `duration_seconds`. **نیاز به tenant header**
  - GET `/api/audio/chapter-audios/{id}/` — جزئیات صوت شامل timestamps (فقط اگر متعلق به tenant جاری باشد). **نیاز به tenant header**
  - PATCH/DELETE `/api/audio/chapter-audios/{id}/` — مدیریت (admin، فقط در محدوده tenant). **نیاز به tenant header**

- AudioTimestamp
  - GET `/api/audio/timestamps/` — فهرست timestamps tenant جاری (فیلتر از طریق chapter_audio__chapter__book__tenant). **نیاز به tenant header**
  - POST `/api/audio/timestamps/` — ایجاد timestamp برای tenant جاری: `chapter_audio_id`, `verse_id`, `start_time`, `end_time` (اختیاری). **نیاز به tenant header**

- Auth / Users
  - POST `/api/auth/register/` — ثبت‌نام. **نیاز به tenant header** — کاربر به tenant جاری اختصاص داده می‌شود.
  - POST `/api/auth/login/` — دریافت access/refresh token. **نیاز به tenant header** (اختیاری برای لاگین، اما برای دسترسی به داده‌ها لازم است).
  - POST `/api/auth/refresh/` — رفرش توکن.
  - GET `/api/users/me/` — پروفایل کاربر جاری (auth required). **نیاز به tenant header**
  - PATCH `/api/users/me/` — ویرایش پروفایل (avatar upload). **نیاز به tenant header**

- Notes / Bookmarks / PlayHistory
  - GET `/api/notes/` — فهرست یادداشت‌های کاربر جاری در tenant جاری (auth required). **نیاز به tenant header**
  - POST `/api/notes/` — ایجاد یادداشت برای tenant جاری (auth required). **نیاز به tenant header**
  - GET/PATCH/DELETE `/api/notes/{id}/` — مدیریت یادداشت (owner یا admin، فقط در محدوده tenant). **نیاز به tenant header**
  - GET `/api/bookmarks/` — فهرست بوکمارک‌های کاربر در tenant جاری (auth required). **نیاز به tenant header**
  - POST `/api/bookmarks/` — ایجاد بوکمارک برای tenant جاری (auth required). **نیاز به tenant header**
  - DELETE `/api/bookmarks/{id}/` — حذف (owner یا admin، فقط در محدوده tenant). **نیاز به tenant header**
  - GET `/api/notes/history/` — فهرست تاریخچه پخش کاربر در tenant جاری (auth required). **نیاز به tenant header**
  - POST `/api/notes/history/` — ایجاد/بروزرسانی رکورد پخش برای tenant جاری (auth required). **نیاز به tenant header**

## 4. جریان‌های اصلی (Flows) و معیارهای پذیرش

### 4.0. راه‌اندازی Tenant (پیش‌نیاز)
- پیش‌شرط: دسترسی به Django Admin یا shell.
- گام‌ها:
  1. ساخت superuser (در صورت نیاز): `python manage.py createsuperuser`
  2. ورود به Admin Panel: `/admin/` با credentials superuser
  3. ایجاد tenant از طریق Admin (`/admin/core/tenant/`) یا command: `python manage.py create_tenant "Tenant Name" domain_name`
  4. دریافت Tenant ID یا Domain برای استفاده در headerها.
- معیار پذیرش:
  - Tenant با domain منحصر به فرد ایجاد شود.
  - Tenant در Admin قابل مشاهده و مدیریت باشد.
  - در Admin Panel می‌توان Users را با انتخاب Tenant ایجاد کرد.

### 4.1. ایجاد کتاب و محتوا (Admin)
- پیش‌شرط: کاربر admin است و tenant شناسایی شده است.
- گام‌ها:
  1. ارسال درخواست با header `X-Tenant-Domain: domain_name` یا `X-Tenant-ID: tenant_id`
  2. POST `/api/books/` با `title`, `description`, `language` — کتاب به tenant جاری اختصاص داده می‌شود.
  3. برای هر فصل: POST `/api/chapters/` با `book_id`, `title`, `number`, optional `juz` — book باید متعلق به tenant جاری باشد.
  4. برای هر آیه: POST `/api/verses/` با `book_id`, `chapter_id`, `number`, `text`, optional `translation`, optional `page_number` — book و chapter باید متعلق به tenant جاری باشند.
- معیار پذیرش:
  - Status 201 برای هر ایجاد، موجودیت در DB ساخته شود و `tenant` field به درستی تنظیم شود.
  - GET `/api/books/{id}/` با همان tenant header، فصل‌ها را نمایش دهد.
  - ایجاد آیه با شماره‌ی تکراری در فصل منجر به 400 با پیام مناسب شود.
  - **ایزولاسیون**: درخواست با tenant دیگر نباید کتاب‌های این tenant را ببیند.

### 4.2. افزودن صوت فصل و تعیین تایم‌استمپ‌ها
- پیش‌شرط: admin/uploader و tenant شناسایی شده است.
- گام‌ها:
  1. ارسال درخواست با header `X-Tenant-Domain` یا `X-Tenant-ID`
  2. POST `/api/audio/reciters/` برای ایجاد قاری در tenant جاری (در صورت نیاز).
  3. POST `/api/audio/chapter-audios/` با `reciter_id`, `chapter_id`, `file` یا `external_url`, `duration_seconds` — chapter و reciter باید متعلق به tenant جاری باشند.
  4. برای هر آیه: POST `/api/audio/timestamps/` با `chapter_audio_id`, `verse_id`, `start_time`, `end_time` — همه باید متعلق به tenant جاری باشند.
- معیار پذیرش:
  - audio ساخته شده و GET `/api/audio/chapter-audios/{id}/` با همان tenant header، timestamps را نشان دهد.
  - اگر timestamp تکراری برای یک verse و همان audio ارسال شود، رفتار مشخص (update یا error) رخ دهد.
  - **ایزولاسیون**: audioهای tenant دیگر قابل مشاهده نیستند.

### 4.3. پخش صوت و ذخیره موقعیت پخش
- پیش‌شرط: کاربر auth شده و tenant شناسایی شده است.
- گام‌ها:
  1. ارسال درخواست با header `X-Tenant-Domain` یا `X-Tenant-ID` و JWT token.
  2. کلاینت فایل صوتی را برای playback از `ChapterAudio.file` یا streaming endpoint بگیرد (فقط audioهای tenant جاری).
  3. در زمان توقف/ذخیره، POST `/api/notes/history/` با `chapter_audio_id`, `last_position` انجام شود.
- معیار پذیرش:
  - یک رکورد PlayHistory برای (user, chapter_audio) در tenant جاری ایجاد یا بروزرسانی شود.
  - پاسخ 200 و body شامل رکورد جدید/بروزشده باشد.
  - **ایزولاسیون**: تاریخچه پخش فقط برای audioهای tenant جاری قابل ذخیره است.

### 4.4. افزودن بوکمارک یا یادداشت
- پیش‌شرط: کاربر auth شده و tenant شناسایی شده است.
- گام‌ها:
  1. ارسال درخواست با header `X-Tenant-Domain` یا `X-Tenant-ID` و JWT token.
  2. POST `/api/bookmarks/` یا `/api/notes/` با اطلاعات مربوطه — book/chapter/verse باید متعلق به tenant جاری باشند.
- معیار پذیرش:
  - رکورد ساخته شود و GET مربوطه آن را بازگرداند (فقط در محدوده tenant جاری).
  - در صورت تداخل با unique constraint، پیام خطا و وضعیت مناسب (400 یا 409) بازگردد.
  - **ایزولاسیون**: بوکمارک‌ها و یادداشت‌ها فقط برای محتوای tenant جاری قابل ایجاد هستند.

### 4.5. ثبت‌نام و مدیریت پروفایل
- پیش‌شرط: public (اما نیاز به شناسایی tenant برای ثبت‌نام).
- گام‌ها:
  1. ارسال درخواست با header `X-Tenant-Domain` یا `X-Tenant-ID`.
  2. POST `/api/auth/register/` با `username`, `email`, `password` — کاربر به tenant جاری اختصاص داده می‌شود.
  3. POST `/api/auth/login/` با `username` و `password` برای دریافت access token — باید با tenant header باشد.
  4. GET/PATCH `/api/users/me/` با tenant header و JWT token برای مشاهده و به‌روزرسانی profile و avatar.
- معیار پذیرش:
  - رمز به‌صورت hashed ذخیره شود.
  - کاربر به tenant مشخص شده در header اختصاص داده شود.
  - avatar در `MEDIA_ROOT` ذخیره و URL در response برگردانده شود.
  - **ایزولاسیون**: کاربر فقط می‌تواند در tenant خود ثبت‌نام کند و به داده‌های tenant خود دسترسی دارد.

## 5. قواعد اعتبارسنجی (Validation) و خطاها
- **Tenant Validation**:
  - در صورت عدم شناسایی tenant در درخواست => پاسخ خالی (empty queryset).
  - در صورت ارجاع به resource متعلق به tenant دیگر => 404 Not Found.
  - در صورت ایجاد resource با tenant نامعتبر => 400 Bad Request.
- `Book`/`Reciter`:
  - `unique_together ('tenant', 'title')` و `('tenant', 'name')` باید بررسی شود.
- `Verse`:
  - `unique_together ('chapter', 'number')` حتماً بررسی شود؛ در صورت تکرار => 400.
  - book و chapter باید متعلق به tenant جاری باشند.
- `ChapterAudio`:
  - حداقل یکی از `file` یا `external_url` باید وجود داشته باشد => در غیر اینصورت 400.
  - chapter و reciter باید متعلق به tenant جاری باشند.
- `AudioTimestamp`:
  - `start_time` باید >= 0.
  - اگر `end_time` داده شود، باید > `start_time`.
  - chapter_audio و verse باید متعلق به tenant جاری باشند.
- `UserNote`/`Bookmark`:
  - هنگام ایجاد برای یک `verse` که قبلاً برای همان کاربر وجود دارد، یا 400/409 یا رفتار update تعیین شود.
  - book/chapter/verse باید متعلق به tenant جاری باشند.
- Auth errors:
  - عملیات نوشتنی بدون توکن => 401 Unauthorized.
- Not found:
  - اشاره به مدل ناموجود => 404.
  - اشاره به resource متعلق به tenant دیگر => 404.

## 6. موارد لبه (Edge Cases)
- **Tenant Isolation**:
  - درخواست بدون tenant header => پاسخ خالی (نه خطا).
  - تلاش برای دسترسی به resource tenant دیگر => 404.
  - ایجاد resource با reference به resource tenant دیگر => 400.
- همزمانی (Concurrency): دو درخواست همزمان برای ایجاد یک `Verse` با همان `(chapter, number)` در همان tenant => یکی موفق، دیگری 400.
- حذف cascade: حذف `Book` باید فصل‌ها/آیات وابسته را پاک کند و در صورت استفاده از فایل‌های صوتی محلی، فایل‌ها نیز پاک یا از storage حذف شوند (فقط در محدوده tenant).
- حذف Tenant: حذف tenant باید تمام داده‌های وابسته را cascade delete کند (books, reciters, users, notes, etc.).
- تایم‌استمپ نامناسب: اضافه کردن timestamp برای verse که به chapter دیگری تعلق دارد یا متعلق به tenant دیگر است => 400.
- فایل‌های بزرگ: آپلود صوت با حجم بزرگ باید محدود و در validation بررسی شود.
- Avatar با MIME نامعتبر => 400.
- تغییر tenant کاربر: کاربر نمی‌تواند tenant خود را تغییر دهد (فقط admin).

## 7. صفحه‌بندی، مرتب‌سازی و فیلترها
- تمام لیست‌ها باید قابل صفحه‌بندی باشند (`page`, `page_size`).
- فیلترهای معمول: `language`, `search` روی `title/text`, `page_number`, `juz`, `reciter_id`.

## 8. رسانه و ذخیره‌سازی (Media & Storage)
- در development: `MEDIA_ROOT` لوکال و Django static serve.
- در production: پیشنهاد `django-storages[boto3]` و S3 به عنوان `DEFAULT_FILE_STORAGE`.
- Cleanup: در حذف رکوردهای صوتی باید فایل‌های مربوطه نیز حذف شوند یا lifecycle مدیریت شود.

## 9. چک‌لیست برای نوشتن تست‌ها (برای مرحلهٔ بعد)
- آماده‌سازی factories/fixtures برای: `Tenant`, `User`, `Book`, `Chapter`, `Verse`, `Reciter`, `ChapterAudio`, `AudioTimestamp`.
- گروه‌بندی تست‌ها:
  - **Tenant Management**: ایجاد، ویرایش، حذف tenant، شناسایی tenant از header/subdomain/query.
  - **Tenant Isolation**: تست ایزولاسیون داده‌ها بین tenantهای مختلف.
  - Auth: ثبت‌نام با tenant، لاگین، توکن ریفرش.
  - Books/Chapters/Verses CRUD: positive/negative cases (unique constraint، tenant validation).
  - Audio upload: multipart file و external_url validation، tenant validation.
  - Timestamps: validation rules (`start_time`, `end_time`, verse/chapter consistency، tenant consistency).
  - Notes/Bookmarks/PlayHistory: auth enforcement، tenant filtering، unique constraints، CRUD.
  - Edge cases: concurrency، cascade deletes، file cleanup، tenant isolation edge cases.
- استفاده از Django test client یا pytest-django، و استفاده از `SimpleUploadedFile` برای تست آپلودها.
- **تست‌های Tenant**: تست با headerهای مختلف (`X-Tenant-ID`, `X-Tenant-Domain`)، تست بدون tenant، تست با tenant نامعتبر.

## 10. نگاشت مدل‌ها برای کمک به تست‌نویسی
- `Tenant` -> `core.models.Tenant`
- `Book` -> `books.models.Book` (دارای field `tenant`)
- `Chapter` -> `books.models.Chapter` (tenant از طریق `book.tenant`)
- `Verse` -> `books.models.Verse` (tenant از طریق `book.tenant`)
- `Reciter` -> `audio.models.Reciter` (دارای field `tenant`)
- `ChapterAudio` -> `audio.models.ChapterAudio` (tenant از طریق `chapter.book.tenant`)
- `AudioTimestamp` -> `audio.models.AudioTimestamp` (tenant از طریق `chapter_audio.chapter.book.tenant`)
- `User` -> `users.models.User` (دارای field `tenant`)
- `UserNote` -> `notes.models.UserNote` (tenant از طریق `book.tenant`)
- `Bookmark` -> `notes.models.Bookmark` (tenant از طریق `book.tenant`)
- `PlayHistory` -> `notes.models.PlayHistory` (tenant از طریق `chapter_audio.chapter.book.tenant`)

## 11. پایگاه داده (Database)
- **PostgreSQL**: پروژه از PostgreSQL به عنوان پایگاه داده استفاده می‌کند.
- تنظیمات از طریق متغیرهای محیطی در `.env`:
  - `DB_NAME`: نام دیتابیس
  - `DB_USER`: نام کاربری
  - `DB_PASSWORD`: رمز عبور
  - `DB_HOST`: آدرس host (پیش‌فرض: localhost)
  - `DB_PORT`: پورت (پیش‌فرض: 5432)

## 12. سناریوهای پنل ادمین (Admin Panel Scenarios)

### 12.1. دسترسی به پنل ادمین
- پیش‌شرط: superuser ساخته شده (`python manage.py createsuperuser`)
- گام‌ها:
  1. رفتن به `/admin/`
  2. وارد کردن username و password
  3. کلیک روی "Log in"
- معیار پذیرش:
  - با credentials صحیح وارد شود و داشبورد ادمین نمایش داده شود
  - با credentials نادرست پیام خطا نمایش داده شود
  - بعد از لاگین، منوی ادمین با تمام بخش‌ها قابل مشاهده باشد

### 12.2. مدیریت Tenantها
- پیش‌شرط: ورود به پنل ادمین
- گام‌ها:
  1. رفتن به بخش "Tenants" (`/admin/core/tenant/`)
  2. مشاهده لیست tenantها با فیلدهای: name, domain, is_active, created_at
  3. افزودن tenant جدید: کلیک "Add Tenant" → پر کردن Name, Domain, Is active → Save
  4. ویرایش tenant موجود: کلیک روی tenant → تغییر فیلدها → Save
  5. حذف tenant: انتخاب tenant → Delete → تایید
  6. جستجو: استفاده از search box برای name یا domain
  7. فیلتر: استفاده از فیلتر is_active
- معیار پذیرش:
  - لیست tenantها با تمام فیلدها نمایش داده شود
  - افزودن tenant با domain منحصر به فرد موفق باشد
  - افزودن tenant با domain تکراری => خطای validation
  - ویرایش tenant موفق باشد
  - حذف tenant => cascade delete تمام داده‌های وابسته (books, users, etc.)
  - جستجو و فیلتر به درستی کار کند

### 12.3. مدیریت Users
- پیش‌شرط: ورود به پنل ادمین، وجود حداقل یک tenant
- گام‌ها:
  1. رفتن به بخش "Users" (`/admin/users/user/`)
  2. مشاهده لیست کاربران با فیلدهای: username, email, tenant, is_staff, is_active
  3. افزودن کاربر جدید: کلیک "Add User" → پر کردن Username, Password, Email → انتخاب Tenant در بخش "Tenant Information" → Save
  4. ویرایش کاربر: کلیک روی کاربر → تغییر فیلدها (مثلاً تغییر tenant، فعال/غیرفعال کردن) → Save
  5. حذف کاربر: انتخاب کاربر → Delete → تایید
  6. فیلتر: استفاده از فیلتر tenant, is_staff, is_active, is_superuser
  7. جستجو: استفاده از search box برای username یا email
- معیار پذیرش:
  - لیست کاربران با tenant نمایش داده شود
  - افزودن کاربر با انتخاب tenant موفق باشد
  - افزودن کاربر بدون tenant => کاربر با tenant=null ساخته شود (اختیاری)
  - ویرایش tenant کاربر موفق باشد
  - username یکسان در tenantهای مختلف قابل ساخت باشد
  - username یکسان در یک tenant => خطای unique constraint
  - فیلتر بر اساس tenant به درستی کار کند
  - جستجو به درستی کار کند

### 12.4. مدیریت Books
- پیش‌شرط: ورود به پنل ادمین، وجود حداقل یک tenant
- گام‌ها:
  1. رفتن به بخش "Books" (`/admin/books/book/`)
  2. مشاهده لیست کتاب‌ها با فیلدهای: title, tenant, language, created_at
  3. افزودن کتاب جدید: کلیک "Add Book" → پر کردن Title, Description, Language → انتخاب Tenant → Save
  4. ویرایش کتاب: کلیک روی کتاب → تغییر فیلدها → Save
  5. حذف کتاب: انتخاب کتاب → Delete → تایید (cascade delete برای chapters/verses)
  6. فیلتر: استفاده از فیلتر tenant, language, created_at
  7. جستجو: استفاده از search box برای title یا description
- معیار پذیرش:
  - لیست کتاب‌ها با tenant نمایش داده شود
  - افزودن کتاب با انتخاب tenant موفق باشد
  - title یکسان در tenantهای مختلف قابل ساخت باشد
  - title یکسان در یک tenant => خطای unique constraint
  - حذف کتاب => cascade delete chapters و verses مرتبط
  - فیلتر بر اساس tenant به درستی کار کند

### 12.5. مدیریت Chapters و Verses
- پیش‌شرط: ورود به پنل ادمین، وجود حداقل یک book
- گام‌ها:
  1. رفتن به بخش "Chapters" (`/admin/books/chapter/`)
  2. افزودن Chapter: کلیک "Add Chapter" → انتخاب Book → پر کردن Title, Number, Juz → Save
  3. رفتن به بخش "Verses" (`/admin/books/verse/`)
  4. افزودن Verse: کلیک "Add Verse" → انتخاب Book و Chapter → پر کردن Number, Text, Translation, Page number → Save
  5. ویرایش و حذف chapters/verses
  6. فیلتر: استفاده از فیلتر tenant (از طریق book__tenant)
- معیار پذیرش:
  - book انتخاب شده باید متعلق به tenant باشد
  - unique constraint برای (chapter, number) رعایت شود
  - فیلتر بر اساس tenant (از طریق book) به درستی کار کند
  - حذف chapter => cascade delete verses مرتبط

### 12.6. مدیریت Reciters و Audios
- پیش‌شرط: ورود به پنل ادمین، وجود حداقل یک tenant
- گام‌ها:
  1. رفتن به بخش "Reciters" (`/admin/audio/reciter/`)
  2. افزودن Reciter: کلیک "Add Reciter" → انتخاب Tenant → پر کردن Name, Language, Bio → Save
  3. رفتن به بخش "Chapter Audios" (`/admin/audio/chapteraudio/`)
  4. افزودن ChapterAudio: کلیک "Add Chapter Audio" → انتخاب Chapter و Reciter → آپلود File یا وارد کردن External URL → پر کردن Duration → Save
  5. رفتن به بخش "Audio Timestamps" (`/admin/audio/audiotimestamp/`)
  6. افزودن AudioTimestamp: کلیک "Add Audio Timestamp" → انتخاب Chapter Audio و Verse → پر کردن Start time, End time → Save
  7. فیلتر: استفاده از فیلتر tenant
- معیار پذیرش:
  - همه موارد با tenant مرتبط باشند
  - فیلتر بر اساس tenant به درستی کار کند
  - validation: حداقل یکی از file یا external_url باید وجود داشته باشد
  - start_time >= 0 و end_time > start_time

### 12.7. مدیریت Notes, Bookmarks, PlayHistory
- پیش‌شرط: ورود به پنل ادمین
- گام‌ها:
  1. رفتن به بخش "User Notes" (`/admin/notes/usernote/`)
  2. مشاهده لیست Notes با فیلتر tenant (از طریق book__tenant)
  3. مشاهده جزئیات Note
  4. حذف Note (در صورت نیاز)
  5. همین کار برای Bookmarks و PlayHistory
- معیار پذیرش:
  - لیست با فیلتر tenant نمایش داده شود
  - جزئیات قابل مشاهده باشد
  - حذف موفق باشد

## 13. سناریوهای دیپلوی (Deployment Scenarios)

### 13.1. تنظیمات CI/CD
- پیش‌شرط: ریپو Git آماده (GitHub/GitLab/Bitbucket)
- گام‌ها:
  1. ساخت workflow file (مثلاً `.github/workflows/deploy.yml` برای GitHub Actions)
  2. تنظیمات environment variables در CI/CD platform:
     - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
     - `SECRET_KEY`
     - `DEBUG=False` (برای production)
     - `ALLOWED_HOSTS`
  3. تنظیمات تست خودکار قبل از دیپلوی:
     - اجرای `python manage.py test` یا `pytest`
     - بررسی coverage
  4. تنظیمات دیپلوی به محیط تست:
     - اجرای migrations: `python manage.py migrate`
     - جمع‌آوری static files: `python manage.py collectstatic --noinput`
     - راه‌اندازی سرور
- معیار پذیرش:
  - با هر push به branch اصلی (مثلاً `main`)، workflow اجرا شود
  - تست‌ها به صورت خودکار اجرا شوند
  - در صورت موفقیت تست‌ها، دیپلوی انجام شود
  - در صورت خطا در تست‌ها، دیپلوی انجام نشود
  - لاگ‌های دیپلوی قابل مشاهده باشد
  - notification در صورت موفقیت/خطا ارسال شود

### 13.2. دیپلوی روزانه
- پیش‌شرط: CI/CD تنظیم شده
- گام‌ها:
  1. توسعه‌دهنده تغییرات کد را انجام می‌دهد
  2. Commit تغییرات: `git add .` → `git commit -m "message"` → `git push origin main`
  3. CI/CD به صورت خودکار:
     - Pull latest code
     - اجرای تست‌ها
     - در صورت موفقیت: اجرای migrations → collectstatic → restart server
  4. بررسی محیط تست:
     - بررسی دسترسی به API endpoints
     - بررسی عملکرد اپلیکیشن
     - بررسی لاگ‌ها
- معیار پذیرش:
  - دیپلوی بدون خطا انجام شود
  - اپلیکیشن در محیط تست در دسترس باشد
  - داده‌های تست حفظ شوند (migrations به درستی اجرا شوند)
  - static files به درستی serve شوند
  - API endpoints به درستی کار کنند
  - زمان downtime حداقل باشد

### 13.3. Rollback در صورت خطا
- پیش‌شرط: دیپلوی انجام شده
- گام‌ها:
  1. شناسایی خطا در محیط تست:
     - بررسی لاگ‌های سرور
     - بررسی خطاهای API
     - بررسی خطاهای database
  2. Rollback به نسخه قبلی:
     - استفاده از Git: `git revert` یا `git reset`
     - یا استفاده از feature CI/CD برای rollback خودکار
  3. بررسی عملکرد نسخه قبلی:
     - تست API endpoints
     - بررسی database integrity
- معیار پذیرش:
  - Rollback سریع انجام شود (زمان downtime کم)
  - نسخه قبلی به درستی کار کند
  - داده‌ها حفظ شوند
  - لاگ‌های rollback ثبت شوند

### 13.4. دیپلوی به Production
- پیش‌شرط: تست موفق در محیط تست
- گام‌ها:
  1. Tag کردن نسخه: `git tag -a v1.0.0 -m "Release version"`
  2. Push tag: `git push origin v1.0.0`
  3. دیپلوی به production (manual یا automatic):
     - Backup database
     - اجرای migrations
     - collectstatic
     - restart server
  4. بررسی production:
     - بررسی health check endpoint
     - بررسی API endpoints
     - بررسی performance
- معیار پذیرش:
  - Backup قبل از دیپلوی انجام شود
  - Migrations به درستی اجرا شوند
  - اپلیکیشن در production در دسترس باشد
  - Performance قابل قبول باشد
  - Monitoring و alerting فعال باشد

## 14. سناریوهای تست (Testing Scenarios)

### 14.1. تست‌های واحد (Unit Tests)
- **مدل‌ها (Models)**:
  - ایجاد instance با فیلدهای معتبر
  - Validation errors برای فیلدهای نامعتبر
  - Relationships (ForeignKey, ManyToMany)
  - Unique constraints
  - Methods و properties
- **Serializerها**:
  - Serialization (model → dict)
  - Deserialization (dict → model)
  - Validation
  - Custom fields
- **Viewها**:
  - Queryset filtering بر اساس tenant
  - Permissions (IsAuthenticated, IsAdminUser)
  - perform_create برای تنظیم tenant
- **Middleware**:
  - شناسایی tenant از header X-Tenant-ID
  - شناسایی tenant از header X-Tenant-Domain
  - شناسایی tenant از subdomain
  - شناسایی tenant از query parameter
  - رفتار در صورت عدم شناسایی tenant

### 14.2. تست‌های یکپارچه (Integration Tests)
- **API Endpoints**:
  - GET requests با tenant header → فیلتر صحیح
  - POST requests با tenant header → ایجاد با tenant صحیح
  - GET requests بدون tenant header → پاسخ خالی
  - دسترسی به resource tenant دیگر → 404
- **Tenant Isolation**:
  - کاربر tenant1 فقط داده‌های tenant1 را می‌بیند
  - کاربر tenant2 فقط داده‌های tenant2 را می‌بیند
  - ایجاد resource با reference به resource tenant دیگر → 400
- **Authentication**:
  - Register با tenant header → کاربر به tenant اختصاص داده شود
  - Login با tenant header → token دریافت شود
  - Access protected resource با token → موفق باشد
  - Access protected resource بدون token → 401

### 14.3. تست‌های End-to-End (E2E)
- **جریان کامل ایجاد محتوا**:
  1. ساخت tenant
  2. ساخت user در آن tenant
  3. Login و دریافت token
  4. ساخت book با tenant header
  5. ساخت chapter برای book
  6. ساخت verse برای chapter
  7. بررسی ایزولاسیون: user tenant دیگر نباید این داده‌ها را ببیند
- **جریان کامل Authentication**:
  1. Register با tenant header
  2. Login با tenant header
  3. Access protected resource با token
  4. Refresh token
  5. Logout (در صورت پیاده‌سازی)

---

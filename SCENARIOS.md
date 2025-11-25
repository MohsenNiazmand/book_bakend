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
  1. ایجاد tenant از طریق Admin (`/admin/core/tenant/`) یا command: `python manage.py create_tenant "Tenant Name" domain_name`
  2. دریافت Tenant ID یا Domain برای استفاده در headerها.
- معیار پذیرش:
  - Tenant با domain منحصر به فرد ایجاد شود.
  - Tenant در Admin قابل مشاهده و مدیریت باشد.

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

---

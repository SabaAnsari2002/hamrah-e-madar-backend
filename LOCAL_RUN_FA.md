# اجرای لوکال بک‌اند همراه‌مادر

این پروژه برای توسعه‌ی محلی از SQLite استفاده می‌کند و به Docker نیاز ندارد.

## پیش‌نیاز
- Python 3.12 یا 3.13 پیشنهادی
- اینترنت فقط برای نصب اولیه‌ی پکیج‌های `requirements.txt`

## Windows / PowerShell — روش سریع
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\run_local.ps1
```

## macOS / Linux — روش سریع
```bash
chmod +x scripts/run_local.sh
./scripts/run_local.sh
```

## روش دستی — Windows
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:DEBUG="true"
$env:SECRET_KEY="local-dev-secret-change-me"
$env:ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0,10.0.2.2"
python manage.py migrate
python manage.py seed_demo
python manage.py check
python manage.py test
python manage.py runserver 0.0.0.0:8000
```

## روش دستی — macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export DEBUG=true
export SECRET_KEY='local-dev-secret-change-me'
export ALLOWED_HOSTS='localhost,127.0.0.1,0.0.0.0,10.0.2.2'
python manage.py migrate
python manage.py seed_demo
python manage.py check
python manage.py test
python manage.py runserver 0.0.0.0:8000
```

## آدرس‌ها
- Swagger: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`
- Admin: `http://127.0.0.1:8000/admin/`
- API base: `http://127.0.0.1:8000/api/v1/`

## ورود دمو
- Phone: `09120000000`
- OTP در حالت `DEBUG=true`: `123456`

ابتدا:
```http
POST /api/v1/auth/otp/request/
Content-Type: application/json

{"phone_number":"09120000000"}
```
سپس:
```http
POST /api/v1/auth/otp/verify/
Content-Type: application/json

{"phone_number":"09120000000","code":"123456"}
```
توکن `access` خروجی را به شکل `Authorization: Bearer <ACCESS_TOKEN>` برای endpointهای محافظت‌شده ارسال کنید.

## Android Emulator
اگر Android Emulator و Django روی یک کامپیوتر اجرا می‌شوند، داخل اپ از این base URL استفاده کنید:
`http://10.0.2.2:8000/api/v1/`

`127.0.0.1` داخل Emulator به خود Emulator اشاره می‌کند، نه کامپیوتر میزبان.

## گوشی فیزیکی
کامپیوتر و گوشی باید در یک شبکه باشند. IP LAN کامپیوتر را پیدا کنید (مثلاً `192.168.1.20`) و اجرا کنید:
```bash
# macOS/Linux example
export ALLOWED_HOSTS='localhost,127.0.0.1,0.0.0.0,192.168.1.20'
python manage.py runserver 0.0.0.0:8000
```
در Android از `http://192.168.1.20:8000/api/v1/` استفاده کنید. Firewall باید TCP/8000 را فقط روی شبکه‌ی مورد اعتماد اجازه دهد.

## Reset دیتای محلی
برای شروع تمیز:
```bash
# سرور را متوقف کنید
# سپس db.sqlite3 را حذف کنید
python manage.py migrate
python manage.py seed_demo
```

## ماهیت داده‌ها
رکوردهای وزن، فشارخون، قندخون، علائم، ویزیت، آزمایش، سونوگرافی، دارو و reminder همگی **synthetic demo data** هستند و متعلق به بیمار واقعی نیستند. محتوای پزشکی seed اصلی نیز demo است و به‌عنوان توصیه یا تشخیص پزشکی نباید استفاده شود.

## محتوای مرجع
علاوه بر داده‌های synthetic، سه مقاله‌ی کوتاه source-backed با لینک مستقیم به WHO/NHS seed می‌شوند. این‌ها محتوای آموزشی عمومی هستند، نه داده‌ی بیمار واقعی و نه توصیه‌ی شخصی پزشکی.

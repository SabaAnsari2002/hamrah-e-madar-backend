# راه‌اندازی اشتراک کافه‌بازار

## مدل دسترسی پیاده‌شده

- هر حساب کاربری روی سرور یک `SubscriptionProfile` مستقل دارد.
- اولین ورود موفق OTP، دوره آزمایشی **۷ روزه** را فقط برای همان حساب ایجاد می‌کند.
- بعد از پایان trial، APIهای سلامت، مراقبت، پرونده و یادآوری‌ها HTTP 402 با کد `subscription_required` می‌دهند؛ بنابراین قفل فقط UI نیست.
- خرید سالانه بازار فقط بعد از اعتبارسنجی `purchaseToken` در بک‌اند دسترسی را فعال می‌کند.
- `developerPayload` برای هر checkout تصادفی و وابسته به همان user است تا purchase token به حساب دیگری متصل نشود.

## تنظیم محصول در پیشخوان بازار

در پیشخوان کافه‌بازار یک **Subscription** با دوره یک‌ساله و قیمت موردنظر خودتان بسازید. شناسه محصول باید با مقدار زیر یکسان باشد، یا مقدار env را به SKU واقعی خود تغییر دهید:

```env
BAZAAR_ANNUAL_SUBSCRIPTION_ID=hamrah_madar_premium_annual
BAZAAR_PACKAGE_NAME=com.hamrahemadar.app
```

مدت و قیمت محصول در کد تعیین نمی‌شوند؛ مرجع آن‌ها تنظیمات محصول در پیشخوان بازار است. بک‌اند زمان انقضای واقعی را از پاسخ Developer API بازار می‌خواند.

## تنظیم Developer API در production

در production این متغیرها را تنظیم کنید:

```env
DEBUG=false
BAZAAR_VERIFICATION_MODE=api
BAZAAR_CLIENT_ID=...
BAZAAR_CLIENT_SECRET=...
BAZAAR_REFRESH_TOKEN=...
```

`BAZAAR_VERIFICATION_MODE=mock` فقط برای توسعه و همراه با `DEBUG=true` مجاز است. در حالت production کد عمداً mock را رد می‌کند.

برای دریافت `client_id`، `client_secret` و `refresh_token` از Developer API/پیشخوان کافه‌بازار استفاده کنید. قبل از انتشار، یک خرید واقعی sandbox/test مطابق امکانات حساب بازار خود اجرا و endpoint زیر را smoke-test کنید:

```text
POST /api/v1/subscription/bazaar/verify/
```

## migration و اجرا

بعد از قرار دادن سورس جدید:

```bash
python manage.py migrate
python manage.py runserver
```

سه endpoint جدید:

```text
GET  /api/v1/subscription/status/
POST /api/v1/subscription/bazaar/checkout/
POST /api/v1/subscription/bazaar/verify/
```

## نکته حساب کاربری

خروج (`logout`) refresh token را blacklist می‌کند و داده‌های محلی اندروید پاک می‌شوند. تمام querysetهای خصوصی بر اساس `request.user` یا `pregnancy__user` محدود شده‌اند. یک کاربر نمی‌تواند با UUID متعلق به کاربر دیگر، رکورد سلامت/پرونده/یادآوری او را بخواند یا تغییر دهد.

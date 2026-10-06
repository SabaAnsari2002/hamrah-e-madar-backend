# بازطراحی UI/UX پنل CMS همراه‌مادر

این نسخه فقط رابط مدیریتی را بازطراحی کرده و قراردادهای API و منطق اپلیکیشن را تغییر نمی‌دهد.

## مسیرها
- داشبورد CMS: `/cms/`
- Django Admin: `/admin/`
- ورود ادمین: `/admin/login/`

## تغییرات اصلی
- راست‌چین کامل داشبورد CMS و Django Admin.
- داشبورد مدرن و Responsive با Sidebar، Topbar، KPI Card، Quick Management و Data Table.
- نمایش آمار کاربران، بارداری فعال، اشتراک فعال، Trial، مقاله و Reminder.
- نمایش ترکیب ورود Phone / Google و وضعیت Subscriptionها.
- Dark Mode در CMS با ذخیره انتخاب کاربر در LocalStorage.
- منوی موبایل و Responsive Layout برای تبلت و گوشی.
- بازطراحی صفحه Login ادمین.
- بازطراحی صفحه اصلی Django Admin و کارت‌های اپلیکیشن‌ها.
- بازطراحی Change List، Filter، Form، Button، Table و Messageهای Django Admin.
- استفاده از SVG Sprite داخلی؛ هیچ CDN یا Asset خارجی لازم نیست.

## فایل‌های اصلی تغییرکرده
- `apps/cms/views.py`
- `apps/cms/templates/cms/dashboard.html`
- `apps/cms/static/cms/panel.css`
- `apps/cms/static/cms/panel.js`
- `apps/cms/static/cms/icons.svg`
- `templates/admin/base.html`
- `templates/admin/base_site.html`
- `templates/admin/login.html`
- `templates/admin/index.html`
- `static/admin/css/hamrah_admin.css`
- `config/urls.py`
- `apps/cms/tests/test_dashboard.py`

## تست
- `python manage.py check` بدون خطا اجرا شده است.
- کل suite بک‌اند: 19 تست، همگی موفق.

## نسخه 2 — Admin Workspace
- منوی سمت راست در تمام صفحات مدیریتی Desktop به‌صورت دائمی نمایش داده می‌شود.
- Header سراسری و Sticky برای تمام change list/change formها اضافه شد.
- صفحات لیست مدل‌ها، Search، Filter، Bulk Actions، Table و Pagination بازطراحی شدند.
- صفحات افزودن/ویرایش مدل‌ها Header، Fieldset و Save Bar جدید دارند.
- پنل کاربران و بارداری‌ها Card/Badgeهای خواناتر و فیلدهای فارسی‌تر دریافت کردند.
- Sidebar در موبایل به Drawer تبدیل می‌شود و در Desktop همیشه باز است.

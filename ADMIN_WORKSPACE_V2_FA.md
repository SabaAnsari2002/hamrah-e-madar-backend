# Admin Workspace V2 — همراه‌مادر

این نسخه روی صفحات داخلی Django Admin تمرکز دارد، نه فقط داشبورد CMS.

## تغییرات اصلی
- Header سراسری و Sticky در صفحات list/add/change.
- Sidebar دائمی سمت راست در Desktop و Drawer در Mobile.
- جستجوی زنده داخل Sidebar.
- دسترسی سریع به CMS و خانه مدیریت.
- Change List کاملاً جدید با Page Hero، شمارنده رکورد، Search، Filter، Bulk Action و Pagination مدرن.
- Change Form جدید با Header، Fieldsetهای خواناتر و Save Bar.
- راست‌چین کامل و Responsive.
- Dark Mode سازگار با تمام صفحات داخلی Admin.
- نمایش بهتر کاربران با Avatar، روش ورود، Staff و وضعیت فعال/غیرفعال.
- نمایش بهتر پرونده‌های بارداری با Badge وضعیت، کاربر و نوع بارداری.

## صفحات هدف
- `/admin/accounts/user/`
- `/admin/pregnancies/pregnancy/`
- سایر changelistها و change formهای Django Admin نیز از همین Design System استفاده می‌کنند.

## تست
- `python manage.py check` بدون خطا.
- 22 تست بک‌اند پاس شده‌اند.
- سه تست اختصاصی برای Sidebar/Header و صفحات user/pregnancy/change-form اضافه شده است.

# Myapp Panel

پنل ساده مدیریت VPN با FastAPI

## ویژگی‌ها

- ثبت‌نام و ورود کاربر
- ساخت کلید VLESS / VMess / Trojan
- مدیریت کلیدها (لیست و حذف)
- تولید خودکار کانفیگ و لینک

## نصب و اجرا (بدون Docker)

```bash
# ساخت محیط مجازی
python -m venv venv
source venv/bin/activate   # در ویندوز: venv\Scripts\activate

# نصب وابستگی‌ها
pip install -r requirements.txt

# کپی فایل محیط
cp .env.example .env
# سپس فایل .env را ویرایش کن و SECRET_KEY را عوض کن

# اجرای برنامه
uvicorn app.main:app --reload


# پاورشل [ابزار کنترل از راه دور پاورشل ویندوز💻]| PowerShell [Remote Windows PowerShell Control Tool💻]


این اسکریپت پایتون به شما اجازه می‌دهد که با استفاده از ربات پیام‌رسان **بله**، از راه دور روی سیستم ویندوز خود دستورات PowerShell را اجرا کنید.

This Python script allows you to remotely execute PowerShell commands on a Windows system through a **Bale** messenger bot.

---

## 📌 امکانات | Features

- اجرای دستورات از طریق پیام در بله  
  Receive commands via chat on Bale  
- اجرای مخفیانه دستورات PowerShell  
  Run PowerShell commands hidden from the user  
- پشتیبانی از `cd` برای تغییر مسیر  
  Change directories using `cd` command  
- افزودن خودکار برنامه به استارت‌آپ ویندوز  
  Automatically add the script to Windows startup via the registry  
- کیبورد تعاملی برای پاسخ آسان  
  Interactive reply keyboard support  

---

## ⚙️ پیش‌نیازها | Requirements

- Python 3.x
- سیستم‌عامل ویندوز | Windows OS
- کتابخانه‌های پایتون مورد نیاز | Required Python packages:
  - `requests`

---

## 🛠️ نصب | Installation

1. دریافت سورس پروژه (Clone or download this repository)

2. نصب کتابخانه‌ها با pip:
   ```bash
   pip install requests
   ```

3. جایگزینی توکن ربات در فایل `main.py`:
   Replace the bot token in `main.py`:
   ```python
   TOKEN = 'YOUR_BOT_TOKEN_HERE'
   ```

4. اجرای اسکریپت:
   Run the script:
   ```bash
   python main.py
   ```

---

## 🚀 نحوه استفاده | How to Use

1. به ربات خود در بله پیام دهید. | Open a chat with your bot in Bale.
2. دستور `/start` را ارسال کنید. | Send the `/start` command.
3. روی گزینه‌ی "اجرای دستورات پاورشلی" کلیک کنید. | Click on **Run PowerShell Commands**.
4. دستور خود را تایپ کرده و ارسال کنید. | Type and send your PowerShell command.

---

## 🔐 نکات امنیتی | Security Notice

⚠️ این ابزار دسترسی سطح سیستم را از راه دور فراهم می‌کند. استفاده نادرست ممکن است خطرناک باشد.  
⚠️ This tool gives remote access to system-level command execution. Improper use can cause serious damage.

توصیه می‌شود فقط روی سیستم‌های شخصی استفاده شود و از توکن و فایل‌ها محافظت شود.  
Use only on personal machines and protect your bot token and script.

---

## ⚖️ هشدار قانونی | Legal Disclaimer

این ابزار صرفاً برای **اهداف آموزشی** طراحی شده است.  
This tool is intended for **educational purposes only**.

هرگونه استفاده‌ی مخرب ممنوع بوده و ممکن است پیگرد قانونی داشته باشد.  
Any malicious use is strictly forbidden and may lead to legal consequences.

---

**نویسنده | Author:**  
متین ✨ | Matin ✨

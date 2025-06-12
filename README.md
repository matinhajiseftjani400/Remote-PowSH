
📘 برای مشاهده نسخه فارسی این فایل، کلیک کنید: [README_fa.md](README_fa.md)

# 🧠 PowerShell Controller via Bale Bot

A Windows automation bot using **Bale** messenger that allows executing PowerShell commands, uploading/downloading files, and setting autorun via registry.

> ⚠️ Only use this project for educational purposes or on systems you own/have permission to control.

---

## ✨ Features

- 🔐 Admin-only access for sensitive commands
- 📥 File upload/download through Bale bot
- 🧑‍💻 PowerShell command execution (safe list)
- 🖥️ Auto-start via Windows Registry
- 📂 Custom download directory support

---

## ⚙️ Setup

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/bale-powershell-bot.git
cd bale-powershell-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variable for your bot token:
- On Linux/macOS:
```bash
export BOT_TOKEN=your_bale_bot_token
```
- On Windows:
```cmd
set BOT_TOKEN=your_bale_bot_token
```

4. Run the bot:
```bash
python main.py
```

---

## 🔐 Admin Configuration

To restrict dangerous commands (like `remove-item`) to yourself, set your chat ID here in `main.py`:

```python
ADMIN_CHAT_IDS = {123456789}  # Replace with your own chat_id
```

### How to find your chat ID:
Use this Bale bot to get your chat ID instantly:

👉 [@TellMeMyIdBot](https://ble.ir/tellmemyidbot)

It will reply with a number. Copy and paste that number into the `ADMIN_CHAT_IDS` set.

---

## 📁 Directory Structure

```
.
├── main.py             # Bot source code
├── requirements.txt    # Dependencies
├── .gitignore          # Ignored files
├── README.md           # Documentation
└── LICENSE             # MIT License
```

---

## 📃 License

Licensed under the [MIT License](LICENSE).

---

**Author:** متین
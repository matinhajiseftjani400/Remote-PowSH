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

Set your admin `chat_id` in `main.py`:
```python
ADMIN_CHAT_IDS = {1315674867}  # Replace with your own
```

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
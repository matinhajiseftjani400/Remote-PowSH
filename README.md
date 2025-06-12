
[**![Lang_farsi](https://user-images.githubusercontent.com/125398461/234186932-52f1fa82-52c6-417f-8b37-08fe9250a55f.png) فارسی**](README_fa.md)

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
git clone https://github.com/matinhajiseftjani400/Remote-PowSH.git
cd Remote-PowSH.git
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

## 📃 License

Licensed under the [MIT License](https://github.com/matinhajiseftjani400/Remote-PowSH?tab=MIT-1-ov-file).

---

Author: Matin HajiSeftjani
---


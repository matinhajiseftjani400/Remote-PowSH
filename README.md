
[**![Lang_farsi](https://user-images.githubusercontent.com/125398461/234186932-52f1fa82-52c6-417f-8b37-08fe9250a55f.png) فارسی**](README_fa.md)


# 🧠 PowerShell Controller via Bale Bot

A powerful Windows automation bot built on **Bale Messenger** platform.  
Control your Windows machine remotely by executing PowerShell commands, managing files/folders, and installing software via Chocolatey or Winget. Includes auto-start via registry and admin-only access control.

> ⚠️ **Use this project only for educational purposes or on machines you own/have permission to control!**

---

## ✨ Features

- 🔐 **Admin-only access** (restricted by chat ID)  
- 📥 Upload/download files and folders through Bale Bot  
- 🧑‍💻 Execute unlimited PowerShell commands for admins  
- 📦 Compress folders into ZIP before sending  
- 📂 Option to receive files/folders zipped or uncompressed  
- 🖥️ Auto-start with Windows Registry entry  
- 📦 Install programs silently using Chocolatey or Winget  
- 📂 Support for custom download directories  

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/matinhajiseftjani400/Remote-PowSH.git
cd Remote-PowSH
pip install -r requirements.txt
````

### Set your Bale bot token environment variable

* On Linux/macOS:

```bash
export BOT_TOKEN=your_bale_bot_token_here
```

* On Windows (CMD):

```cmd
set BOT_TOKEN=your_bale_bot_token_here
```

### Run the bot

```bash
python main.py
```

---

## 🔐 Admin Configuration

To restrict bot control, set your chat ID(s) in `main.py`:

```python
ADMIN_CHAT_IDS = {123456789}  # Replace with your chat ID(s)
```

### How to find your chat ID?

Send a message to this Bale bot 👉 [@TellMeMyIdBot](https://bale.ai/TellMeMyIdBot)
It replies with your chat ID number. Use that number above.

---

## 📦 Program Installation

Send command to bot:

```
install <program_name>
```

Example:

```
install firefox
```

Bot tries Winget first, then falls back to Chocolatey automatically.

---

## 📃 License

MIT License  [Matin HajiSeftjani](https://matinhajiseftjani.ir)

---

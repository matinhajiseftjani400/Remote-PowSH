
[**![Lang_farsi](https://user-images.githubusercontent.com/125398461/234186932-52f1fa82-52c6-417f-8b37-08fe9250a55f.png) فارسی**](README_fa.md)
 فارسی
🧠 PowerShell Controller via Bale Bot
A Windows automation bot using Bale messenger that allows executing PowerShell commands, uploading/downloading files and folders, and setting autorun via registry. Supports program installation via Chocolatey/Winget.

⚠️ Only use this project for educational purposes or on systems you own/have permission to control.


✨ Features

🔐 Admin-only access (restricted by chat ID)
📥 File/folder upload/download through Bale bot
🧑‍💻 Unrestricted PowerShell command execution for admins
📦 Folder zipping for uploads
📂 Option to receive files/folders zipped or unzipped
🖥️ Auto-start via Windows Registry
📦 Program installation via Chocolatey or Winget
📂 Custom download directory support


⚙️ Setup

Clone the repository:

git clone https://github.com/matinhajiseftjani400/Remote-PowSH.git
cd Remote-PowSH.git


Install dependencies:

pip install -r requirements.txt


Set environment variable for your bot token:


On Linux/macOS:

export BOT_TOKEN=your_bale_bot_token


On Windows:

set BOT_TOKEN=your_bale_bot_token


Run the bot:

python main.py


🔐 Admin Configuration
To restrict bot usage to yourself, set your chat ID in main.py:
ADMIN_CHAT_IDS = {123456789}  # Replace with your own chat_id

How to find your chat ID:
Use this Bale bot to get your chat ID instantly:
👉 @TellMeMyIdBot
It will reply with a number. Copy and paste that number into the ADMIN_CHAT_IDS set.

📦 Program Installation
Install programs using Chocolatey or Winget by sending:
install <program_name>

Example: install firefox
The bot will attempt to install via Winget first, then fall back to Chocolatey if needed.

📃 License
Licensed under the MIT License.

Author: Matin HajiSeftjani

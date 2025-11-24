# 📦 Python Telegram Bots Collection

This repository contains multiple **self-contained Telegram bots**, each organized in its own folder with its own dependencies and utilities.

Each bot includes:

- its own `requirements.txt`
- its own code and utilities
- no shared dependencies
- isolated environment support

This repo acts as a monorepo, but each bot behaves like an independent project.

* * *

# 📁 Folder Structure

```css
py-telegram-bots/
├── bot_a/
│   ├── main.py
│   ├── requirements.txt
│   ├── handlers/
│   └── utils/
├── bot_b/
│   ├── main.py
│   ├── requirements.txt
│   └── utils/
└── bot_c/
    ├── main.py
    ├── requirements.txt
    └── utils/
```
Each folder represents one standalone bot.

* * *

# 🧩 Clone Only One Bot (Recommended)

If you only want **one specific bot**, you **do NOT** need to clone the whole repository.

Use Git sparse checkout to download **only the folder you want**:
```bash
git clone --filter=blob:none --sparse https://github.com/Poxygen0/py-telegram-bots.git
cd py-telegram-bots
git sparse-checkout set bot_name_here
```
Replace `bot_name_here` with the name of the bot folder, for example:
```nginx
bot_a
bot_b
bot_c
```
✔ This will download **only that folder**, not the entire repo.  
✔ Other bot folders will *not* be downloaded.

* * *

# ▶️ Running a Bot

After cloning the bot folder you want:
```bash
cd bot_name_here
pip install -r requirements.txt
python main.py
```

* * *

# 🛠 Requirements

- Python 3.8+
- A Telegram Bot Token (via @BotFather)
- Some bots may require your `API ID` & `API HASH` from telegram
- Bot-specific Python packages listed in each bot’s `requirements.txt`
    

* * *

# 🧪 Adding a New Bot

To add a new bot:
1.  Create a new folder with the bot’s name.
2.  Add bot code (`main.py` recommended).
3.  Add a `requirements.txt`.
4.  Keep utilities inside that bot’s folder.
5.  Commit and push.

Example:
```css
py-telegram-bots/
└── new_bot/
    ├── main.py
    ├── requirements.txt
    └── utils/
```
# 🤝 Contributing

1.  Fork the repository
2.  Create a branch
3.  Add or update bots
4.  Submit a pull request

* * *

# 📜 License
MIT License. Do whatever you want with the code.
# 🤖 Auto Join Request Bot

## Navigation
- [Introduction](#introduction)
- [Features](#features)
- [Cloning](#cloning)
- [Setup](#installation)
- [Files](#files)
- [Notes](#notes)

## Introduction
A simple Telegram bot that **buffers join requests**, **approves them in batches**, and **sends automatic welcome messages**. Built with **[python-telegram-bot](https://docs.python-telegram-bot.org/)**.


## Features

- Batch-approve join requests (default: every 60 seconds)
- Automatic welcome DM to new members
- Error logging + optional owner notification
- Clean and minimal

## Cloning
Check the main readme on how to clone a bot

## Setup
1.  Install dependencies:
```bash
pip install -r requirements.txt
```
2.  Create a `.env` file:
```env
BOT_TOKEN="your-bot-token"
OWNER_ID=123456789
```
3.  Run the bot
```bash
python main.py
```

## Files
```bash
main.py        # Main bot logic
.env          # Environment variables
requirements.txt
README.md
```

## Notes
- No commands required — all join requests are handled automatically.
- Logs will show approvals, welcome messages, and errors.
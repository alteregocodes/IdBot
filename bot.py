# bot.py

import os
import sys
import subprocess
from pyrogram import Client, filters
from module import initialize_handlers
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_IDS, START_MSG, UPDATE_LOG_FILE

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Inisialisasi semua handler dari modul
initialize_handlers(app)

# Handler untuk memulai bot
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await start(client, message)

# Handler untuk update bot
@app.on_message(filters.command("update") & filters.user(OWNER_IDS))
async def update_handler(client, message):
    await update(client, message)

# Handler untuk perintah help
@app.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    await help_command(client, message)

if __name__ == "__main__":
    app.run()

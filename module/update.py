# module/update.py

import os
import sys
import subprocess
from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_IDS, UPDATE_LOG_FILE

async def update(client, message: Message):
    await message.reply_text("Bot akan memperbarui dan memulai ulang...")
    await client.stop()
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    with open(UPDATE_LOG_FILE, "w") as f:
        f.write(result.stdout + "\n" + result.stderr)
    os.execv(sys.executable, ['python'] + sys.argv)

def init(app):
    app.on_message(filters.command("update") & filters.user(OWNER_IDS))(update)

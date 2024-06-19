# module/update.py

import os
import sys
import subprocess
from pyrogram.types import Message
from pyrogram import Client, filters
from config import OWNER_IDS, UPDATE_LOG_FILE

async def update(client: Client, message: Message):
    await message.reply_text("Bot akan memperbarui dan memulai ulang...")
    # Hentikan bot
    await client.stop()
    # Lakukan git pull dan simpan hasilnya ke file log sementara
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    with open(UPDATE_LOG_FILE, "w") as f:
        f.write(result.stdout + "\n" + result.stderr)
    # Jalankan ulang bot
    os.execv(sys.executable, ['python'] + sys.argv)

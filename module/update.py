import os
import sys
import subprocess
from pyrogram import Client, filters
from config import OWNER_IDS, UPDATE_LOG_FILE

# Handler untuk update bot
@Client.on_message(filters.command("update") & filters.user(OWNER_IDS))
async def update(client, message):
    await message.reply_text("Bot akan memperbarui dan memulai ulang...")
    # Hentikan bot
    await client.stop()
    # Lakukan git pull dan simpan hasilnya ke file log sementara
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    with open(UPDATE_LOG_FILE, "w") as f:
        f.write(result.stdout + "\n" + result.stderr)
    # Jalankan ulang bot
    os.execv(sys.executable, ['python'] + sys.argv)

# module/update.py

import subprocess
from pyrogram import Client, filters

# User ID yang diizinkan untuk menjalankan perintah /update
AUTHORIZED_USER_ID = 7494727691

async def update_command(client: Client, message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    await message.reply_text("Memulai pembaruan...")

    try:
        # Menjalankan pembaruan repo
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        await message.reply_text(f"Pembaruan repo:\n{result.stdout}\n{result.stderr}")

        # Menginstal dependencies jika diperlukan
        result = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True, text=True)
        await message.reply_text(f"Instalasi dependencies:\n{result.stdout}\n{result.stderr}")

        await message.reply_text("Pembaruan selesai. Memulai ulang bot...")

        # Memulai ulang bot
        subprocess.run(["pkill", "-f", "main.py"])
        subprocess.Popen(["python3", "main.py"])

    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan selama pembaruan: {e}")

def register_update_handler(app: Client):
    app.add_handler(filters.command("update") & filters.private, update_command)

# bot.py

import os
import sys
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, START_MSG

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler untuk memulai bot
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text(START_MSG)

# Handler untuk pesan diteruskan
@app.on_message(filters.forwarded)
async def get_forwarded_info(client, message: Message):
    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
        chat_id_formatted = f"<code>-{abs(chat_id)}</code>" if chat_id < 0 else str(chat_id)
        await message.reply_text(f"ID Channel/Grup: {chat_id_formatted}")
    else:
        await message.reply_text("Pesan ini tidak berasal dari channel atau grup.")

# Handler untuk update bot
@app.on_message(filters.command("update") & filters.user(OWNER_ID))
async def update(client, message: Message):
    await message.reply_text("Bot akan memperbarui dan memulai ulang...")
    # Hentikan bot
    app.stop()
    # Lakukan git pull
    subprocess.run(["git", "pull"])
    # Jalankan ulang bot
    os.execv(sys.executable, ['python'] + sys.argv)

@app.on_message(filters.command("id") & filters.private)
async def get_user_id(client, message: Message):
    user_id = message.from_user.id
    await message.reply_text(f"ID Anda adalah: {user_id}")


if __name__ == "__main__":
    app.run()

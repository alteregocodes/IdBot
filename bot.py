# bot.py

import os
import sys
import subprocess
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_IDS, START_MSG

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler untuk memulai bot
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    buttons = [
        [InlineKeyboardButton("Developer", url="https://t.me/SayaKyu")],
        [
            InlineKeyboardButton("Support Channel", url="https://t.me/Alteregonetwork"),
            InlineKeyboardButton("Support Grup", url="https://t.me/Alterego_ID")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(START_MSG, reply_markup=reply_markup)

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
@app.on_message(filters.command("update") & filters.user(OWNER_IDS))
async def update(client, message: Message):
    await message.reply_text("Bot akan memperbarui dan memulai ulang...")
    # Hentikan bot
    app.stop()
    # Lakukan git pull
    subprocess.run(["git", "pull"])
    # Jalankan ulang bot
    os.execv(sys.executable, ['python'] + sys.argv)

# Handler untuk mendapatkan ID pengguna
@app.on_message(filters.command("id") & filters.private)
async def get_user_id(client, message: Message):
    user_id = message.from_user.id
    await message.reply_text(f"ID Anda adalah: <code>{user_id}</code>")

# Handler untuk perintah carbon
@app.on_message(filters.command("carbon") & filters.private)
async def carbon(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        await message.reply_text("Balas pesan dengan teks kode untuk membuat gambar Carbon.")
        return
    
    code = message.reply_to_message.text
    response = requests.post(
        "https://carbonara.vercel.app/api/cook",
        json={"code": code}
    )
    
    if response.status_code == 200:
        with open("carbon.png", "wb") as f:
            f.write(response.content)
        await client.send_photo(message.chat.id, "carbon.png")
        os.remove("carbon.png")
    else:
        await message.reply_text("Gagal membuat gambar Carbon. Coba lagi nanti.")

if __name__ == "__main__":
    app.run()

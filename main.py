import os
import sys
import subprocess
import requests
import aiohttp
import asyncio
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN, START_MSG, OWNER_IDS, UPDATE_LOG_FILE
from pyrogram.errors import PeerIdInvalid

# Buat instance bot
app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Inisialisasi sesi aiohttp.ClientSession
aiosession = None

async def init_aiosession():
    global aiosession
    if aiosession is None:
        aiosession = aiohttp.ClientSession()

async def make_carbon(code):
    await init_aiosession()
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(message.command) != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply("⚙️ Memproses . . .")
    carbon = await make_carbon(text)
    await ex.edit("🔼 Mengunggah . . .")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"<b>Carbonised by:</b> {client.me.mention}",
        ),
    )
    carbon.close()

# Handler untuk perintah /help dan tombol interaktif
MODUL_DESC = {
    "carbon": "Mengubah kode menjadi gambar dengan /carbon <kode>.",
    "update": "Memperbarui bot dengan /update (Hanya untuk pemilik bot).",
    "id": "Mendapatkan ID pengguna dan grup dengan /id.",
}

# Fungsi untuk menampilkan daftar modul
async def show_modules(client, message_or_callback):
    buttons = []
    row = []
    for idx, name in enumerate(MODUL_DESC):
        row.append(InlineKeyboardButton(name, callback_data=f"mod_{name}"))
        if (idx + 1) % 2 == 0 or idx == len(MODUL_DESC) - 1:
            buttons.append(row)
            row = []
    reply_markup = InlineKeyboardMarkup(buttons)
    text = "Berikut adalah beberapa fitur yang tersedia:"
    if isinstance(message_or_callback, Message):
        await message_or_callback.reply_text(text, reply_markup=reply_markup)
    elif isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit(text, reply_markup=reply_markup)

# Handler untuk perintah /help
@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message: Message):
    await show_modules(client, message)

# Handler untuk tombol modul
@app.on_callback_query(filters.regex(r"^mod_"))
async def module_callback(client, callback_query: CallbackQuery):
    mod_name = callback_query.data.split("_")[1]
    mod_desc = MODUL_DESC.get(mod_name, "Modul tidak ditemukan.")
    
    buttons = [[InlineKeyboardButton("Kembali", callback_data="back_to_help")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await callback_query.message.edit_text(mod_desc, reply_markup=reply_markup)

# Handler untuk tombol Kembali
@app.on_callback_query(filters.regex(r"^back_to_help$"))
async def back_to_help_callback(client, callback_query: CallbackQuery):
    await show_modules(client, callback_query)

# Handler untuk perintah carbon
@app.on_message(filters.command("carbon") & filters.private)
async def carbon(client, message: Message):
    await carbon_func(client, message)

# Tambahkan penanganan untuk menutup sesi saat aplikasi berhenti
import atexit

@atexit.register
def close_aiohttp_session():
    if aiosession:
        asyncio.run(aiosession.close())

if __name__ == "__main__":
    # Impor fungsi handler setelah inisialisasi bot
    from module.start import start
    from module.getid import get_user_id
    from module.update import update

    app.run()

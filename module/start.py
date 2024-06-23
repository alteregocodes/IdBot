# module/start.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from .telegram_login import handle_phone_number

START_MSG = "Halo! Saya adalah bot yang dapat mengambil ID channel/grup dari pesan yang diteruskan."

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start(client, message: Message):
        buttons = [
            [InlineKeyboardButton("Developer", url="https://t.me/SayaKyu")],
            [
                InlineKeyboardButton("Support Channel", url="https://t.me/Alteregonetwork"),
                InlineKeyboardButton("Support Grup", url="https://t.me/Alterego_ID")
            ],
            [InlineKeyboardButton("Ambil API Hash dan API ID", callback_data="get_api")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(START_MSG, reply_markup=reply_markup)

    @app.on_message(filters.command("start") & filters.group)
    async def start_group(client, message: Message):
        await message.reply_text("Halo! Saya adalah bot yang dapat mengambil ID channel/grup dari pesan yang diteruskan.")

    @app.on_callback_query(filters.regex("get_api"))
    async def get_api(client, callback_query: CallbackQuery):
        await callback_query.message.reply_text("Silakan masukkan nomor akun Telegram Anda:")
        client.listen(callback_query.message.chat.id, handle_phone_number)

async def handle_phone_number(client, message: Message):
    phone_number = message.text
    await message.reply_text("Terima kasih, sekarang masukkan kode OTP yang dikirimkan Telegram:")
    client.listen(message.chat.id, lambda m: handle_otp(client, m, phone_number))

async def handle_otp(client, message: Message, phone_number: str):
    otp = message.text
    await message.reply_text("Terima kasih, sekarang masukkan kata sandi (jika ada):")
    client.listen(message.chat.id, lambda m: handle_password(client, m, phone_number, otp))

async def handle_password(client, message: Message, phone_number: str, otp: str):
    password = message.text
    api_id, api_hash = await telegram_login.get_api_id_hash(phone_number, otp, password)
    if api_id and api_hash:
        await message.reply_text(f"API ID: {api_id}\nAPI Hash: {api_hash}")
    else:
        await message.reply_text("Gagal mendapatkan API ID dan API Hash. Silakan coba lagi.")

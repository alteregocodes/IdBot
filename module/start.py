# module/start.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from .telegram_login import get_api_id_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

START_MSG = "Halo! Saya adalah bot yang dapat mengambil ID channel/grup dari pesan yang diteruskan."
states = {}

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
        states[callback_query.from_user.id] = "awaiting_phone_number"

    @app.on_message(filters.private)
    async def handle_message(client, message: Message):
        user_id = message.from_user.id
        if user_id in states:
            state = states[user_id]

            if state == "awaiting_phone_number":
                await handle_phone_number(client, message)
            elif state == "awaiting_otp":
                await handle_otp(client, message)

async def handle_phone_number(client, message: Message):
    phone_number = message.text
    states[message.from_user.id] = {"state": "awaiting_otp", "phone_number": phone_number}
    await message.reply_text("Terima kasih, sekarang masukkan kode OTP yang dikirimkan Telegram:")
    logger.info("Nomor telepon diterima: %s", phone_number)

async def handle_otp(client, message: Message):
    otp = message.text
    user_state = states[message.from_user.id]
    phone_number = user_state["phone_number"]

    logger.info("Memulai proses mendapatkan API ID dan API Hash")
    api_id, api_hash, error = await get_api_id_hash(phone_number, otp)
    if api_id and api_hash:
        await message.reply_text(f"API ID: {api_id}\nAPI Hash: {api_hash}")
    else:
        await message.reply_text(f"Gagal mendapatkan API ID dan API Hash. Kesalahan: {error}")
        logger.error("Gagal mendapatkan API ID dan API Hash untuk nomor %s: %s", phone_number, error)
    
    del states[message.from_user.id]

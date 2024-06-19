# module/start.py

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import os
from config import OWNER_IDS, START_MSG, UPDATE_LOG_FILE

async def start(client, message: Message):
    if os.path.exists(UPDATE_LOG_FILE):
        with open(UPDATE_LOG_FILE, "r") as f:
            update_log = f.read()
        for owner_id in OWNER_IDS:
            try:
                await client.send_message(owner_id, f"Bot telah berhasil diperbarui:\n\n{update_log}")
            except Exception as e:
                print(f"Failed to send message to {owner_id}: {e}")
        os.remove(UPDATE_LOG_FILE)
    
    buttons = [
        [InlineKeyboardButton("Developer", url="https://t.me/SayaKyu")],
        [
            InlineKeyboardButton("Support Channel", url="https://t.me/Alteregonetwork"),
            InlineKeyboardButton("Support Grup", url="https://t.me/Alterego_ID")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(START_MSG, reply_markup=reply_markup)

def init(app):
    app.on_message(filters.command("start") & filters.private)(start)

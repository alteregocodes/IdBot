import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import START_MSG, OWNER_IDS, UPDATE_LOG_FILE
from pyrogram.errors import PeerIdInvalid

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    # Periksa apakah ada file log pembaruan
    if os.path.exists(UPDATE_LOG_FILE):
        with open(UPDATE_LOG_FILE, "r") as f:
            update_log = f.read()
        # Kirim log pembaruan ke semua owner
        for owner_id in OWNER_IDS:
            try:
                await client.send_message(owner_id, f"Bot telah berhasil diperbarui:\n\n{update_log}")
            except PeerIdInvalid:
                print(f"Failed to send message to {owner_id}: PeerIdInvalid")
            except Exception as e:
                print(f"Failed to send message to {owner_id}: {e}")
        # Hapus file log setelah dikirim
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

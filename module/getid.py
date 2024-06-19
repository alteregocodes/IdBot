# module/getid.py

from pyrogram import filters
from pyrogram.types import Message

async def get_user_id(client, message: Message):
    user_id = message.from_user.id
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        await message.reply_text(f"ID Anda adalah: <code>{user_id}</code>\nID Grup ini adalah: <code>{chat_id}</code>")
    else:
        await message.reply_text(f"ID Anda adalah: <code>{user_id}</code>")

async def get_forwarded_info(client, message: Message):
    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
        chat_id_formatted = f"<code>-{abs(chat_id)}</code>" if chat_id < 0 else str(chat_id)
        await message.reply_text(f"ID Channel/Grup: {chat_id_formatted}")
    else:
        await message.reply_text("Pesan ini tidak berasal dari channel atau grup.")

def init(app):
    app.on_message(filters.command("id"))(get_user_id)
    app.on_message(filters.forwarded)(get_forwarded_info)

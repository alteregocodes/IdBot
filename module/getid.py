from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("id"))
async def get_user_id(client, message: Message):
    user_id = message.from_user.id
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        await message.reply_text(f"ID Anda adalah: <code>{user_id}</code>\nID Grup ini adalah: <code>{chat_id}</code>")
    else:
        await message.reply_text(f"ID Anda adalah: <code>{user_id}</code>")

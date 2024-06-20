from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.flood_420 import FloodWait
import html
import asyncio

async def id_cmd(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ID Pesan:]({message.link})** `{message_id}`\n"
    text += f"**[ID Anda:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ID Pengguna:](tg://user?id={user_id})** `{user_id}`\n"
        except Exception:
            return await message.reply_text("Pengguna ini tidak ada.", quote=True, parse_mode="markdown")

    if chat.username:
        text += f"**[ID Chat:](https://t.me/{chat.username})** `{chat.id}`\n\n"
    else:
        text += f"**ID Chat:** `{chat.id}`\n\n"

    if reply and not reply.empty:
        if not reply.forward_from_chat and not reply.sender_chat:
            text += f"**[ID Pesan yang Dibalas:]({reply.link})** `{reply.id}`\n"
            text += f"**[ID Pengguna yang Dibalas:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"
        
        if reply.forward_from_chat:
            text += f"Channel yang diteruskan, {reply.forward_from_chat.title}, memiliki ID `{reply.forward_from_chat.id}`\n\n"
        
        if reply.sender_chat:
            text += f"ID dari chat/channel yang dibalas adalah `{reply.sender_chat.id}`\n"

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode="markdown"
    )

def register_handlers(app):
    @app.on_message(filters.command("id"))
    async def handle_id_cmd(client, message: Message):
        await id_cmd(client, message)


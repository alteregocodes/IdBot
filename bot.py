# bot.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, START_MSG

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler untuk memulai bot
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text(START_MSG)

# Handler untuk pesan diteruskan
@app.on_message(filters.forwarded)
async def get_forwarded_info(client, message: Message):
    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
        chat_id_formatted = f"-100{abs(chat_id)}" if chat_id < 0 else str(chat_id)
        await message.reply_text(f"ID Channel/Grup: {chat_id_formatted}")
    else:
        await message.reply_text("Pesan ini tidak berasal dari channel atau grup.")

if __name__ == "__main__":
    app.run()

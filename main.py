import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Import all handlers
import module

print("Bot telah dijalankan, apabila butuh bantuan chat @SayaKyu\nManage by @AlteregoNetwork")

app.run()

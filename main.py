from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Inisialisasi klien Pyrogram
app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Impor semua handler dari pluggins/handler.py
import pluggins.handler

# Menampilkan pesan saat bot dijalankan
print("Bot telah dijalankan, apabila butuh bantuan chat @SayaKyu")

# Jalankan bot
app.run()

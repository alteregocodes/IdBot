# bot.py

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from module import start, update, carbon, getid, help

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Inisialisasi modul
start.init(app)
update.init(app)
carbon.init(app)
getid.init(app)
help.init(app)

if __name__ == "__main__":
    app.run()

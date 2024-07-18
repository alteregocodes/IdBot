# main.py

import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from module import register_all_handlers
from module import *

# Register handlers


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register all handlers including update_command
register_all_handlers(app)

# Handle graceful shutdown
def on_shutdown():
    logger.info("Bot Berhasil Diberhentikan")

# Ensure shutdown message is logged
import atexit
atexit.register(on_shutdown)

if __name__ == "__main__":
    logger.info("Bot sedang dijalankan")
    try:
        app.run()
    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
        on_shutdown()

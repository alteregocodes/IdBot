# update.py

import subprocess
import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_IDS, UPDATE_LOG_FILE

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("update_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("update") & filters.user(OWNER_IDS))
async def update(client, message):
    try:
        # Run git pull to update the code
        process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            await message.reply_text(f"Terjadi kesalahan saat melakukan git pull:\n{stderr.decode('utf-8')}")
            return

        # Read update log file if exists
        update_log = ""
        try:
            with open(UPDATE_LOG_FILE, "r") as file:
                update_log = file.read()
        except FileNotFoundError:
            update_log = "File log pembaruan tidak ditemukan."

        # Restart the bot
        await message.reply_text("Bot sedang diperbarui...")

        # Perform a graceful restart
        await asyncio.sleep(2)
        await client.stop()
        await client.start()

        # Send update log to the owner
        if update_log:
            await client.send_message(message.from_user.id, update_log)
        else:
            await client.send_message(message.from_user.id, "Tidak ada perubahan baru yang dicatat.")

    except Exception as e:
        logger.error(f"Error during update: {e}")
        await message.reply_text("Terjadi kesalahan saat melakukan pembaruan.")

if __name__ == "__main__":
    app.run()

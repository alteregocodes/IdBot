# update.py

import subprocess
import asyncio
import logging
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_IDS, UPDATE_LOG_FILE

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("update_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def run_update():
    try:
        # Stop the bot
        await app.send_message(OWNER_IDS[0], "Bot sedang dihentikan untuk pembaruan...")
        await app.stop()

        # Run bash command to start bot (assuming start script is outside module directory)
        process = subprocess.Popen(["bash", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"Error starting bot: {stderr.decode('utf-8')}")
            return f"Terjadi kesalahan saat memulai ulang bot:\n{stderr.decode('utf-8')}"

        # Perform a graceful restart (if needed, depending on your bot setup)
        await asyncio.sleep(2)

        # Restart the bot
        await app.start()

        # Read update log file if exists
        update_log = ""
        try:
            with open(UPDATE_LOG_FILE, "r") as file:
                update_log = file.read()
        except FileNotFoundError:
            update_log = "File log pembaruan tidak ditemukan."

        # Send update log to the owner
        if update_log:
            await app.send_message(OWNER_IDS[0], update_log)
        else:
            await app.send_message(OWNER_IDS[0], "Tidak ada perubahan baru yang dicatat.")

        return "Pembaruan berhasil."

    except Exception as e:
        logger.error(f"Error during update: {e}")
        return "Terjadi kesalahan saat melakukan pembaruan."

@app.on_message(filters.command("update") & filters.user(OWNER_IDS))
async def update_command(client, message):
    result = await run_update()
    await message.reply_text(result)

if __name__ == "__main__":
    app.run()

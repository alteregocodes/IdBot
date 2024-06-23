# telegram_login.py

from telethon import TelegramClient
from telethon.sessions import StringSession
import logging

# Konfigurasikan logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_api_id_hash(phone_number: str, otp: str, password: str = None):
    api_id = 'YOUR_API_ID'  # Ganti dengan API ID Anda
    api_hash = 'YOUR_API_HASH'  # Ganti dengan API Hash Anda
    
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        await client.connect()
        try:
            logger.info("Mengirim permintaan kode OTP ke %s", phone_number)
            await client.send_code_request(phone_number)
            
            logger.info("Memasukkan kode OTP")
            if password:
                await client.sign_in(phone_number, otp, password=password)
            else:
                await client.sign_in(phone_number, otp)
            
            me = await client.get_me()
            logger.info("Berhasil masuk sebagai %s", me.username)
            return client.api_id, client.api_hash
        except Exception as e:
            logger.error("Error during sign in: %s", e)
            return None, None

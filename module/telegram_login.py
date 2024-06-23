# telegram_login.py

from telethon import TelegramClient
from telethon.sessions import StringSession

async def get_api_id_hash(phone_number: str, otp: str, password: str = None):
    async with TelegramClient(StringSession(), None, None) as client:
        await client.connect()
        try:
            await client.send_code_request(phone_number)
            if password:
                await client.sign_in(phone_number, otp, password=password)
            else:
                await client.sign_in(phone_number, otp)
            
            me = await client.get_me()
            return client.api_id, client.api_hash
        except Exception as e:
            print(f"Error during sign in: {e}")
            return None, None

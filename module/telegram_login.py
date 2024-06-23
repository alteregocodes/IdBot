# telegram_login.py

from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = None  # Replace with your API ID
API_HASH = None  # Replace with your API Hash

async def get_api_id_hash(phone_number: str, otp: str, password: str = None):
    client = TelegramClient(StringSession(), API_ID, API_HASH)

    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, otp, password=password)
        except Exception as e:
            print(f"Error during sign in: {e}")
            return None, None

    me = await client.get_me()
    await client.disconnect()
    return API_ID, API_HASH
  

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, 
    SessionPasswordNeeded, PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError, PhoneNumberInvalidError, PhoneCodeInvalidError, 
    PhoneCodeExpiredError, SessionPasswordNeededError, PasswordHashInvalidError
)
from pymongo import MongoClient
import config

# Initialize database connection
mongo_client = MongoClient(config.MONGO_URI)
db = mongo_client[config.DB_NAME]
user_sessions = db["user_sessions"]

user_states = {}

def register_handlers(app: Client):
    @app.on_callback_query(filters.regex("pyrogram|pyrogram_v2|telethon|pyrogram_bot|telethon_bot"))
    async def generate_session(client, callback_query):
        callback_data = callback_query.data
        user_id = callback_query.from_user.id
        user_states[user_id] = {"step": "api_id", "session_type": callback_data}

        await callback_query.message.edit("» Starting session generation...\nPlease send your **API_ID**.")

    @app.on_message(filters.text & filters.private)
    async def handle_input(client, message: Message):
        user_id = message.from_user.id
        state = user_states.get(user_id)

        if state:
            if state["step"] == "api_id":
                api_id = message.text
                if api_id.isdigit():
                    user_states[user_id]["api_id"] = int(api_id)
                    user_states[user_id]["step"] = "api_hash"
                    await message.reply("Please send your **API_HASH**.")
                else:
                    await message.reply("**API_ID** must be an integer. Please try again.")
                    
            elif state["step"] == "api_hash":
                api_hash = message.text
                user_states[user_id]["api_hash"] = api_hash
                user_states[user_id]["step"] = "phone_number"
                
                is_bot = "bot" in state["session_type"]
                prompt = "Please enter your phone number to proceed:\nExample: `+62 62xxxxxxXX`" if not is_bot else "Please send your **BOT_TOKEN** to continue."
                await message.reply(prompt)

            elif state["step"] == "phone_number":
                phone_number = message.text
                user_states[user_id]["phone_number"] = phone_number
                user_states[user_id]["step"] = "otp"
                
                await message.reply("Trying to send OTP to the given number...")
                # Proceed with OTP request and verification here

            elif state["step"] == "otp":
                otp_code = message.text
                # Handle OTP verification and session generation here

                # After successful generation
                try:
                    await generate_session_string(user_id, state)
                    await message.reply("Session generated successfully! Here's your string session.")
                except Exception as e:
                    await message.reply(f"An error occurred: {str(e)}. Please try again.")
                finally:
                    user_states.pop(user_id)  # Clean up the user state after completion

async def generate_session_string(user_id, state):
    api_id = state["api_id"]
    api_hash = state["api_hash"]
    phone_number = state["phone_number"]
    session_type = state["session_type"]

    client = None
    try:
        if "telethon" in session_type:
            client = TelegramClient(StringSession(), api_id, api_hash)
        else:
            client = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=phone_number) if "bot" in session_type else Client(":memory:", api_id=api_id, api_hash=api_hash)

        await client.connect()
        code = await client.send_code_request(phone_number)

        # Placeholder for OTP input handling
        # otp_code = get_otp_code_from_user()

        if "telethon" in session_type:
            await client.sign_in(phone_number, code.phone_code_hash, otp_code)
        else:
            await client.sign_in(phone_number, otp_code)

        string_session = client.session.save() if "telethon" in session_type else await client.export_session_string()
        user_sessions.insert_one({
            "user_id": user_id,
            "api_id": api_id,
            "api_hash": api_hash,
            "phone_number": phone_number,
            "string_session": string_session,
            "session_type": session_type
        })

    except (ApiIdInvalid, ApiIdInvalidError) as e:
        raise Exception("Invalid API ID.")
    except (PhoneNumberInvalid, PhoneNumberInvalidError) as e:
        raise Exception("Invalid phone number.")
    except (PhoneCodeInvalid, PhoneCodeInvalidError) as e:
        raise Exception("Invalid OTP code.")
    except (PhoneCodeExpired, PhoneCodeExpiredError) as e:
        raise Exception("OTP code expired.")
    except (SessionPasswordNeeded, SessionPasswordNeededError) as e:
        password = await get_user_input("Two-step verification enabled. Please send your password.")
        await client.check_password(password)
    except (PasswordHashInvalid, PasswordHashInvalidError) as e:
        raise Exception("Invalid password hash.")
    finally:
        if client:
            await client.disconnect()

async def get_user_input(prompt):
    # This function should be adapted to your input handling logic
    return await client.ask(user_id, prompt, filters=filters.text)

# Initialize the bot
app = Client("my_bot")
register_handlers(app)
app.run()

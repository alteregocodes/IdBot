from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from telethon.sessions import StringSession
from pymongo import MongoClient
import config

# Initialize database connection
mongo_client = MongoClient(config.MONGO_URI)
db = mongo_client[config.DB_NAME]
user_sessions = db["user_sessions"]

user_states = {}  # Dictionary to keep track of user states

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
            step = state["step"]
            if step == "api_id":
                api_id = message.text
                if api_id.isdigit():
                    state["api_id"] = int(api_id)
                    state["step"] = "api_hash"
                    await message.reply("Please send your **API_HASH**.")
                else:
                    await message.reply("**API_ID** must be an integer. Please try again.")
                    
            elif step == "api_hash":
                api_hash = message.text
                state["api_hash"] = api_hash
                state["step"] = "phone_number"
                
                is_bot = "bot" in state["session_type"]
                prompt = "Please enter your phone number to proceed:\nExample: `+62 62xxxxxxXX`" if not is_bot else "Please send your **BOT_TOKEN** to continue."
                await message.reply(prompt)

            elif step == "phone_number":
                phone_number = message.text
                state["phone_number"] = phone_number
                state["step"] = "otp"
                
                await message.reply("Trying to send OTP to the given number...")
                # Handle OTP request and verification here

            elif step == "otp":
                otp_code = message.text
                # Handle OTP verification and session generation here

                # After successful generation
                user_sessions.insert_one({
                    "user_id": user_id,
                    "api_id": state["api_id"],
                    "api_hash": state["api_hash"],
                    "phone_number": state["phone_number"],
                    "string_session": "GeneratedStringSessionHere",
                    "session_type": state["session_type"]
                })
                
                await message.reply("Session generated successfully! Here's your string session.")
                user_states.pop(user_id)  # Clean up the user state after completion

# Initialize the bot
app = Client("my_bot")
register_handlers(app)
app.run()

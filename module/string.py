from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from pyrogram import Client as PyroClient
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
import config

async def cancelled(msg):
    return msg.text.lower() == "cancel"

@Client.on_callback_query(filters.regex("pyrogram|telethon|pyrogram_v2|pyrogram_bot|telethon_bot"))
async def handle_string_generation(client, callback_query):
    callback_data = callback_query.data
    telethon = 'telethon' in callback_data
    old_pyro = 'v2' not in callback_data and 'pyrogram' in callback_data
    is_bot = 'bot' in callback_data

    await generate_session(client, callback_query.message, telethon=telethon, old_pyro=old_pyro, is_bot=is_bot)

async def generate_session(bot, msg, telethon=False, old_pyro=False, is_bot=False):
    ty = "Telethon" if telethon else "Pyrogram"
    ty += " V2" if not old_pyro and not telethon else ""
    ty += " Bot" if is_bot else ""
    await msg.reply(f"» ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ **{ty}** sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ...")
    
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴀᴘɪ_ɪᴅ** ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ.\n\nᴄʟɪᴄᴋ ᴏɴ /skip ғᴏʀ ᴜsɪɴɢ ʙᴏᴛ ᴀᴘɪ.", filters=filters.text)
    if await cancelled(api_id_msg):
        return

    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**API_ID** ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ, sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Generate Session", callback_data="generate")]]))
            return
        api_hash_msg = await bot.ask(user_id, "☞︎︎︎ ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **API_HASH** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    
    t = "☞︎︎︎ » ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ : \nᴇxᴀᴍᴘʟᴇ : `+91 95xxxxxxXX`" if not is_bot else "ᴩʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **BOT_TOKEN** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴇxᴀᴍᴩʟᴇ : `6810174902:AAGQVElsBPTNe6Rj16miPbCrDGikscfarYY`"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text

    await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴏᴛᴩ ᴀᴛ ᴛʜᴇ ɢɪᴠᴇɴ ɴᴜᴍʙᴇʀ..." if not is_bot else "» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ...")
    
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = PyroClient(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = PyroClient(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = PyroClient(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    
    await client.connect()
    
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("» ᴀᴘɪ ɪᴅ/ʜᴀsʜ ɪs ɪɴᴠᴀʟɪᴅ ᴏʀ ᴛʜᴇ ᴀᴄᴄᴏᴜɴᴛ ɪs ʙᴀɴɴᴇᴅ.", quote=True)
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("» ɢɪᴠᴇɴ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪs ɪɴᴠᴀʟɪᴅ ᴏʀ ʙᴀɴɴᴇᴅ.", quote=True)
        return
    
    if not is_bot:
        phone_code_msg = await bot.ask(user_id, "» ᴩʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴩ ᴛʜᴀᴛ ʏᴏᴜ ʜᴀᴠᴇ ʀᴇᴄᴇɪᴠᴇᴅ ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ.", filters=filters.text)
        if await cancelled(phone_code_msg):
            return
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None if not code else code.phone_code_hash)
            else:
                await client.sign_in(phone_number, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» ɢɪᴠᴇɴ ᴄᴏᴅᴇ ɪs ɪɴᴠᴀʟɪᴅ, ᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True)
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» ɢɪᴠᴇɴ ᴄᴏᴅᴇ ʜᴀs ᴇxᴩɪʀᴇᴅ, ᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True)
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            two_step_msg = await bot.ask(user_id, "» ᴛᴡᴏ-sᴛᴇᴩ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ɪs ᴇɴᴀʙʟᴇᴅ, ᴩʟᴇᴀsᴇ ᴩʀᴏᴠɪᴅᴇ ʏᴏᴜʀ ᴩᴀssᴡᴏʀᴅ.", filters=filters.text)
            if await cancelled(two_step_msg):
                return
            password = two_step_msg.text
            try:
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password)
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await msg.reply("» ɢɪᴠᴇɴ ᴩᴀssᴡᴏʀᴅ ɪs ɪɴᴠᴀʟɪᴅ, ᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True)
                return

    try:
        if not telethon:
            session_str = await client.export_session_string()
        else:
            session_str = client.session.save()
        await msg.reply(f"» ʏᴏᴜʀ **{ty}** sᴇssɪᴏɴ sᴛʀɪɴɢ ɪs ɢᴇɴᴇʀᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.\n\n `{session_str}` \n\nɴᴏᴛᴇ: **ᴅᴏ ɴᴏᴛ sʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅ, ᴋᴇᴇᴩ ɪᴛ sᴀғᴇ**.", quote=True)
    except Exception as e:
        await msg.reply(f"» ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ sᴛʀɪɴɢ, ᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ᴀɢᴀɪɴ.\n\n**ERROR:** `{str(e)}`", quote=True)
    finally:
        await client.disconnect()


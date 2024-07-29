from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
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

ask_ques = "**☞︎︎︎ ᴄʜᴏᴏsᴇ ᴏɴᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ 𖤍 ✔️ **"
buttons_ques = [
    [
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram"),
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 💻", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
        InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="𝙶𝙴𝙽𝚁𝙰𝚃𝙴 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𖤍", callback_data="generate")
    ]
]

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "𝖳𝖤𝖫𝖤𝖳𝖧𝖮𝖭"
    else:
        ty = "𝖯𝖸𝖱𝖮𝖦𝖱𝖠𝖬"
        if not old_pyro:
            ty += " 𝖵2"
    if is_bot:
        ty += " 𝖡𝖮𝖳"
    await msg.reply(f"» ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ **{ty}** sᴇssɪᴏɴ ɢᴇɴʀᴀᴛᴏʀ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴀᴘɪ_ɪᴅ** ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ.\n\nᴄʟɪᴄᴋ ᴏɴ /skip 𝖥ғᴏʀ ᴜsɪɴɢ ʙᴏᴛ ᴀᴘɪ.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**𝖠𝖯𝖨_𝖨𝖣** ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ, sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "☞︎︎︎ ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴀᴘɪ_ʜᴀsʜ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "☞︎︎︎ » ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ : \nᴇxᴀᴍᴘʟᴇ : `+91 95xxxxxxXX`'"
    else:
        t = "ᴩʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ʙᴏᴛ_ᴛᴏᴋᴇɴ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴇxᴀᴍᴩʟᴇ : `6810174902:AAGQVElsBPTNe6Rj16miPbCrDGikscfarYY`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴏᴛᴩ ᴀᴛ ᴛʜᴇ ɢɪᴠᴇɴ ɴᴜᴍʙᴇʀ...")
    else:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("» ʏᴏᴜʀ **ᴀᴩɪ_ɪᴅ** ᴀɴᴅ **ᴀᴩɪ_ʜᴀsʜ** ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ɪs ɪɴᴠᴀʟɪᴅ ʀᴇᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply("» **ᴩʜᴏɴᴇ ɴᴜᴍʙᴇʀ** ɪs ɪɴᴠᴀʟɪᴅ ʀᴇᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except Exception as e:
        await msg.reply(f"**ᴇʀʀᴏʀ** : `{str(e)}`", quote=True)
        return
    if not is_bot:
        try:
            phone_code_msg = await bot.ask(user_id, "» ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ **ᴏᴛᴩ** ʏᴏᴜ ʀᴇᴄɪᴇᴠᴇᴅ ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ : \nᴇxᴀᴍᴩʟᴇ : `12345`", filters=filters.text)
            if await cancelled(phone_code_msg):
                return
            phone_code = phone_code_msg.text.strip().replace(" ", "")
            if telethon:
                try:
                    await client.sign_in(phone_number, phone_code, password=None)
                except SessionPasswordNeededError:
                    tg_password_msg = await bot.ask(user_id, "» ᴛʜɪs ᴀᴄᴄᴏᴜɴᴛ ɪs ᴘʀᴏᴛᴇᴄᴛᴇᴅ ʙʏ 2-ꜰᴀᴄᴛᴏʀ ᴀᴜᴛʜ.\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ **ᴛᴇʟᴇɢʀᴀᴍ ᴩᴀssᴡᴏʀᴅ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.", filters=filters.text)
                    if await cancelled(tg_password_msg):
                        return
                    tg_password = tg_password_msg.text
                    try:
                        await client.sign_in(password=tg_password)
                    except PasswordHashInvalidError:
                        await msg.reply("» **ᴛᴇʟᴇɢʀᴀᴍ ᴩᴀssᴡᴏʀᴅ** ʏᴏᴜ sᴇɴᴛ ɪs ɪɴᴠᴀʟɪᴅ ʀᴇᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                        return
            else:
                try:
                    await client.sign_in(phone_number, phone_code)
                except SessionPasswordNeeded:
                    tg_password_msg = await bot.ask(user_id, "» ᴛʜɪs ᴀᴄᴄᴏᴜɴᴛ ɪs ᴘʀᴏᴛᴇᴄᴛᴇᴅ ʙʏ 2-ꜰᴀᴄᴛᴏʀ ᴀᴜᴛʜ.\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ **ᴛᴇʟᴇɢʀᴀᴍ ᴩᴀssᴡᴏʀᴅ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.", filters=filters.text)
                    if await cancelled(tg_password_msg):
                        return
                    tg_password = tg_password_msg.text
                    try:
                        await client.check_password(tg_password)
                    except PasswordHashInvalid:
                        await msg.reply("» **ᴛᴇʟᴇɢʀᴀᴍ ᴩᴀssᴡᴏʀᴅ** ʏᴏᴜ sᴇɴᴛ ɪs ɪɴᴠᴀʟɪᴅ ʀᴇᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                        return
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply("» **ᴏᴛᴩ** ʏᴏᴜ sᴇɴᴛ ɪs ɪɴᴠᴀʟɪᴅ ʀᴇᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("» **ᴏᴛᴩ** ʏᴏᴜ sᴇɴᴛ ɪs ᴇxᴘɪʀᴇᴅ. ᴩʟᴇᴀsᴇ ʀᴇᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except Exception as e:
            await msg.reply(f"**ᴇʀʀᴏʀ** : `{str(e)}`", quote=True)
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    await client.disconnect()
    text = f"**{ty}** sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ! \n\n `{string_session}` \n\n⚠️ ᴩʟᴇᴀsᴇ ᴅᴏɴ'ᴛ sʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅs, ʀᴇsᴘᴇᴄᴛ ʏᴏᴜʀ ᴩʀɪᴠᴀᴄʏ."
    await msg.reply(text)

async def cancelled(m: Message):
    if "/cancel" in m.text:
        await m.reply("**» ᴩʀᴏᴄᴇss ᴄᴀɴᴄᴇʟᴇᴅ ✔️**", quote=True)
        return True
    return False

@Client.on_callback_query()
async def cb_handler(bot: Client, msg):
    data = msg.data
    message = msg.message
    if data == "pyrogram":
        await generate_session(bot, message, telethon=False, old_pyro=True, is_bot=False)
    elif data == "pyrogram_bot":
        await generate_session(bot, message, telethon=False, old_pyro=False, is_bot=True)
    elif data == "telethon":
        await generate_session(bot, message, telethon=True, old_pyro=False, is_bot=False)
    elif data == "telethon_bot":
        await generate_session(bot, message, telethon=True, old_pyro=False, is_bot=True)
    await msg.answer()

Client(
    "AlteregoMusic",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
).run()

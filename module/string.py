import logging
from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from telethon.sessions import StringSession
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ask_ques = "**☞︎︎︎ ᴄʜᴏᴏsᴇ ᴏɴᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ 𖤍 ✔️ **"
buttons_ques = [
    [
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram"),
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("𝚃𝙴𝙇𝙀𝚃𝙷𝙾𝙽 💻", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
        InlineKeyboardButton("𝚃𝙴𝙇𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="𝙶𝙴𝙽𝚁𝙰𝚃𝙴 𝚂𝙴𝚂𝚎𝙸𝙾𝙽 𖤍", callback_data="generate")
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
    await msg.reply(f"» ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ **{ty}** sᴇssɪᴏɴ ɢᴇɪʀᴀᴛᴏʀ...")
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
            await api_id_msg.reply("**𝖠𝖯𝖨_𝖨𝖳** ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ, sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
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
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇ...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="session", api_id=api_id, api_hash=api_hash, in_memory=True)
    
    try:
        if not is_bot:
            if telethon:
                await client.connect()
                if not await client.is_user_authorized():
                    await client.send_code_request(phone_number)
                    code = await bot.ask(user_id, "» ᴇɴᴛᴇʀ ᴛʜᴇ ᴄᴏᴅᴇ ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ :")
                    if await cancelled(code):
                        return
                    await client.sign_in(phone_number, code.text)
                await msg.reply(f"**💾 𝖲𝙴𝒮𝒮𝒾𝒪𝒩 𝚲𝚨𝚦𝙰𝚃𝙸𝙾𝙽 𝙷𝒶𝓈 𝒷𝑒𝑒𝓃 𝒸𝒽𝑒𝒸𝓀𝑒𝒹 💾**\n\n**𝑆𝑒𝓈𝓈𝒾𝑜𝓃** : `{client.session.save()}`", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            else:
                await client.start(phone_number)
                await msg.reply(f"**💾 𝖲𝙴𝒮𝒮𝒾𝒪𝒩 𝚲𝚨𝚦𝙰𝚳𝙸𝙾𝙽 𝙷𝒶𝓈 𝒷𝑒𝑒𝓃 𝒸𝒽𝑒𝒸𝓀𝑒𝒹 💾**\n\n**𝑆𝑒𝓈𝓈𝒾𝑜𝓃** : `{client.session_str}`", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        else:
            await client.start()
            await msg.reply(f"**💾 𝖲𝙴𝒮𝒮𝒾𝒪𝒩 𝚲𝚨𝚦𝙰𝚳𝙸𝙾𝙽 𝙷𝒶𝓈 𝒷𝑒𝑒𝓃 𝒸𝒽𝑒𝒸𝓀𝑒𝒹 💾**\n\n**𝑆𝑒𝓈𝓈𝒾𝑜𝓃** : `{client.session.save()}`", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
    except ApiIdInvalidError as e:
        await msg.reply(f"**𝖠𝖯𝖨 𝙸𝙳 𝙸𝙽𝙑𝖠𝙻𝙸𝒹**\n\n𝙻𝙴𝒶𝓈𝑒 𝒸𝒽𝑒𝒸𝓀 ʏᴏᴜʳ ᵃᵖⁱ_ⁱᵈ ᵃɢᵃɪɴ. **", quote=True)
        logger.error(f"ApiIdInvalidError: {e}")
    except PhoneNumberInvalidError as e:
        await msg.reply(f"**𝙿𝚑𝑜𝓃𝑒 𝙽𝓊𝓂𝒷𝑒ʳ 𝙸𝙽𝙵𝙰𝙻𝙸𝒹**\n\n𝙻𝙴𝒶𝓈𝑒 𝒸𝒽𝑒𝒸𝓀 ʏᴏᴜʳ 𝒸𝑜𝓃𝓉𝒶𝒸𝓉 𝓃𝓊𝓂𝒷𝑒𝓇 ᵉxᵐᵖˡ𝑒 `+91 95xxxxxxXX`", quote=True)
        logger.error(f"PhoneNumberInvalidError: {e}")
    except PhoneCodeInvalidError as e:
        await msg.reply(f"**𝙿𝚑𝑜𝓃𝑒 𝙲𝑜𝒹𝑒 𝙸𝙽𝙵𝒶𝙻𝙸𝒹**\n\n𝙻𝙴𝒶𝓈𝑒 𝒸𝒽𝑒𝒸𝓀 ʏᴏᴜʳ 𝑐𝑜𝒹𝑒 ᴀɢᴀɪɴ.", quote=True)
        logger.error(f"PhoneCodeInvalidError: {e}")
    except PhoneCodeExpiredError as e:
        await msg.reply(f"**𝙿𝚑𝑜𝓃𝑒 𝙲𝑜𝒹𝑒 𝙴𝚇𝙿𝙸𝚁𝙴𝙳**\n\n𝙻𝙴𝒶𝓈𝑒 ᴅᴜʀɪɴɢ ᴛᴇsᴛᴄᴏᴅᴇ ᴡɪᴛʜᴏᴜᴛ ᴅᴇʟᵁɢᴇ. ᴀʀʟᴇᵂ ᴀɪᴍ ᵃɢᴀɪɴ.", quote=True)
        logger.error(f"PhoneCodeExpiredError: {e}")
    except SessionPasswordNeededError as e:
        await msg.reply(f"**𝙿𝒶𝒮𝒮𝒲𝒪𝒭𝒹 𝙽𝒺𝐸𝒹𝐸𝒟**\n\n𝙻𝙴𝒶𝓈𝑒 𝓈ᴇ𝓃ᴅ 𝓎ᴏᴜʿ𝓈 𝓉ᴏ𝒯𝒶𝒷 ᴅᴜʀɪɴɢ 𝓉ʜᴇ ᴏᴛᴴᴇ𝒶𝓃 ᴇxᵃᴍᴩʟ𝑒 {str(e)}", quote=True)
        logger.error(f"SessionPasswordNeededError: {e}")
    except PasswordHashInvalidError as e:
        await msg.reply(f"**𝙿𝒶𝒮𝒮𝒲𝒪𝒭𝒹 𝙷𝒶𝒮𝒽 𝙸𝙽𝙵𝒶𝙻𝙸𝒹**\n\n𝙻𝙴𝒶𝓈𝑒 𝒸𝒽𝑒𝒸𝓀 ᴘʀᴏᴄᴇss ᴄ𝑜𝓂𝒹 ʀ𝒾𝓉𝑒.", quote=True)
        logger.error(f"PasswordHashInvalidError: {e}")
    except TimeoutError as e:
        await msg.reply("**𝑇𝒾𝑀𝒺𝒪𝑈𝒯**\n\n𝙻𝙴𝒶𝓈𝑒 𝓇ᴇ𝒸ᴇ𝒾𝓋𝑒 𝑒𝓇𝓇𝑜𝓇 ᵒʳ 𝒾𝓃𝓁𝒾𝓃𝑒 𝓉𝑒𝓍𝓉 𝒷𝒶𝒸𝓀 ᵍᵒ 𝒸𝒾𝓇𝒸𝓁𝒾𝒻 𝓌𝒾𝓉ʜ 𝒾𝓃 𝑒𝓍 ᴠ𝒾𝒹𝑒 𝒾𝒹.', quote=True)
        logger.error(f"TimeoutError: {e}")
    except Exception as e:
        await msg.reply("**𝑆ᴏᴍᴇ𝓉ʜ𝒾𝓃𝑔 𝒲𝑅𝒪𝒩𝒢**\n\n𝒸ʷ𝑒 𝓈ᴜʟ𝑙 𝒸ᵉʀ𝒸 𝑒xᵃᴍᵈ ᵃɢᵒ 𝓈𝑒𝓂 𝒷ᵘ𝑇𝓉𝒶𝒽𝓁ᵌ𝒾𝓉𝑒.", quote=True)
        logger.error(f"Exception: {e}")

async def cancelled(message):
    return message.text == "/cancel"

if __name__ == "__main__":
    import asyncio
    from config import API_ID, API_HASH

    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_telegram_bot())
    loop.run_forever()

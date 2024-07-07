from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("Support Channel", url="https://t.me/support_channel")],
        [InlineKeyboardButton("Support Group", url="https://t.me/support_group")],
        [InlineKeyboardButton("Ambil String", callback_data="ambil_string")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply("Welcome! Please choose an option:", reply_markup=reply_markup)

@Client.on_callback_query(filters.regex("ambil_string"))
async def ambil_string(client, callback_query):
    ask_ques = "**☞︎︎︎ ᴄʜᴏᴏsᴇ ᴏɴᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ 𖤍 ✔️ **"
    buttons_ques = [
        [
            InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram"),
            InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram_v2"),
        ],
        [
            InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 💻", callback_data="telethon"),
        ],
        [
            InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
            InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
        ],
    ]
    await callback_query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

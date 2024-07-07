from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

START_MSG = "Halo! Saya adalah bot yang dapat mengambil ID channel/grup dari pesan yang diteruskan."

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start(client, message: Message):
        buttons = [
            [InlineKeyboardButton("Developer", url="https://t.me/SayaKyu")],
            [
                InlineKeyboardButton("Support Channel", url="https://t.me/Alteregonetwork"),
                InlineKeyboardButton("Support Grup", url="https://t.me/Alterego_ID")
            ],
            [InlineKeyboardButton("Ambil String", callback_data="ambil_string")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(START_MSG, reply_markup=reply_markup)

    @app.on_message(filters.command("start") & filters.group)
    async def start_group(client, message: Message):
        await message.reply_text("Halo! Saya adalah bot yang dapat mengambil ID channel/grup dari pesan yang diteruskan.")
    
    @app.on_callback_query(filters.regex("ambil_string"))
    async def string_callback(client, callback_query):
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
        reply_markup = InlineKeyboardMarkup(buttons_ques)
        await callback_query.message.reply(ask_ques, reply_markup=reply_markup)

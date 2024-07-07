from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define the new buttons
buttons = [
    [InlineKeyboardButton("Support Channel", url="https://t.me/support_channel")],
    [InlineKeyboardButton("Support Gryp", url="https://t.me/support_gryp")],
    [InlineKeyboardButton("Ambil String", callback_data="ambil_string")],
]

# Define the start command handler
@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "Welcome to the bot!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback handler for the new "Ambil String" button
@Client.on_callback_query(filters.regex("ambil_string"))
async def ambil_string_callback(client, callback_query):
    await callback_query.message.reply(
        "**☞︎︎︎ ᴄʜᴏᴏsᴇ ᴏɴᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ 𖤍 ✔️ **",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram"),
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram_v2"),
            ],
            [InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 💻", callback_data="telethon")],
            [
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
                InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
            ],
        ])
    )

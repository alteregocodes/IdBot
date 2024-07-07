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
            [InlineKeyboardButton("Ambil String", callback_data="get_string")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(START_MSG, reply_markup=reply_markup)

    @app.on_message(filters.command("start") & filters.group)
    async def start_group(client, message: Message):
        await message.reply_text("Halo! Saya adalah bot yang dapat mengambil ID channel/grup dari pesan yang diteruskan.")

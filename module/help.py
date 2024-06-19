# module/help.py

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import HELP_MSG

async def help(client, message: Message):
    buttons = [
        [InlineKeyboardButton("Start", callback_data="help_start")],
        [InlineKeyboardButton("Update", callback_data="help_update")],
        [InlineKeyboardButton("Carbon", callback_data="help_carbon")],
        [InlineKeyboardButton("Get ID", callback_data="help_getid")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(HELP_MSG, reply_markup=reply_markup)

async def help_callback(client, callback_query):
    data = callback_query.data
    if data == "help_start":
        await callback_query.message.edit_text("Perintah /start digunakan untuk memulai bot.")
    elif data == "help_update":
        await callback_query.message.edit_text("Perintah /update digunakan untuk memperbarui bot. Hanya dapat digunakan oleh owner.")
    elif data == "help_carbon":
        await callback_query.message.edit_text("Perintah /carbon digunakan untuk membuat gambar kode. Gunakan dengan membalas pesan berisi kode.")
    elif data == "help_getid":
        await callback_query.message.edit_text("Perintah /id digunakan untuk mendapatkan ID pengguna atau grup.")

def init(app):
    app.on_message(filters.command("help") & filters.private)(help)
    app.on_callback_query(filters.create(lambda _, __, query: query.data.startswith("help_")))(help_callback)

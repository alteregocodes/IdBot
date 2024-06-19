# module/help.py

from pyrogram.types import Message
from pyrogram import Client, InlineKeyboardButton, InlineKeyboardMarkup
from module import update, start, carbon, getid

async def help_command(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("Update", callback_data="help_update"),
            InlineKeyboardButton("Start", callback_data="help_start"),
            InlineKeyboardButton("Carbon", callback_data="help_carbon"),
        ],
        [
            InlineKeyboardButton("Get ID", callback_data="help_getid"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("Pilih modul untuk melihat keterangan perintah:", reply_markup=reply_markup)

async def help_update(client: Client, message: Message):
    await message.reply_text("ℹ️ Update:\n\nPerintah untuk memperbarui dan memulai ulang bot.", disable_web_page_preview=True)

async def help_start(client: Client, message: Message):
    await message.reply_text("ℹ️ Start:\n\nPerintah untuk memulai bot dengan tombol Developer, Support Channel, dan Support Grup.", disable_web_page_preview=True)

async def help_carbon(client: Client, message: Message):
    await message.reply_text("ℹ️ Carbon:\n\nBalas pesan dengan kode untuk membuat gambar Carbon dari kode tersebut.", disable_web_page_preview=True)

async def help_getid(client: Client, message: Message):
    await message.reply_text("ℹ️ Get ID:\n\nPerintah untuk mendapatkan ID Anda atau ID grup/channel dari pesan yang diteruskan.", disable_web_page_preview=True)

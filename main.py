import os
import sys
import subprocess
import asyncio
import aiohttp
from datetime import datetime
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatMemberUpdated
from config import *
from pyrogram.errors import PeerIdInvalid
from module.tts import *
import json

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

aiosession = None

async def init_aiosession():
    global aiosession
    if aiosession is None:
        aiosession = aiohttp.ClientSession()

async def make_carbon(code):
    await init_aiosession()
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(message.command) != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply("⚙️ Memproses . . .")
    carbon = await make_carbon(text)
    await ex.edit("🔼 Mengunggah . . .")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"<b>Carbonised by:</b> {client.me.mention}",
        ),
    )
    carbon.close()

async def welcome_new_member(client, chat_member_updated: ChatMemberUpdated):
    new_member = chat_member_updated.new_chat_member
    chat_id = chat_member_updated.chat.id
    group_name = chat_member_updated.chat.title
    
    fullname = new_member.user.first_name + " " + (new_member.user.last_name or "")
    username = new_member.user.username or "-"
    user_id = new_member.user.id
    join_date = datetime.now().strftime("%d %B %Y")
    
    text = (
        f"Nama: {fullname}\n"
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"Tanggal Bergabung: {join_date}\n\n"
        f"Selamat datang di {group_name}, semoga betah!"
    )
    
    carbon_image = await make_carbon(text)
    
    await client.send_photo(
        chat_id,
        photo=carbon_image,
        caption=f"Selamat datang @{username} di {group_name}, semoga betah!",
    )
    
    carbon_image.close()

def get_lang_code(user_id):
    try:
        with open('language_preferences.json', 'r') as f:
            lang_preferences = json.load(f)
        return lang_preferences.get(str(user_id), 'en')
    except FileNotFoundError:
        return 'en'

def set_lang_preference(user_id, lang_code):
    try:
        with open('language_preferences.json', 'r') as f:
            lang_preferences = json.load(f)
    except FileNotFoundError:
        lang_preferences = {}
    
    lang_preferences[str(user_id)] = lang_code
    
    with open('language_preferences.json', 'w') as f:
        json.dump(lang_preferences, f)

def get_lang_name(lang_code):
    for lang, code in LANG_CODES.items():
        if code == lang_code:
            return lang
    return "Unknown"

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    buttons = [
        [InlineKeyboardButton("Developer", url="https://t.me/SayaKyu")],
        [
            InlineKeyboardButton("Support Channel", url="https://t.me/Alteregonetwork"),
            InlineKeyboardButton("Support Grup", url="https://t.me/Alterego_ID")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(START_MSG, reply_markup=reply_markup)

@app.on_message(filters.forwarded)
async def get_forwarded_info(client, message: Message):
    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
        chat_id_formatted = f"<code>-{abs(chat_id)}</code>" if chat_id < 0 else str(chat_id)
        await message.reply_text(f"ID Channel/Grup: {chat_id_formatted}")
    else:
        await message.reply_text("Pesan ini tidak berasal dari channel atau grup.")

@app.on_message(filters.command("id"))
async def get_user_id(client, message: Message):
    user_id = message.from_user.id
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        text = f"ID Anda adalah: <code>{user_id}</code>\nID Grup ini adalah: <code>{chat_id}</code>"
    else:
        text = f"ID Anda adalah: <code>{user_id}</code>"
    
    await message.reply_text(text)

@app.on_message(filters.command("carbon") & (filters.group | filters.private))
async def carbon_command(client, message: Message):
    await carbon_func(client, message)

# Handler untuk perintah TTS (/tts)
@app.on_message(filters.command("tts") & filters.private)
async def tts_command(client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply("Silakan berikan teks yang ingin diubah menjadi suara.")
        return
    
    text = message.reply_to_message.text if message.reply_to_message else message.text.split(None, 1)[1]
    language = get_lang_code(message.from_user.id)
    output_file = text_to_speech(text, language)
    
    try:
        # Kirim suara dengan membalas/mereply ke pesan asal
        await client.send_voice(
            chat_id=message.chat.id,
            voice=output_file,
            reply_to_message_id=message.message_id
        )
    except Exception as e:
        await message.reply_text(f"Error: {e}")
    finally:
        remove_output_file(output_file)

# Handler untuk callback setting bahasa TTS
@app.on_callback_query(filters.regex(r"^set_lang_"))
async def set_tts_language_callback(client, callback_query: CallbackQuery):
    language_code = callback_query.data.split("_")[2]
    set_lang_preference(callback_query.from_user.id, language_code)
    language_name = get_lang_name(language_code)
    
    # Tampilkan alert bahwa bahasa TTS telah diatur
    await callback_query.answer(f"Bahasa TTS diatur ke {language_name}", show_alert=True)
    
    # Hapus pilihan bahasa dari keyboard inline
    await callback_query.message.edit_reply_markup(reply_markup=None)

    try:
        # Hapus pesan pilihan bahasa yang dikirim oleh bot
        await callback_query.message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

@app.on_callback_query(filters.regex(r"^set_lang_"))
async def set_tts_language_callback(client, callback_query: CallbackQuery):
    language_code = callback_query.data.split("_")[2]
    set_lang_preference(callback_query.from_user.id, language_code)
    language_name = get_lang_name(language_code)
    
    await callback_query.answer(f"Bahasa TTS diatur ke {language_name}", show_alert=True)
    
    await callback_query.message.delete_reply_markup()

    try:
        await callback_query.message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

@app.on_message(filters.command("start") & filters.group)
async def start_group(client, message: Message):
    await message.reply_text("Halo! Saya adalah bot yang dapat mengambil ID channel/grup dari pesan yang diteruskan.")

@app.on_chat_member_updated()
async def welcome_new_members(client, chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member and chat_member_updated.new_chat_member.status == "member":
        await welcome_new_member(client, chat_member_updated)

import atexit

@atexit.register
def close_aiohttp_session():
    if aiosession:
        asyncio.run(aiosession.close())

print("Bot telah dijalankan, apabila butuh bantuan chat @SayaKyu\nManage by @AlteregoNetwork")

app.run()

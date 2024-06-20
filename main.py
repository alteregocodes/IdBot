import os
import sys
import subprocess
import requests
import aiohttp
import asyncio
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQueryResultArticle, InputTextMessageContent
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_IDS, START_MSG, UPDATE_LOG_FILE
from pyrogram.errors import PeerIdInvalid
from gtts import gTTS
from gpytranslate import Translator

app = Client("channel_id_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Inisialisasi sesi aiohttp.ClientSession
aiosession = None

# Daftar kode bahasa untuk Google TTS
LANG_CODES = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Japanese": "ja",
    "Korean": "ko",
    "Sundanese": "su",
    "Thai": "th",
    "Filipino": "fil",
    # Tambahkan bahasa lain sesuai kebutuhan
}

# Default bahasa TTS
DEFAULT_LANG = "en"  # Bahasa Inggris sebagai default

# Inisialisasi translator untuk gpytranslate
translator = Translator()

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

# Handler untuk memulai bot
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    # Periksa apakah ada file log pembaruan
    if os.path.exists(UPDATE_LOG_FILE):
        with open(UPDATE_LOG_FILE, "r") as f:
            update_log = f.read()
        # Kirim log pembaruan ke semua owner
        for owner_id in OWNER_IDS:
            try:
                await client.send_message(owner_id, f"Bot telah berhasil diperbarui:\n\n{update_log}")
            except PeerIdInvalid:
                print(f"Failed to send message to {owner_id}: PeerIdInvalid")
            except Exception as e:
                print(f"Failed to send message to {owner_id}: {e}")
        # Hapus file log setelah dikirim
        os.remove(UPDATE_LOG_FILE)
    
    buttons = [
        [InlineKeyboardButton("Developer", url="https://t.me/SayaKyu")],
        [
            InlineKeyboardButton("Support Channel", url="https://t.me/Alteregonetwork"),
            InlineKeyboardButton("Support Grup", url="https://t.me/Alterego_ID")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(START_MSG, reply_markup=reply_markup)

# Handler untuk pesan diteruskan
@app.on_message(filters.forwarded)
async def get_forwarded_info(client, message: Message):
    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
        chat_id_formatted = f"<code>-{abs(chat_id)}</code>" if chat_id < 0 else str(chat_id)
        await message.reply_text(f"ID Channel/Grup: {chat_id_formatted}")
    else:
        await message.reply_text("Pesan ini tidak berasal dari channel atau grup.")

# Handler untuk update bot
@app.on_message(filters.command("update") & filters.user(OWNER_IDS))
async def update(client, message: Message):
    await message.reply_text("Bot akan memperbarui dan memulai ulang...")
    # Hentikan bot
    await app.stop()
    # Lakukan git pull dan simpan hasilnya ke file log sementara
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    with open(UPDATE_LOG_FILE, "w") as f:
        f.write(result.stdout + "\n" + result.stderr)
    # Jalankan ulang bot dengan perintah bash 'start'
    os.system("bash start")
    sys.exit(0)

# Handler untuk mendapatkan ID pengguna
@app.on_message(filters.command("id"))
async def get_user_id(client, message: Message):
    user_id = message.from_user.id
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        await message.reply_text(f"ID Anda adalah: <code>{user_id}</code>\nID Grup ini adalah: <code>{chat_id}</code>")
    else:
        await message.reply_text(f"ID Anda adalah: <code>{user_id}</code>")

# Handler untuk perintah carbon
@app.on_message(filters.command("carbon") & filters.private)
async def carbon(client, message: Message):
    await carbon_func(client, message)

# Handler untuk perintah TTS (/tts)
@app.on_message(filters.command("tts") & filters.private)
async def tts_command(client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply("Silakan berikan teks yang ingin diubah menjadi suara.")
        return
    text = message.reply_to_message.text if message.reply_to_message else message.text.split(None, 1)[1]
    language = LANG_CODES.get(message.from_user.id, DEFAULT_LANG)
    tts = gTTS(text, lang=language)
    tts.save("output.ogg")
    try:
        await client.send_voice(message.chat.id, voice="output.ogg", reply_to_message_id=message.message_id)
        await message.delete()
    except Exception as e:
        await message.reply_text(f"Error: {e}")
    finally:
        os.remove("output.ogg")

# Handler untuk perintah setting bahasa TTS (/bahasatts)
@app.on_message(filters.command("bahasatts") & filters.private)
async def set_tts_language(client, message: Message):
    buttons = []
    for lang, code in LANG_CODES.items():
        buttons.append([InlineKeyboardButton(lang, callback_data=f"set_lang_{code}")])
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("Pilih bahasa untuk TTS:", reply_markup=reply_markup)

# Handler untuk callback setting bahasa TTS
@app.on_callback_query(filters.regex(r"^set_lang_"))
async def set_tts_language_callback(client, callback_query: CallbackQuery):
    language_code = callback_query.data.split("_")[2]
    client._translate[client.me.id] = {"negara": language_code}
    await callback_query.answer(f"Bahasa TTS diatur ke {language_code}")

# Tambahkan penanganan untuk menutup sesi saat aplikasi berhenti
import atexit

@atexit.register
def close_aiohttp_session():
    if aiosession:
        asyncio.run(aiosession.close())

if __name__ == "__main__":
    print("Bot telah dijalankan, apabila butuh bantuan chat @SayaKyu")
    print("Manage by @AlteregoNetwork")
    app.run()

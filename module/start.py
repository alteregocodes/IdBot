from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# URL untuk video GIF
GIF_URL = "https://telegra.ph/file/35cf8363e5b42adf1ca94.mp4"

def register_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start(client, message):
        await client.send_animation(
            chat_id=message.chat.id,
            animation=GIF_URL,
            caption="Selamat datang di bot kami!",
            reply_markup=get_main_buttons()
        )

    @app.on_callback_query(filters.regex("ambil_string"))
    async def handle_ambil_string(client, callback_query):
        await client.send_animation(
            chat_id=callback_query.message.chat.id,
            animation=GIF_URL,
            caption="**» Pilih Jenis String yang Ingin Dibuat **",
            reply_markup=get_string_type_buttons()
        )

    @app.on_callback_query(filters.regex("help"))
    async def handle_help(client, callback_query):
        help_message = """
**Daftar Perintah:**

/tts <teks> - Mengubah teks menjadi suara dengan bahasa yang dipilih.
/bahasatts - Mengatur bahasa untuk Text-to-Speech (TTS).
/id - Menampilkan ID Anda dan ID grup (jika di grup).
/carbon <kode> - Membuat gambar "carbon" dari kode yang diberikan.
/song <judul lagu/tautan YouTube> - Mengunduh dan mengirim file audio dari lagu atau tautan YouTube.
/vsong <judul video/tautan YouTube> - Mengunduh dan mengirim file video dari video atau tautan YouTube.

**Cara Mendapatkan ID Channel/Grup:**
Forward pesan dari channel/grup ke bot ini, atau gunakan perintah /id jika di dalamnya.

**Cara Mendapatkan String Session Telegram:**
Untuk mendapatkan string session Telegram Anda, Anda perlu membuatnya menggunakan salah satu opsi di bawah menu "Ambil String" yang telah kami sediakan sebelumnya. Ikuti petunjuk untuk memasukkan kredensial API Anda (API_ID, API_HASH), dan opsional nomor telepon atau token bot Anda. Bot akan memandu Anda melalui proses untuk menghasilkan dan mendapatkan string session Anda.

Klik tombol "Kembali" untuk kembali ke pesan sebelumnya.
"""
        await callback_query.message.edit(help_message, reply_markup=get_back_button())

    @app.on_callback_query(filters.regex("back_to_start"))
    async def handle_back_to_start(client, callback_query):
        await client.send_animation(
            chat_id=callback_query.message.chat.id,
            animation=GIF_URL,
            caption="Selamat datang di bot kami!",
            reply_markup=get_main_buttons()
        )

def get_main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Support Channel", url="https://t.me/supportchannel")],
        [InlineKeyboardButton("Ambil String", callback_data="ambil_string"),
         InlineKeyboardButton("Bantuan", callback_data="help")],
    ])

def get_string_type_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram"),
            InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram_v2"),
        ],
        [InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 💻", callback_data="telethon")],
        [
            InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
            InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
        ],
        [get_back_button()]
    ])

def get_back_button():
    return InlineKeyboardButton("Kembali", callback_data="back_to_start")

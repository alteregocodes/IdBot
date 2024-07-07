from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo

def register_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start(client, message):
        buttons = [
            [InlineKeyboardButton("Support Channel", url="https://t.me/supportchannel")],
            [InlineKeyboardButton("Bantuan", callback_data="help"), InlineKeyboardButton("Module", callback_data="module")],
            [InlineKeyboardButton("Ambil String", callback_data="ambil_string")],
        ]
        video_url = "https://telegra.ph/file/35cf8363e5b42adf1ca94.mp4"
        caption = "Selamat datang di bot kami!"

        await client.send_video(
            chat_id=message.chat.id,
            video=video_url,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    @app.on_callback_query(filters.regex("ambil_string"))
    async def handle_ambil_string(client, callback_query):
        ask_ques = "**» Pilih Jenis String yang Ingin Dibuat **"
        buttons_ques = [
            [
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram"),
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram_v2"),
            ],
            [InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 💻", callback_data="telethon")],
            [
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
                InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
            ],
            [InlineKeyboardButton("Kembali", callback_data="back_to_start")],
        ]
        await callback_query.message.edit(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

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
        back_button = InlineKeyboardButton("Kembali", callback_data="back_to_start")
        await callback_query.message.edit(help_message, reply_markup=InlineKeyboardMarkup([[back_button]]))

    @app.on_callback_query(filters.regex("module"))
    async def handle_module(client, callback_query):
        module_ques = "**» Pilih Module yang Ingin Anda Gunakan **"
        buttons_module = [
            [InlineKeyboardButton("TTS", callback_data="module_tts"), InlineKeyboardButton("Carbon", callback_data="module_carbon")],
            [InlineKeyboardButton("Song", callback_data="module_song"), InlineKeyboardButton("vSong", callback_data="module_vsong")],
            [InlineKeyboardButton("Kembali", callback_data="back_to_start")],
        ]
        await callback_query.message.edit(module_ques, reply_markup=InlineKeyboardMarkup(buttons_module))

    @app.on_callback_query(filters.regex("^module_"))
    async def handle_specific_module(client, callback_query):
        module = callback_query.data.split("_")[1]
        module_messages = {
            "tts": """
**Cara Menggunakan Module TTS:**
/tts <teks> - Mengubah teks menjadi suara dengan bahasa yang dipilih.
/bahasatts - Mengatur bahasa untuk Text-to-Speech (TTS).
""",
            "carbon": """
**Cara Menggunakan Module Carbon:**
/carbon <kode> - Membuat gambar "carbon" dari kode yang diberikan.
""",
            "song": """
**Cara Menggunakan Module Song:**
/song <judul lagu/tautan YouTube> - Mengunduh dan mengirim file audio dari lagu atau tautan YouTube.
""",
            "vsong": """
**Cara Menggunakan Module vSong:**
/vsong <judul video/tautan YouTube> - Mengunduh dan mengirim file video dari video atau tautan YouTube.
"""
        }
        module_message = module_messages.get(module, "Module tidak ditemukan.")
        back_button = InlineKeyboardButton("Kembali", callback_data="module")
        await callback_query.message.edit(module_message, reply_markup=InlineKeyboardMarkup([[back_button]]))

    @app.on_callback_query(filters.regex("back_to_start"))
    async def handle_back_to_start(client, callback_query):
        buttons = [
            [InlineKeyboardButton("Support Channel", url="https://t.me/supportchannel")],
            [InlineKeyboardButton("Bantuan", callback_data="help"), InlineKeyboardButton("Module", callback_data="module")],
            [InlineKeyboardButton("Ambil String", callback_data="ambil_string")],
        ]
        video_url = "https://telegra.ph/file/35cf8363e5b42adf1ca94.mp4"
        caption = "Selamat datang di bot kami!"

        await callback_query.message.edit_media(
            media=InputMediaVideo(media=video_url, caption=caption),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# module/help.py

from pyrogram import Client, filters
from pyrogram.types import Message

HELP_TEXT = """
Daftar Perintah yang Tersedia:

/tts <teks> - Mengubah teks menjadi suara dengan bahasa yang dipilih.
/bahasatts - Mengatur bahasa untuk Text-to-Speech (TTS).
/id - Menampilkan ID Anda dan ID grup (jika di grup).
/carbon <kode> - Membuat gambar "carbon" dari kode yang diberikan.
Cara Mendapatkan ID Channel/Grup:
Forward pesan dari channel/grup ke bot ini, atau gunakan perintah /id jika di dalamnya.
"""

def register_handlers(app):
    @app.on_message(filters.command("help"))
    async def help_command(client, message: Message):
        await message.reply_text(HELP_TEXT, parse_mode="markdownv2")

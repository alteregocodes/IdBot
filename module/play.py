# module/play.py

import os
import yt_dlp as youtube_dl
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from collections import deque
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Folder untuk menyimpan sementara file audio
os.makedirs("os", exist_ok=True)

def download_audio(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'os/%(title)s.%(ext)s',
        'default_search': 'ytsearch',
        'quiet': True,
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=True)
        file_path = ydl.prepare_filename(info_dict)
        base, ext = os.path.splitext(file_path)
        return f"{base}.mp3"

# Inisialisasi PyTgCalls
pytgcalls = None
audio_queue = deque()

def register_handlers(app: Client):
    global pytgcalls
    pytgcalls = PyTgCalls(app)

    @app.on_message(filters.command("play"))
    async def play_audio(client, message: Message):
        query = " ".join(message.command[1:])
        if not query:
            await message.reply_text("Harap berikan judul lagu atau tautan YouTube.")
            return
        
        await message.reply_text("Sedang mendownload audio...")
        
        try:
            audio_file = download_audio(query)
            audio_queue.append(audio_file)
            await message.reply_text(f"Lagu '{query}' ditambahkan ke antrian.")
            if len(audio_queue) == 1:
                await start_playing(message.chat.id)
        except Exception as e:
            logger.error(f"Terjadi kesalahan: {e}")
            await message.reply_text(f"Terjadi kesalahan: {e}")

    async def start_playing(chat_id):
        if audio_queue:
            current_audio = audio_queue[0]
            await pytgcalls.join_group_call(
                chat_id,
                AudioPiped(current_audio, HighQualityAudio()),
                stream_type="local"
            )

    @pytgcalls.on_stream_end()
    async def on_stream_end_handler(update: Update):
        if audio_queue:
            os.remove(audio_queue.popleft())
            if audio_queue:
                chat_id = update.chat_id
                await start_playing(chat_id)

    pytgcalls.start()

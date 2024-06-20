from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp as youtube_dl
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Folder untuk menyimpan sementara file audio
os.makedirs("downloads", exist_ok=True)

async def download_progress_hook(d, message):
    if d['status'] == 'downloading':
        percent = d['_percent_str'].strip()
        await message.edit(f"Sedang mendownload... {percent}")
    elif d['status'] == 'finished':
        await message.edit("Download selesai, sedang memproses...")

def register_handlers(app):
    @app.on_message(filters.command("song"))
    async def download_audio(client, message: Message):
        query = " ".join(message.command[1:])
        if not query:
            await message.reply_text("Harap berikan judul lagu atau tautan YouTube.")
            return
        
        progress_message = await message.reply_text("Sedang mendownload audio...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'default_search': 'ytsearch',
            'quiet': True,
            'noplaylist': True,
            'progress_hooks': [lambda d: client.loop.create_task(download_progress_hook(d, progress_message))],
        }

        try:
            # Menyimpan daftar file yang ada sebelum unduhan
            files_before = set(os.listdir("downloads"))

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(query, download=True)
            
            # Menemukan file baru yang diunduh
            files_after = set(os.listdir("downloads"))
            new_files = files_after - files_before
            new_file = list(new_files)[0] if new_files else None

            if new_file:
                audio_file_path = os.path.join("downloads", new_file)
                logger.info(f"Newly downloaded file: {audio_file_path}")
                await progress_message.edit("Pengunduhan selesai. Mengirim audio...")
                await message.reply_audio(audio_file_path, title=info_dict.get('title', 'Unknown'), performer=info_dict.get('uploader', 'Unknown'))
                os.remove(audio_file_path)
            else:
                await progress_message.edit("File audio tidak ditemukan setelah diunduh.")
                logger.error("File audio tidak ditemukan setelah diunduh.")
        except Exception as e:
            logger.error(f"Terjadi kesalahan: {e}")
            await progress_message.edit(f"Terjadi kesalahan: {e}")

    @app.on_message(filters.command("vsong"))
    async def download_video(client, message: Message):
        query = " ".join(message.command[1:])
        if not query:
            await message.reply_text("Harap berikan judul video atau tautan YouTube.")
            return
        
        progress_message = await message.reply_text("Sedang mendownload video...")
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'default_search': 'ytsearch',
            'quiet': True,
            'noplaylist': True,
            'progress_hooks': [lambda d: client.loop.create_task(download_progress_hook(d, progress_message))],
        }

        try:
            # Menyimpan daftar file yang ada sebelum unduhan
            files_before = set(os.listdir("downloads"))

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(query, download=True)

            # Menemukan file baru yang diunduh
            files_after = set(os.listdir("downloads"))
            new_files = files_after - files_before
            new_file = list(new_files)[0] if new_files else None

            if new_file:
                video_file_path = os.path.join("downloads", new_file)
                logger.info(f"Newly downloaded video file: {video_file_path}")
                await progress_message.edit("Pengunduhan selesai. Mengirim video...")
                await message.reply_video(video_file_path, caption=info_dict.get('title', 'Unknown'))
                os.remove(video_file_path)
            else:
                await progress_message.edit("File video tidak ditemukan setelah diunduh.")
                logger.error("File video tidak ditemukan setelah diunduh.")
        except Exception as e:
            logger.error(f"Terjadi kesalahan: {e}")
            await progress_message.edit(f"Terjadi kesalahan: {e}")

# Panggil register_handlers dalam __init__.py
def init_pytgcalls(app):
    from pytgcalls import PyTgCalls
    from pytgcalls.types import Update
    from pytgcalls.types.input_stream import AudioPiped
    from pytgcalls.types.input_stream.quality import HighQualityAudio
    from collections import deque

    pytgcalls = PyTgCalls(app)
    audio_queue = deque()

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

    return pytgcalls, audio_queue


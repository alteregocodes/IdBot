from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp as youtube_dl
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_handlers(app):
    @app.on_message(filters.command("song"))
    async def download_audio(client, message: Message):
        query = " ".join(message.command[1:])
        if not query:
            await message.reply_text("Harap berikan judul lagu atau tautan YouTube.")
            return
        
        await message.reply_text("Sedang mendownload audio...")
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
                await message.reply_audio(audio_file_path, title=info_dict.get('title', 'Unknown'), performer=info_dict.get('uploader', 'Unknown'))
                os.remove(audio_file_path)
            else:
                await message.reply_text("File audio tidak ditemukan setelah diunduh.")
                logger.error("File audio tidak ditemukan setelah diunduh.")
        except Exception as e:
            logger.error(f"Terjadi kesalahan: {e}")
            await message.reply_text(f"Terjadi kesalahan: {e}")

    @app.on_message(filters.command("vsong"))
    async def download_video(client, message: Message):
        query = " ".join(message.command[1:])
        if not query:
            await message.reply_text("Harap berikan judul video atau tautan YouTube.")
            return
        
        await message.reply_text("Sedang mendownload video...")
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'default_search': 'ytsearch',
            'quiet': True,
            'noplaylist': True,
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
                await message.reply_video(video_file_path, caption=info_dict.get('title', 'Unknown'))
                os.remove(video_file_path)
            else:
                await message.reply_text("File video tidak ditemukan setelah diunduh.")
                logger.error("File video tidak ditemukan setelah diunduh.")
        except Exception as e:
            logger.error(f"Terjadi kesalahan: {e}")
            await message.reply_text(f"Terjadi kesalahan: {e}")

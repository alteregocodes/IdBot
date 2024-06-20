from pyrogram import Client, filters
from pyrogram.types import Message
import youtube_dl
import os

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
            'default_search': 'ytsearch',  # Tambahkan default_search
            'quiet': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(query, download=True)
                audio_file = ydl.prepare_filename(info_dict)
                os.rename(audio_file, audio_file + ".mp3")
                audio_file += ".mp3"
                
                await message.reply_audio(audio_file, title=info_dict.get('title', 'Unknown'), performer=info_dict.get('uploader', 'Unknown'))
                os.remove(audio_file)
        except Exception as e:
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
            'default_search': 'ytsearch',  # Tambahkan default_search
            'quiet': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(query, download=True)
                video_file = ydl.prepare_filename(info_dict)
                
                await message.reply_video(video_file, caption=info_dict.get('title', 'Unknown'))
                os.remove(video_file)
        except Exception as e:
            await message.reply_text(f"Terjadi kesalahan: {e}")

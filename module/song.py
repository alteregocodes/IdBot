from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp as youtube_dl
import os
import time

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
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(query, download=True)
                base, ext = os.path.splitext(ydl.prepare_filename(info_dict))
                audio_file = f"{base}.mp3"
                
                # Verifikasi file ada dan menunggu file selesai
                time.sleep(1)
                if os.path.exists(audio_file):
                    await message.reply_audio(audio_file, title=info_dict.get('title', 'Unknown'), performer=info_dict.get('uploader', 'Unknown'))
                    os.remove(audio_file)
                else:
                    await message.reply_text("File audio tidak ditemukan setelah diunduh.")
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
            'default_search': 'ytsearch',
            'quiet': True,
            'noplaylist': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(query, download=True)
                video_file = ydl.prepare_filename(info_dict)
                
                # Verifikasi file ada dan menunggu file selesai
                time.sleep(1)
                if os.path.exists(video_file):
                    await message.reply_video(video_file, caption=info_dict.get('title', 'Unknown'))
                    os.remove(video_file)
                else:
                    await message.reply_text("File video tidak ditemukan setelah diunduh.")
        except Exception as e:
            await message.reply_text(f"Terjadi kesalahan: {e}")

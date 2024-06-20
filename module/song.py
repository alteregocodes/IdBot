# module/song.py

import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import yt_dlp

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download audio from YouTube
async def download_audio(update: Message, context):
    query = ' '.join(context.command[1:])
    if not query:
        await update.reply_text('Silakan berikan judul lagu atau link YouTube untuk mengunduh audio.')
        return

    await update.reply_text('Sedang mencari dan mengunduh audio, harap tunggu... ⏳')

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,  # Suppress console output
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(query, download=True)
                file_title = ydl.prepare_filename(info_dict)
            except yt_dlp.DownloadError as e:
                logger.error(f'Failed to download audio: {e}')
                await update.reply_text('Gagal mengunduh audio. Periksa judul atau link dan coba lagi.')
                return

        # Check if the file exists and send it
        if file_title and os.path.exists(file_title):
            await update.reply_audio(audio=file_title)
            logger.info(f'Audio {file_title} dikirim ke pengguna.')
        else:
            logger.error(f'File not found after download: {file_title}')
            await update.reply_text('Terjadi kesalahan saat memproses judul atau link. Silakan coba lagi.')

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        await update.reply_text('Terjadi kesalahan saat memproses judul atau link yang Anda berikan.')

# Function to download video from YouTube
async def download_video(update: Message, context):
    query = ' '.join(context.command[1:])
    if not query:
        await update.reply_text('Silakan berikan judul video atau link YouTube untuk mengunduh video.')
        return

    await update.reply_text('Sedang mencari dan mengunduh video, harap tunggu... ⏳')

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,  # Suppress console output
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(query, download=True)
                file_title = ydl.prepare_filename(info_dict)
            except yt_dlp.DownloadError as e:
                logger.error(f'Failed to download video: {e}')
                await update.reply_text('Gagal mengunduh video. Periksa judul atau link dan coba lagi.')
                return

        # Check if the file exists and send it
        if file_title and os.path.exists(file_title):
            await update.reply_video(video=file_title)
            logger.info(f'Video {file_title} dikirim ke pengguna.')
        else:
            logger.error(f'File not found after download: {file_title}')
            await update.reply_text('Terjadi kesalahan saat memproses judul atau link. Silakan coba lagi.')

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        await update.reply_text('Terjadi kesalahan saat memproses judul atau link yang Anda berikan.')

# Function to register handlers with Pyrogram
def register_handlers(app: Client):
    @app.on_message(filters.command("song") & filters.private)
    async def handle_song_command(_, message: Message):
        await download_audio(message, message)

    @app.on_message(filters.command("vsong") & filters.private)
    async def handle_vsong_command(_, message: Message):
        await download_video(message, message)

    @app.on_message(filters.private)
    async def handle_text_message(_, message: Message):
        if message.text.startswith('/song') or message.text.startswith('/vsong'):
            return  # Avoid triggering on /song or /vsong commands again
        
        query = message.text.strip()
        if query:
            if query.startswith(('http://', 'https://')):
                await download_video(message, message)
            else:
                await download_audio(message, message)

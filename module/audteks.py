# module/audteks.py

import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import speech_recognition as sr
from pydub import AudioSegment
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="id-ID")  # Speech recognition using Google Web Speech API
    except sr.UnknownValueError:
        text = "Tidak dapat mengenali audio"
    except sr.RequestError as e:
        text = f"Terjadi kesalahan pada layanan pengenalan suara: {e}"
    return text

def register_handlers(app):
    @app.on_message(filters.command("uteks") & filters.reply)
    async def audio_to_text(client, message: Message):
        if not (message.reply_to_message.voice or message.reply_to_message.audio):
            await message.reply_text("Harap balas pesan ini dengan file audio atau pesan suara yang ingin diubah menjadi teks.")
            return
        
        # Download audio file or voice message
        audio_file = await message.reply_to_message.download()
        logger.info(f"Audio file downloaded to {audio_file}")

        # Convert audio to WAV format (required for speech recognition)
        try:
            audio = AudioSegment.from_file(audio_file)
            audio = audio.set_frame_rate(16000).set_channels(1)  # Adjust format if needed
            temp_audio_path = "converted_audio.wav"
            audio.export(temp_audio_path, format="wav")
            logger.info(f"Audio converted to WAV format at {temp_audio_path}")

            # Transcribe audio to text
            await message.reply_text("Sedang mentranskripsi audio, harap tunggu...")
            text = transcribe_audio(temp_audio_path)
            await message.reply_text(f"Hasil transkripsi:\n\n{text}")
        except Exception as e:
            logger.error(f"Terjadi kesalahan: {e}")
            await message.reply_text(f"Terjadi kesalahan saat memproses audio: {e}")
            logger.error(traceback.format_exc())
        finally:
            # Clean up: delete downloaded and temporary files
            if os.path.exists(audio_file):
                os.remove(audio_file)
                logger.info(f"Deleted temporary file {audio_file}")
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                logger.info(f"Deleted temporary file {temp_audio_path}")

# Ensure to handle any exceptions and log them appropriately


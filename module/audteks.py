# module/audteks.py

import os
from pyrogram import Client, filters
from pyrogram.types import Message
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        # Menggunakan Google Web Speech API secara gratis
        text = recognizer.recognize_google(audio, language="id-ID")  # Ganti kode bahasa jika perlu
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
        
        # Mengunduh file audio atau pesan suara
        audio_file = await message.reply_to_message.download()
        audio = AudioSegment.from_file(audio_file)
        audio = audio.set_frame_rate(16000).set_channels(1)  # Konversi ke format yang sesuai
        
        temp_audio_path = "converted_audio.wav"
        audio.export(temp_audio_path, format="wav")
        
        try:
            await message.reply_text("Sedang mentranskripsi audio, harap tunggu...")
            text = transcribe_audio(temp_audio_path)
            await message.reply_text(f"Hasil transkripsi:\n\n{text}")
        except Exception as e:
            await message.reply_text(f"Terjadi kesalahan: {e}")
        finally:
            # Hapus file yang diunduh dan file sementara
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

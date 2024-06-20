import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import speech_recognition as sr
import subprocess

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Temporary audio file storage
TEMP_AUDIO_PATH = "downloads/audio.ogg"

def register_handlers(app):
    @app.on_message(filters.command("uteks"))
    async def audio_to_text(client, message: Message):
        if message.reply_to_message and hasattr(message.reply_to_message, 'voice'):
            try:
                # Download the voice message
                voice_msg = await client.get_messages(message.chat.id, message_ids=message.reply_to_message.message_id)
                await voice_msg.download(file_name=TEMP_AUDIO_PATH)
                logger.info(f"Audio file downloaded to {TEMP_AUDIO_PATH}")

                # Convert audio to WAV format
                wav_file_path = convert_to_wav(TEMP_AUDIO_PATH)
                if not wav_file_path:
                    await message.reply_text("Gagal mengonversi audio ke format WAV.")
                    return

                # Transcribe audio to text
                transcript = transcribe_audio(wav_file_path)
                if transcript:
                    await message.reply_text(f"Hasil transkripsi:\n\n{transcript}")
                else:
                    await message.reply_text("Tidak dapat mengenali audio.")
            except Exception as e:
                logger.error(f"Error during audio to text conversion: {e}")
                await message.reply_text("Terjadi kesalahan saat mengonversi audio ke teks.")

            finally:
                # Clean up temporary files
                cleanup_temp_files()
                logger.info("Temporary files deleted.")
        else:
            await message.reply_text("Harap balas pesan ini dengan file audio yang ingin diubah menjadi teks.")

def convert_to_wav(ogg_file):
    wav_file = "downloads/audio.wav"
    try:
        subprocess.run(['ffmpeg', '-i', ogg_file, wav_file, '-y'], check=True)
        logger.info(f"Audio converted to WAV format at {wav_file}")
        return wav_file
    except Exception as e:
        logger.error(f"Failed to convert audio to WAV: {e}")
        return None

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="id-ID")
            logger.info(f"Transcribed text: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def cleanup_temp_files():
    try:
        if os.path.exists(TEMP_AUDIO_PATH):
            os.remove(TEMP_AUDIO_PATH)
        if os.path.exists("downloads/audio.wav"):
            os.remove("downloads/audio.wav")
    except Exception as e:
        logger.error(f"Failed to delete temporary files: {e}")

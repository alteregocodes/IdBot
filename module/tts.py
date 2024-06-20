# module/tts.py

from gtts import gTTS
from io import BytesIO
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

LANG_CODES = {
    "Indonesian": "id",
    "Sundanese": "su",
    "Japanese": "ja",
    "Amharic": "am",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Arabic": "ar",
    "Korean": "ko",
    "Thai": "th"
    # Tambahkan bahasa lain sesuai kebutuhan
}

DEFAULT_LANG = "id"  # Bahasa Indonesia sebagai default

# Dictionary untuk menyimpan preferensi bahasa pengguna
USER_LANG_PREFS = {}

def text_to_speech(text, language):
    tts = gTTS(text, lang=language)
    output_file = "output.ogg"
    tts.save(output_file)
    return output_file

def get_lang_code(user_id):
    return USER_LANG_PREFS.get(user_id, DEFAULT_LANG)

def set_lang_preference(user_id, language_code):
    USER_LANG_PREFS[user_id] = language_code

def remove_output_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def get_lang_name(language_code):
    for lang, code in LANG_CODES.items():
        if code == language_code:
            return lang
    return "Unknown"

# Handler untuk perintah TTS (/tts)
async def tts_command(client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply("Silakan berikan teks yang ingin diubah menjadi suara.")
        return
    text = message.reply_to_message.text if message.reply_to_message else message.text.split(None, 1)[1]
    language = get_lang_code(message.from_user.id)
    output_file = text_to_speech(text, language)
    try:
        await client.send_voice(message.chat.id, voice=output_file)
        await message.delete()
    except Exception as e:
        await message.reply_text(f"Error: {e}")
    finally:
        remove_output_file(output_file)

# Handler untuk perintah setting bahasa TTS (/bahasatts)
async def set_tts_language(client, message: Message):
    buttons = []
    for lang, code in LANG_CODES.items():
        buttons.append([InlineKeyboardButton(lang, callback_data=f"set_lang_{code}")])
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("Pilih bahasa untuk TTS:", reply_markup=reply_markup)

# Handler untuk callback setting bahasa TTS
async def set_tts_language_callback(client, callback_query: CallbackQuery):
    language_code = callback_query.data.split("_")[2]
    set_lang_preference(callback_query.from_user.id, language_code)
    language_name = get_lang_name(language_code)
    await callback_query.answer(f"Bahasa TTS diatur ke {language_name}")

# Handler untuk perintah TTS (/tts)
@Client.on_message(filters.command("tts"))
async def tts_command_handler(client, message: Message):
    await tts_command(client, message)

# Handler untuk perintah setting bahasa TTS (/bahasatts)
@Client.on_message(filters.command("bahasatts"))
async def set_tts_language_handler(client, message: Message):
    await set_tts_language(client, message)

# Handler untuk callback setting bahasa TTS
@Client.on_callback_query(filters.regex(r"^set_lang_"))
async def set_tts_language_callback_handler(client, callback_query: CallbackQuery):
    await set_tts_language_callback(client, callback_query)

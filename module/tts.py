# module/tts.py

from gtts import gTTS
from io import BytesIO
import os

LANG_CODES = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Japanese": "ja",
    "Korean": "ko",
    "Sundanese": "su",
    "Thai": "th",
    "Filipino": "fil",
    "Indonesian": "id"
    # Tambahkan bahasa lain sesuai kebutuhan
}

DEFAULT_LANG = "id"  # Bahasa Inggris sebagai default

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

# module/tts_utils.py

from gtts import gTTS
import os
import json

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

def text_to_speech(text, language):
    tts = gTTS(text, lang=language)
    output_file = "output.ogg"
    tts.save(output_file)
    return output_file

def get_lang_code(user_id):
    try:
        with open('language_preferences.json', 'r') as f:
            lang_preferences = json.load(f)
        return lang_preferences.get(str(user_id), DEFAULT_LANG)
    except FileNotFoundError:
        return DEFAULT_LANG

def set_lang_preference(user_id, lang_code):
    try:
        with open('language_preferences.json', 'r') as f:
            lang_preferences = json.load(f)
    except FileNotFoundError:
        lang_preferences = {}
    
    lang_preferences[str(user_id)] = lang_code
    
    with open('language_preferences.json', 'w') as f:
        json.dump(lang_preferences, f)

def get_lang_name(lang_code):
    for lang, code in LANG_CODES.items():
        if code == lang_code:
            return lang
    return "Unknown"

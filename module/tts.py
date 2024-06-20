# module/tts.py

import os
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from .tts_utils import text_to_speech, get_lang_code, set_lang_preference, get_lang_name, LANG_CODES

def register_handlers(app):
    @app.on_message(filters.command("tts"))
    async def tts_command(client, message: Message):
        if len(message.command) < 2 and not message.reply_to_message:
            await message.reply("Silakan berikan teks yang ingin diubah menjadi suara.")
            return
        
        text = message.reply_to_message.text if message.reply_to_message else message.text.split(None, 1)[1]
        language = get_lang_code(message.from_user.id)
        output_file = text_to_speech(text, language)
        
        try:
            await message.reply_voice(voice=output_file)
        except Exception as e:
            await message.reply_text(f"Error: {e}")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    @app.on_message(filters.command("bahasatts") & (filters.group | filters.private))
    async def set_tts_language(client, message: Message):
        buttons = []
        user_language_code = get_lang_code(message.from_user.id)
        user_language_name = get_lang_name(user_language_code)
        for lang, code in LANG_CODES.items():
            if code != user_language_code:
                buttons.append([InlineKeyboardButton(lang, callback_data=f"set_lang_{code}")])
        reply_markup = InlineKeyboardMarkup(buttons)
        message_reply = await message.reply_text(
            f"Pilih bahasa untuk TTS:\n\nBahasa yang digunakan sekarang: {user_language_name}",
            reply_markup=reply_markup
        )
        await asyncio.sleep(10)
        await message_reply.delete()  # Menghapus pesan pemilihan bahasa setelah beberapa detik

    @app.on_callback_query(filters.regex(r"^set_lang_"))
    async def set_tts_language_callback(client, callback_query: CallbackQuery):
        language_code = callback_query.data.split("_")[2]
        set_lang_preference(callback_query.from_user.id, language_code)
        language_name = get_lang_name(language_code)
        
        await callback_query.answer(f"Bahasa TTS diatur ke {language_name}", show_alert=True)
        
        await callback_query.message.delete_reply_markup()

        try:
            await callback_query.message.delete()
        except Exception as e:
            print(f"Failed to delete message: {e}")

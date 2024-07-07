from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start(client, message):
        buttons = [
            [InlineKeyboardButton("Support Channel", url="https://t.me/supportchannel")],
            [InlineKeyboardButton("Ambil String", callback_data="ambil_string")],
            [InlineKeyboardButton("Help", callback_data="help")],
        ]
        await message.reply("Welcome to the bot!", reply_markup=InlineKeyboardMarkup(buttons))

    @app.on_callback_query(filters.regex("ambil_string"))
    async def handle_ambil_string(client, callback_query):
        ask_ques = "**» Pilih Jenis Strings Yang Mau di Generate **"
        buttons_ques = [
            [
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram"),
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram_v2"),
            ],
            [InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 💻", callback_data="telethon")],
            [
                InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
                InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
            ],
            [InlineKeyboardButton("Help", callback_data="help")],
        ]
        await callback_query.message.edit(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

    @app.on_callback_query(filters.regex("help"))
    async def handle_help(client, callback_query):
        help_text = """
        Available Commands:
        
        /tts <text> - Convert text to speech in the selected language.
        /setlang - Set language for Text-to-Speech (TTS).
        /id - Display your ID and group ID (if in a group).
        /carbon <code> - Create a "carbon" image from the provided code.
        /song <song title/YouTube link> - Download and send an audio file of the song or YouTube link.
        /vsong <video title/YouTube link> - Download and send a video file of the video or YouTube link.
        
        How to Get Channel/Group IDs:
        Forward a message from the channel/group to this bot, or use the /id command if inside it.
        """
        await callback_query.message.edit(help_text.strip(), reply_markup=None)

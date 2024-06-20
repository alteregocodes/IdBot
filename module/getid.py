from pyrogram import Client, filters
from pyrogram.types import Message

def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)

def register_handlers(app):
    @app.on_message(filters.forwarded)
    async def get_forwarded_info(client, message: Message):
        if message.forward_from_chat:
            chat_id = message.forward_from_chat.id
            chat_id_formatted = f"-{abs(chat_id)}" if chat_id < 0 else str(chat_id)
            await message.reply_text(f"ID Channel/Grup: `{escape_markdown(chat_id_formatted)}`", parse_mode="markdown_v2")
        else:
            await message.reply_text("Pesan ini tidak berasal dari channel atau grup.", parse_mode="markdown_v2")

    @app.on_message(filters.command("id"))
    async def get_user_id(client, message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id  # Mendapatkan ID chat tempat perintah diterima

        # Debugging output untuk memastikan chat_id diambil dengan benar
        print(f"User ID: {user_id}, Chat ID: {chat_id}, Chat Type: {message.chat.type}")

        # Log tambahan
        try:
            if message.chat.type in ["group", "supergroup"]:
                text = f"ID Anda adalah: `{escape_markdown(str(user_id))}`\nID Grup ini adalah: `{escape_markdown(str(chat_id))}`"
            else:
                text = f"ID Anda adalah: `{escape_markdown(str(user_id))}`"
            
            await message.reply_text(text, parse_mode="markdown_v2")
        except Exception as e:
            print(f"Error sending message: {e}")

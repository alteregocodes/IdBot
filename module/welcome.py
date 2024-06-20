# module/welcome.py

from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from .carbon import make_carbon

async def welcome_new_member(client, chat_member_updated: ChatMemberUpdated):
    new_member = chat_member_updated.new_chat_member
    chat_id = chat_member_updated.chat.id
    group_name = chat_member_updated.chat.title
    
    fullname = new_member.user.first_name + " " + (new_member.user.last_name or "")
    username = new_member.user.username or "-"
    user_id = new_member.user.id
    join_date = datetime.now().strftime("%d %B %Y")
    
    text = (
        f"Nama: {fullname}\n"
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"Tanggal Bergabung: {join_date}\n\n"
        f"Selamat datang di {group_name}, semoga betah!"
    )
    
    carbon_image = await make_carbon(text)
    
    await client.send_photo(
        chat_id,
        photo=carbon_image,
        caption=f"Selamat datang @{username} di {group_name}, semoga betah!",
    )
    
    carbon_image.close()

@Client.on_chat_member_updated()
async def welcome_new_members(client, chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member and chat_member_updated.new_chat_member.status == "member":
        await welcome_new_member(client, chat_member_updated)

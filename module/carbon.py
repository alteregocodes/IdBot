# module/carbon.py

import asyncio
import aiohttp
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message

aiosession = None

async def init_aiosession():
    global aiosession
    if aiosession is None:
        aiosession = aiohttp.ClientSession()

async def make_carbon(code):
    await init_aiosession()
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(message.command) != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply("❄️ Memproses . . .")
    carbon = await make_carbon(text)
    await ex.edit("🔼 Mengunggah . . .")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"<b>Carbonised by:</b> {client.me.mention}",
        ),
    )
    carbon.close()

@Client.on_message(filters.command("carbon") & (filters.group | filters.private))
async def carbon_command(client, message: Message):
    await carbon_func(client, message)

import atexit

@atexit.register
def close_aiohttp_session():
    if aiosession:
        asyncio.run(aiosession.close())

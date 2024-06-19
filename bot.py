# bot.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import Config

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)

# Inisialisasi bot dan dispatcher
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot)

async def is_subscribed(user_id):
    if Config.FORCE_SUBS_CHANNEL_ID:
        chat_member = await bot.get_chat_member(Config.FORCE_SUBS_CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    return True

# Handler untuk perintah /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if await is_subscribed(message.from_user.id):
        await message.reply(Config.START_MESSAGE)
    else:
        await message.reply(Config.FORCE_SUBS_MESSAGE.format(channel_link=Config.FORCE_SUBS_CHANNEL_ID))

# Handler untuk pesan yang diteruskan
@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_handler(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await message.reply(Config.FORCE_SUBS_MESSAGE.format(channel_link=Config.FORCE_SUBS_CHANNEL_ID))
        return

    if message.forward_from_chat:
        forward_chat_id = message.forward_from_chat.id
        await message.reply(f"ID channel/grup yang diteruskan: {forward_chat_id}")
    else:
        await message.reply("Pesan ini tidak diteruskan dari channel/grup.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

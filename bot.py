# bot.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import Config

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)

# Inisialisasi bot dan dispatcher
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Handler untuk perintah /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(Config.START_MESSAGE)

# Handler untuk pesan yang diteruskan
@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_handler(message: types.Message):
    if message.forward_from_chat:
        forward_chat_id = message.forward_from_chat.id
        await message.reply(f"ID channel/grup yang diteruskan: {forward_chat_id}")
    else:
        await message.reply("Pesan ini tidak diteruskan dari channel/grup.")

# Handler untuk force subscription
@dp.message_handler(commands=['subscribe'])
async def force_subscribe(message: types.Message):
    if Config.FORCE_SUBS_CHANNEL_ID:
        await message.reply(Config.FORCE_SUBS_MESSAGE, parse_mode=ParseMode.HTML)
    else:
        await message.reply("Tidak ada channel untuk force subscription yang disetel.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

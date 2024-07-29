from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait
from pymongo import MongoClient
import config

# Initialize database connection
client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
user_sessions = db["user_sessions"]

# State storage for tracking user state
user_states = {}

def register_handlers(app: Client):
    @app.on_callback_query(filters.regex("pyrogram|pyrogram_v2|telethon|pyrogram_bot|telethon_bot"))
    async def generate_session(client, callback_query):
        callback_data = callback_query.data
        await callback_query.message.edit("» Trying to start **{}** session generator...".format(callback_data.upper()))

        # Start generating session based on the selected type
        await generate_session_logic(client, callback_query.message, callback_data)

    @app.on_message(filters.text)
    async def handle_user_input(client, message: Message):
        user_id = message.chat.id
        if user_id in user_states:
            state = user_states[user_id]
            if state["waiting_for"] == "api_id":
                await handle_api_id(client, message, user_id)
            elif state["waiting_for"] == "api_hash":
                await handle_api_hash(client, message, user_id)
            elif state["waiting_for"] == "phone_number":
                await handle_phone_number(client, message, user_id)
            elif state["waiting_for"] == "otp":
                await handle_otp(client, message, user_id)
            elif state["waiting_for"] == "password":
                await handle_password(client, message, user_id)

async def handle_api_id(client: Client, message: Message, user_id: int):
    api_id = message.text
    if api_id == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
        user_states[user_id]["api_id"] = api_id
        user_states[user_id]["api_hash"] = api_hash
        await client.send_message(user_id, "Please send your **API_HASH** to continue.")
        user_states[user_id]["waiting_for"] = "api_hash"
    else:
        try:
            api_id = int(api_id)
            user_states[user_id]["api_id"] = api_id
            await client.send_message(user_id, "Please send your **API_HASH** to continue.")
            user_states[user_id]["waiting_for"] = "api_hash"
        except ValueError:
            await client.send_message(user_id, "**API_ID** must be an integer. Please try again.")
            return

async def handle_api_hash(client: Client, message: Message, user_id: int):
    api_hash = message.text
    user_states[user_id]["api_hash"] = api_hash
    await client.send_message(user_id, "Please send your phone number to proceed:\nExample: `+62 62xxxxxxXX`.")
    user_states[user_id]["waiting_for"] = "phone_number"

async def handle_phone_number(client: Client, message: Message, user_id: int):
    phone_number = message.text
    user_states[user_id]["phone_number"] = phone_number
    await client.send_message(user_id, "Please send the **OTP** you received from Telegram on your account.\nIf OTP is `12345`, please send it as `1 2 3 4 5`.")
    user_states[user_id]["waiting_for"] = "otp"

async def handle_otp(client: Client, message: Message, user_id: int):
    otp = message.text.replace(" ", "")
    user_states[user_id]["otp"] = otp
    # Proceed with logging in, etc.
    # Once done, you can clear the state
    user_states.pop(user_id, None)

async def handle_password(client: Client, message: Message, user_id: int):
    password = message.text
    user_states[user_id]["password"] = password
    # Proceed with password handling, etc.
    # Once done, you can clear the state
    user_states.pop(user_id, None)

async def generate_session_logic(bot: Client, msg: Message, session_type: str):
    telethon = "telethon" in session_type
    is_bot = "bot" in session_type
    old_pyro = session_type == "pyrogram"

    user_id = msg.chat.id

    user_states[user_id] = {"waiting_for": "api_id"}

    await bot.send_message(user_id, "Please send your **API_ID** to proceed.\nClick /skip for using bot API.")

# Start the Pyrogram client and register handlers
app = Client("my_bot")
register_handlers(app)
app.run()

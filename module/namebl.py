import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserAdminInvalid, FloodWait, RPCError
import config
from database import Database

db = Database()

def register_handlers(app: Client):
    @app.on_message(filters.new_chat_members)
    async def check_new_members(client, message):
        blacklist = db.load_blacklist()
        blacklist = [name.lower() for name in blacklist]  # Convert all blacklisted names to lowercase
        new_members = message.new_chat_members
        for member in new_members:
            member_name = (member.first_name + " " + member.last_name).lower() if member.last_name else member.first_name.lower()
            print(f"New member name: {member_name}")  # Debug log for new member names
            # Periksa apakah nama member mengandung kata yang di-blacklist
            for blacklisted_name in blacklist:
                if blacklisted_name in member_name:
                    try:
                        await ban_user_from_all_groups(client, member.id)
                        await message.reply_text(f"User {member.mention} telah di-ban dari semua grup karena namanya mengandung kata yang di-blacklist.")
                    except UserAdminInvalid:
                        await message.reply_text(f"Tidak dapat ban {member.mention} karena bot bukan admin di beberapa grup.")
                    except FloodWait as e:
                        print(f"Flood wait: {e.x} seconds")
                        await asyncio.sleep(e.x)
                    except Exception as e:
                        print(f"Error: {e}")
                    break  # Tidak perlu memeriksa nama yang lain jika sudah match

    @app.on_message(filters.command("addblacklist") & filters.user(config.OWNER_IDS))
    async def add_blacklist_command(client, message):
        if len(message.command) > 1:
            name_to_add = " ".join(message.command[1:])
            db.add_to_blacklist(name_to_add)
            await message.reply_text(f"Nama '{name_to_add}' telah ditambahkan ke blacklist.")
        else:
            await message.reply_text("Gunakan perintah dengan format: /addblacklist [nama]")

async def ban_user_from_all_groups(client: Client, user_id: int):
    async for dialog in client.get_dialogs():
        if dialog.chat.type in ["group", "supergroup"] and dialog.chat.permissions.can_restrict_members:
            try:
                await client.ban_chat_member(dialog.chat.id, user_id)
                print(f"Banned user {user_id} from {dialog.chat.title}")
            except UserAdminInvalid:
                print(f"Bot is not an admin in {dialog.chat.title}")
            except FloodWait as e:
                print(f"Flood wait: {e.x} seconds")
                await asyncio.sleep(e.x)
            except Exception as e:
                print(f"Error banning user {user_id} from {dialog.chat.title}: {e}")

async def monitor_groups_for_blacklist(client: Client):
    while True:
        blacklist = db.load_blacklist()
        blacklist = [name.lower() for name in blacklist]  # Convert all blacklisted names to lowercase
        print(f"Loaded blacklist: {blacklist}")  # Debugging log
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"] and dialog.chat.permissions.can_restrict_members:
                print(f"Checking group: {dialog.chat.title}")  # Debugging log
                async for member in client.get_chat_members(dialog.chat.id):
                    member_name = (member.user.first_name + " " + member.user.last_name).lower() if member.user.last_name else member.user.first_name.lower()
                    print(f"Checking member: {member_name} in group {dialog.chat.title}")  # Debug log for member names in groups
                    for blacklisted_name in blacklist:
                        if blacklisted_name in member_name:
                            try:
                                await client.ban_chat_member(dialog.chat.id, member.user.id)
                                print(f"Banned user {member.user.first_name} ({member.user.id}) from {dialog.chat.title} because their name contains a blacklisted term.")
                            except UserAdminInvalid:
                                print(f"Bot is not an admin in {dialog.chat.title}")
                            except FloodWait as e:
                                print(f"Flood wait: {e.x} seconds")
                                await asyncio.sleep(e.x)
                            except RPCError as e:
                                print(f"RPC Error: {e}")
                            except Exception as e:
                                print(f"Error banning user {member.user.id} from {dialog.chat.title}: {e}")
                            break  # Tidak perlu memeriksa nama yang lain jika sudah match
        await asyncio.sleep(5)  # Tunggu 5 detik sebelum memeriksa lagi

async def main():
    app = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)
    register_handlers(app)

    async with app:
        # Mulai task untuk memantau grup dan memeriksa anggota yang ada
        asyncio.create_task(monitor_groups_for_blacklist(app))

        # Menunggu perintah dari pengguna atau event dari chat
        await app.idle()

if __name__ == "__main__":
    asyncio.run(main())

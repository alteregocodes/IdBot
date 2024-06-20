import asyncio
import math
import os
from datetime import timedelta
from time import time

import wget
from pyrogram import Client
from pyrogram.errors import FloodWait, MessageNotModified
from youtubesearchpython import VideosSearch

# Function to convert bytes to human-readable format
def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "kb", 2: "mb", 3: "gb", 4: "tb"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}"

# Function to format milliseconds into human-readable time
def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} hari, " if days else "")
        + (f"{str(hours)} jam, " if hours else "")
        + (f"{str(minutes)} menit, " if minutes else "")
        + (f"{str(seconds)} detik, " if seconds else "")
        + (f"{str(milliseconds)} mikrodetik, " if milliseconds else "")
    )
    return tmp[:-2]

# Function to show download progress
async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("•" for _ in range(math.floor(percentage / 10))),
            "".join("~" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nestimasi: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    f"""
<b>{type_of_ps}</b>

<b>file_id:</b> <code>{file_name}</code>

<b>{tmp}</b>
"""
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit(f"{type_of_ps}\n{tmp}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass

# Function to handle /vsong command to download video
async def vsong_cmd(client: Client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>❌ Video tidak ditemukan,</b>\nMohon masukkan judul video dengan benar.",
        )
    infomsg = await message.reply_text("<b>🔍 Pencarian...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>❌ Pencarian gagal:\n{error}</b>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await infomsg.edit(f"<b>❌ Gagal mengunduh:\n{error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_video(
        message.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "video",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            client.me.mention,
        ),
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            "<b>📥 Mendownload...</b>",
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=message.message_id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)

# Function to handle /song command to download audio
async def song_cmd(client: Client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>❌ Audio tidak ditemukan,</b>\nMohon masukkan judul video dengan benar.",
        )
    infomsg = await message.reply_text("<b>🔍 Pencarian...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>❌ Pencarian gagal:\n{error}</b>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await infomsg.edit(f"<b>❌ Gagal mengunduh:\n{error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_audio(
        message.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "audio",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            client.me.mention,
        ),
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            "<b>📥 Mendownload...</b>",
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=message.message_id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)

async def YoutubeDownload(link, as_video=True):
    # Implementasi fungsi ini tergantung pada bagaimana Anda ingin mengunduh video atau audio dari YouTube.
    # Anda dapat menggunakan pustaka seperti `pytube` atau metode lain yang mendukung unduhan dari YouTube.
    # Silakan sesuaikan logika unduhan berdasarkan kebutuhan Anda.
    pass

import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==== CONFIG ====
API_ID = int(os.getenv("API_ID", 27498866))       # my.telegram.org se lo
API_HASH = os.getenv("API_HASH", "96fbb6ad2e11ab04e83ca09ef3f42455")  # my.telegram.org se lo
BOT_TOKEN = os.getenv("BOT_TOKEN", "7242497051:AAEc9WhkZgahtMjUygbXtMK51t6s3wvAg3c")  # BotFather se lo
# ================

app = Client("youtube_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Function: Video info nikalna
def get_info(url):
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
    return info


# Function: Video download
def download_youtube(url, format_id, file_name="video.mp4"):
    ydl_opts = {
        "outtmpl": file_name,
        "format": format_id,
        "merge_output_format": "mp4"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return file_name


# Function: Audio download (MP3)
def download_audio(url, file_name="audio.mp3"):
    ydl_opts = {
        "outtmpl": file_name,
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return file_name


# /start
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply(
        "👋 Namaste! Mujhe YouTube link bhejo.\n\n"
        "📌 Main aapko Video ya Audio dono options dunga 🎥🎵"
    )


# YouTube link handle
@app.on_message(filters.regex(r"^https?://(www\.)?(youtube\.com|youtu\.be)/"))
async def youtube_link(_, message):
    url = message.text.strip()
    buttons = [
        [InlineKeyboardButton("🎥 Video", callback_data=f"video|{url}")],
        [InlineKeyboardButton("🎵 Audio (MP3)", callback_data=f"audio|{url}")]
    ]
    await message.reply("✅ Select format:", reply_markup=InlineKeyboardMarkup(buttons))


# Callback handle
@app.on_callback_query()
async def callback(_, query):
    action, url = query.data.split("|", 1)

    if action == "video":
        await query.message.edit_text("🔍 Checking video qualities...")
        try:
            info = get_info(url)
            formats = []
            for f in info["formats"]:
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    q = f.get("format_note") or f.get("height")
                    size = f.get("filesize") or 0
                    size_mb = round(size / (1024 * 1024), 2) if size else "?"
                    formats.append((f["format_id"], f"{q} ({size_mb} MB)"))

            if not formats:
                await query.message.reply("❌ Koi video format available nahi mila.")
                return

            buttons = []
            for fmt in formats[:6]:  # Top 6 qualities show karenge
                buttons.append([InlineKeyboardButton(fmt[1], callback_data=f"download_video|{url}|{fmt[0]}")])

            await query.message.reply(
                f"🎬 *{info.get('title')}*\n👤 Channel: {info.get('uploader')}\n\n✅ Select Video Quality:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        except Exception as e:
            await query.message.reply(f"❌ Error: {e}")

    elif action == "audio":
        await query.message.edit_text("📥 Downloading audio... ⏳")
        try:
            info = get_info(url)
            file_path = download_audio(url, f"{query.from_user.id}.mp3")
            await query.message.reply_audio(
                file_path,
                caption=f"🎵 *{info.get('title')}*\n👤 Channel: {info.get('uploader')}\n✅ Audio (MP3)"
            )
            os.remove(file_path)
        except Exception as e:
            await query.message.reply(f"❌ Error: {e}")

    elif action.startswith("download_video"):
        _, url, format_id = action.split("|")
        await query.message.edit_text("📥 Downloading video... ⏳")
        try:
            info = get_info(url)
            file_path = download_youtube(url, format_id, f"{query.from_user.id}.mp4")
            await query.message.reply_video(
                file_path,
                caption=f"🎬 *{info.get('title')}*\n👤 Channel: {info.get('uploader')}\n✅ Video Downloaded"
            )
            os.remove(file_path)
        except Exception as e:
            await query.message.reply(f"❌ Error: {e}")


print("🤖 YouTube Bot Started on Koyeb...")
app.run()

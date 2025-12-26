import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL
from pymongo import MongoClient

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

OWNER_ID = "8247235878"   # owner id string

if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URI]):
    raise RuntimeError("❌ One or more environment variables are missing")

# ================= DATABASE =================

mongo = MongoClient(MONGO_URI)
db = mongo["aesthetic_music_bot"]
sudo_db = db["sudo_users"]

def is_owner(user_id: int):
    return str(user_id) == OWNER_ID

def is_sudo(user_id: int):
    return sudo_db.find_one({"user_id": user_id}) is not None or is_owner(user_id)

# ================= BOT INIT =================

app = Client(
    "aesthetic_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

vc = PyTgCalls(app)

# ================= START =================

@app.on_message(filters.command("start"))
async def start_cmd(_, message):
    await message.reply_text(
        "🎵 **Aesthetic Music Bot**\n\n"
        "Use `/play song name` to play music in VC 🎶"
    )

# ================= PLAY =================

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):
    if not message.from_user:
        return

    if not (is_owner(message.from_user.id) or is_sudo(message.from_user.id)):
        await message.reply_text("❌ You are not allowed to play music.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: `/play song name`")
        return

    query = " ".join(message.command[1:])

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        url = info["entries"][0]["url"]
        title = info["entries"][0]["title"]

    await vc.join_group_call(
        message.chat.id,
        AudioPiped(url),
    )

    await message.reply_text(f"▶️ **Now Playing:** `{title}`")

# ================= ADD SUDO =================

@app.on_message(filters.command("addsudo"))
async def add_sudo(_, message):
    if not message.from_user or not is_owner(message.from_user.id):
        return await message.reply_text("❌ Only owner can use this command.")

    if len(message.command) < 2:
        return await message.reply_text("Usage: `/addsudo user_id`")

    user_id = int(message.command[1])
    sudo_db.insert_one({"user_id": user_id})

    await message.reply_text(f"✅ User `{user_id}` added as SUDO.")

# ================= INFO =================

@app.on_message(filters.command("info"))
async def info_cmd(_, message):
    await message.reply_text(
        "ℹ️ **Bot Info**\n\n"
        "👑 Owner: @notprism\n"
        "🆔 User ID: 8247235878"
    )

# ================= WELCOME =================

@app.on_chat_member_updated()
async def welcome(_, update: ChatMemberUpdated):
    if update.new_chat_member and not update.old_chat_member:
        user = update.new_chat_member.user
        await app.send_message(
            update.chat.id,
            f"""
✨ **Welcome to our group!** ✨

💖 You are now our family member 💖

👤 Name: **{user.first_name}**
🆔 User ID: `{user.id}`
"""
        )

# ================= RUN =================

async def main():
    await app.start()
    await vc.start()
    print("🔥 Aesthetic Music Bot is ONLINE")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

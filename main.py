import os
import asyncio

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL
from pymongo import MongoClient

# ================= ENV =================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

OWNER_ID = 8247235878

# ================= DB =================

mongo = MongoClient(MONGO_URI)
db = mongo["musicbot"]
sudo_db = db["sudo"]

def is_owner(uid):
    return uid == OWNER_ID

def is_sudo(uid):
    return sudo_db.find_one({"uid": uid}) or is_owner(uid)

# ================= BOT =================

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

pytg = PyTgCalls(app)

# ================= COMMANDS =================

@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("🎵 Aesthetic Music Bot is Live")

@app.on_message(filters.command("play") & filters.group)
async def play(_, m):
    if not m.from_user or not is_sudo(m.from_user.id):
        return await m.reply("❌ Permission denied")

    if len(m.command) < 2:
        return await m.reply("Usage: /play song")

    query = " ".join(m.command[1:])
    ydl_opts = {"format": "bestaudio", "quiet": True}

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        url = info["entries"][0]["url"]
        title = info["entries"][0]["title"]

    await pytg.join_group_call(
        m.chat.id,
        AudioPiped(url)
    )

    await m.reply(f"▶️ Playing: `{title}`")

@app.on_message(filters.command("addsudo"))
async def addsudo(_, m):
    if not m.from_user or not is_owner(m.from_user.id):
        return
    uid = int(m.command[1])
    sudo_db.insert_one({"uid": uid})
    await m.reply(f"✅ `{uid}` added as sudo")

@app.on_message(filters.command("info"))
async def info(_, m):
    await m.reply("👑 Owner: @notprism\n🆔 ID: 8247235878")

# ================= RUN =================

async def main():
    await app.start()
    await pytg.start()
    print("🔥 BOT ONLINE")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

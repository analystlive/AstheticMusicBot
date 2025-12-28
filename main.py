import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

from yt_dlp import YoutubeDL

# ================== CONFIG ==================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

OWNER_ID = 8427235878  # अपना ID डालो
# ============================================

# ================== CLIENTS ==================
bot = Client(
    "AestheticMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user = Client(
    SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH
)

pytg = PyTgCalls(user)
# ============================================

# ================== YTDLP ====================
ydl_opts = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True
}
# ============================================


# ================== COMMANDS =================

@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply(
        "🎧 **Aesthetic Music Bot is Online**\n\n"
        "▶️ `/play song name`\n"
        "⏸ `/pause`\n"
        "▶️ `/resume`\n"
        "⏭ `/skip`\n"
        "⛔ `/stop`"
    )


@bot.on_message(filters.command("play") & filters.group)
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply("❌ Usage: `/play song name`")

    query = " ".join(m.command[1:])
    chat_id = m.chat.id

    msg = await m.reply("🔎 Searching...")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            data = info["entries"][0]
            url = data["url"]
            title = data["title"]

        await pytg.join_group_call(
            chat_id,
            AudioPiped(url)
        )

        await msg.edit(f"▶️ **Now Playing:** `{title}`")

    except Exception as e:
        await msg.edit(f"❌ Error:\n`{e}`")


@bot.on_message(filters.command("pause") & filters.group)
async def pause(_, m: Message):
    await pytg.pause_stream(m.chat.id)
    await m.reply("⏸ Paused")


@bot.on_message(filters.command("resume") & filters.group)
async def resume(_, m: Message):
    await pytg.resume_stream(m.chat.id)
    await m.reply("▶️ Resumed")


@bot.on_message(filters.command("skip") & filters.group)
async def skip(_, m: Message):
    await pytg.leave_group_call(m.chat.id)
    await m.reply("⏭ Skipped")


@bot.on_message(filters.command("stop") & filters.group)
async def stop(_, m: Message):
    await pytg.leave_group_call(m.chat.id)
    await m.reply("⛔ Stopped & Left VC")


# ================== RUN ======================
async def main():
    await bot.start()
    await user.start()
    await pytg.start()
    print("✅ Aesthetic Music Bot Started")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

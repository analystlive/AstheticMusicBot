import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ================= ENV =================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ================= BOT =================
app = Client(
    "aesthetic-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= OWNER / ADMIN =================
OWNER_ID = 8247235878
ADMIN_TAG = "@notprism"

# ================= STYLISH FONT =================
def fancy(text):
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    fancy_ = "𝒶𝒷𝒸𝒹𝑒𝒻𝓰𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝓸𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵0123456789"
    return text.translate(str.maketrans(normal, fancy_))

# ================= WELCOME IMAGE =================
WELCOME_IMAGE = "https://i.imgur.com/6XGQ5ZB.jpg"
GOODBYE_IMAGE = "https://i.imgur.com/QMZ8C0G.jpg"

# ================= INLINE BUTTON =================
buttons = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("✨ Admin", url=f"https://t.me/{ADMIN_TAG.replace('@','')}")],
        [InlineKeyboardButton("💬 Support", url="https://t.me/telegram")]
    ]
)

# ================= WELCOME =================
@app.on_message(filters.new_chat_members)
async def welcome(_, m: Message):
    for user in m.new_chat_members:
        name = user.first_name or "User"
        uid = user.id

        text = f"""
✨ 𝓦𝓔𝓛𝓒𝓞𝓜𝓔 𝓣𝓞 𝓞𝓤𝓡 𝓖𝓡𝓞𝓤𝓟 ✨

👤 Name : {fancy(name)}
🆔 User ID : {fancy(str(uid))}

💖 Welcome to our family
👑 Admin : {ADMIN_TAG}
"""

        await m.reply_photo(
            photo=WELCOME_IMAGE,
            caption=text,
            reply_markup=buttons
        )

# ================= GOODBYE =================
@app.on_message(filters.left_chat_member)
async def goodbye(_, m: Message):
    user = m.left_chat_member
    name = user.first_name or "User"

    text = f"""
🥀 𝓖𝓞𝓞𝓓𝓑𝓨𝓔 🥀

👤 {fancy(name)}
😔 You will be missed
"""

    await m.reply_photo(
        photo=GOODBYE_IMAGE,
        caption=text
    )

# ================= START =================
@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("✅ Aesthetic Welcome Bot is Alive!")

# ================= INFO =================
@app.on_message(filters.command("info"))
async def info(_, m):
    await m.reply(
        f"""
👑 Owner : {ADMIN_TAG}
🆔 User ID : {OWNER_ID}
🤖 Status : Online
"""
    )

# ================= RUN =================
async def main():
    await app.start()
    print("🔥 BOT STARTED SUCCESSFULLY")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

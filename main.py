import asyncio
from pyrogram import Client, idle
from pytgcalls import PyTgCalls

# Config (env se values uthti hain)
from config import API_ID, API_HASH, BOT_TOKEN

# Handlers
from handlers import (
    commands,
    callbacks,
    help as help_handler,
    admin,
    welcome,
)

# Background / recovery
from features.recovery import auto_cleanup


# ─────────────────────────────
# Pyrogram Client
# ─────────────────────────────
app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ─────────────────────────────
# PyTgCalls (Voice Chat)
# ─────────────────────────────
vc = PyTgCalls(app)


# ─────────────────────────────
# Register all handlers
# ─────────────────────────────
commands.register(app, vc)     # /play, /queue, etc.
callbacks.register(app, vc)    # inline buttons
help_handler.register(app)     # /help
admin.register(app)            # /addsudo /removesudo /sudolist /maintenance
welcome.register(app)          # auto welcome on join


# ─────────────────────────────
# Background tasks
# ─────────────────────────────
async def start_background_tasks():
    asyncio.create_task(auto_cleanup(vc))


# ─────────────────────────────
# Start Bot
# ─────────────────────────────
async def main():
    await app.start()
    await vc.start()
    await start_background_tasks()
    print("🔥 Aesthetic Music Bot is ONLINE")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

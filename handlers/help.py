from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def register(app):

    @app.on_message(filters.command("help"))
    async def help_cmd(_, m):
        text = (
            "🎧 **Music Bot Help**\n\n"
            "▶️ **Play Music**\n"
            "/play <song name>\n\n"
            "🎛 **Controls (SUDO only)**\n"
            "/pause\n"
            "/resume\n"
            "/skip\n"
            "/stop\n\n"
            "📜 **Info**\n"
            "/queue\n"
            "/help\n"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📜 Queue", callback_data="queue"),
                    InlineKeyboardButton("ℹ️ Info", callback_data="info"),
                ]
            ]
        )

        await m.reply(text, reply_markup=buttons)

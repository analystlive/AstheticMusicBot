from pyrogram import filters
from core.permissions import (
    is_owner,
    add_sudo,
    remove_sudo,
    list_sudo,
)

def register(app):

    @app.on_message(filters.command("addsudo"))
    async def addsudo(_, m):
        if not is_owner(m.from_user.id):
            return await m.reply("❌ Only owner can use this")

        if len(m.command) < 2 or not m.command[1].isdigit():
            return await m.reply("Usage: /addsudo <user_id>")

        uid = int(m.command[1])
        add_sudo(uid)
        await m.reply(f"✅ User `{uid}` added as SUDO")

    @app.on_message(filters.command("removesudo"))
    async def removesudo(_, m):
        if not is_owner(m.from_user.id):
            return await m.reply("❌ Only owner can use this")

        if len(m.command) < 2 or not m.command[1].isdigit():
            return await m.reply("Usage: /removesudo <user_id>")

        uid = int(m.command[1])
        remove_sudo(uid)
        await m.reply(f"🗑 User `{uid}` removed from SUDO")

    @app.on_message(filters.command("sudolist"))
    async def sudolist(_, m):
        if not is_owner(m.from_user.id):
            return await m.reply("❌ Only owner can use this")

        users = list_sudo()
        if not users:
            return await m.reply("📭 No sudo users")

        text = "👑 **SUDO USERS**\n\n"
        for u in users:
            text += f"• `{u}`\n"

        await m.reply(text)

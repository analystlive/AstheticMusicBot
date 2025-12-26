from pyrogram import filters

def register(app):

    @app.on_message(filters.new_chat_members)
    async def welcome(_, m):
        for user in m.new_chat_members:
            name = user.first_name
            user_id = user.id

            text = (
                "✨ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 𝗢𝘂𝗿 𝗙𝗮𝗺𝗶𝗹𝘆 ✨\n\n"
                f"👤 𝗡𝗮𝗺𝗲 : {name}\n"
                f"🆔 𝗨𝘀𝗲𝗿 𝗜𝗗 : `{user_id}`\n\n"
                "💖 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘄 𝗮 𝗽𝗮𝗿𝘁 𝗼𝗳 𝗼𝘂𝗿 𝗳𝗮𝗺𝗶𝗹𝘆 💖"
            )

            await m.reply(text)

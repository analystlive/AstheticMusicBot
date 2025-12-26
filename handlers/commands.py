from pyrogram import filters
from core.permissions import is_sudo
from core import queue as q
from core.player import stream_audio
from core.buttons import music_buttons

from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio


def register(app, vc):

    @app.on_message(filters.command("play") & filters.group)
    async def play(_, m):
        song = " ".join(m.command[1:])
        if not song:
            return await m.reply("❌ Song name do")

        q.add(m.chat.id, song)

        if m.chat.id not in q.now_playing:
            q.now_playing[m.chat.id] = song
            q.states[m.chat.id] = "playing"

            await vc.join_group_call(
                m.chat.id,
                InputAudioStream(
                    stream_audio(song),
                    HighQualityAudio()
                )
            )

            await m.reply(
                f"🎶 **Now Playing:** `{song}`",
                reply_markup=music_buttons(m.chat.id)
            )
        else:
            await m.reply(f"➕ Added to queue: `{song}`")

    @app.on_message(filters.command("queue"))
    async def show_queue(_, m):
        queue = q.get_queue(m.chat.id)
        if not queue:
            return await m.reply("📭 Queue empty")

        text = "📜 **Queue:**\n"
        for i, song in enumerate(queue, 1):
            text += f"{i}. {song}\n"

        await m.reply(text)

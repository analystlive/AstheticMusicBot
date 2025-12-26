from core import queue as q
from core.permissions import is_sudo
from core.buttons import music_buttons
from core.player import stream_audio

from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio


def register(app, vc):

    @app.on_callback_query()
    async def callbacks(_, cb):
        chat_id = cb.message.chat.id
        user_id = cb.from_user.id
        data = cb.data

        if not is_sudo(user_id):
            return await cb.answer("❌ Not allowed", show_alert=True)

        if data == "pause":
            await vc.pause_stream(chat_id)
            q.states[chat_id] = "paused"
            await cb.message.edit_reply_markup(
                reply_markup=music_buttons(chat_id)
            )
            await cb.answer("Paused ⏸")

        elif data == "resume":
            await vc.resume_stream(chat_id)
            q.states[chat_id] = "playing"
            await cb.message.edit_reply_markup(
                reply_markup=music_buttons(chat_id)
            )
            await cb.answer("Resumed ▶️")

        elif data == "skip":
            q.pop(chat_id)
            next_song = q.pop(chat_id)

            if next_song:
                q.now_playing[chat_id] = next_song
                q.states[chat_id] = "playing"

                await vc.change_stream(
                    chat_id,
                    InputAudioStream(
                        stream_audio(next_song),
                        HighQualityAudio()
                    )
                )

                await cb.message.edit_text(
                    f"🎶 **Now Playing:** `{next_song}`",
                    reply_markup=music_buttons(chat_id)
                )
            else:
                await vc.leave_group_call(chat_id)
                q.clear(chat_id)
                await cb.message.edit_text("🛑 Queue finished")

        elif data == "stop":
            q.clear(chat_id)
            await vc.leave_group_call(chat_id)
            await cb.message.edit_text("⏹ Music stopped")

        elif data == "queue":
            queue = q.get_queue(chat_id)
            if not queue:
                return await cb.answer("📭 Queue empty", show_alert=True)

            text = "📜 Queue:\n"
            for i, song in enumerate(queue, 1):
                text += f"{i}. {song}\n"

            await cb.answer(text, show_alert=True)

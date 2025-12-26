from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core import queue as q


def music_buttons(chat_id):
    """
    Song state ke hisaab se dynamic buttons
    """

    state = q.states.get(chat_id, "playing")

    if state == "paused":
        play_pause = InlineKeyboardButton(
            "▶️ Resume", callback_data="resume"
        )
    else:
        play_pause = InlineKeyboardButton(
            "⏸ Pause", callback_data="pause"
        )

    return InlineKeyboardMarkup(
        [
            [play_pause],
            [
                InlineKeyboardButton("⏭ Skip", callback_data="skip"),
                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
            ],
            [
                InlineKeyboardButton("📜 Queue", callback_data="queue"),
                InlineKeyboardButton("ℹ️ Info", callback_data="info"),
            ],
        ]
    )

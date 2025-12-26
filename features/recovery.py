import asyncio
from core import queue as q


async def auto_cleanup(vc):
    """
    Har 30 sec check karega:
    - agar queue empty hai
    - aur koi song play nahi ho raha
    to VC leave karega
    """

    while True:
        await asyncio.sleep(30)

        for chat_id in list(q.now_playing.keys()):
            queue = q.get_queue(chat_id)

            if not queue:
                try:
                    await vc.leave_group_call(chat_id)
                except Exception:
                    pass

                q.clear(chat_id)

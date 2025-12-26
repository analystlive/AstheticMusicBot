from collections import deque

# har group ke liye alag-alag data
queues = {}        # chat_id: deque
now_playing = {}   # chat_id: song
states = {}        # chat_id: playing | paused


def add(chat_id, song):
    queues.setdefault(chat_id, deque()).append(song)


def pop(chat_id):
    if chat_id in queues and queues[chat_id]:
        return queues[chat_id].popleft()


def get_queue(chat_id):
    return queues.get(chat_id, deque())


def clear(chat_id):
    queues.pop(chat_id, None)
    now_playing.pop(chat_id, None)
    states.pop(chat_id, None)

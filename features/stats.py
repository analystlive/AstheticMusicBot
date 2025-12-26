import time

START_TIME = time.time()
groups = set()
users = set()


def track(chat_id: int, user_id: int):
    groups.add(chat_id)
    users.add(user_id)


def get_stats():
    uptime = int(time.time() - START_TIME)
    return uptime, len(groups), len(users)

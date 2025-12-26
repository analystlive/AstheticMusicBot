from database.mongo import playlists


def add_song(user_id: int, song: str):
    playlists.update_one(
        {"user_id": user_id},
        {"$push": {"songs": song}},
        upsert=True
    )


def get_playlist(user_id: int):
    data = playlists.find_one({"user_id": user_id})
    return data["songs"] if data and "songs" in data else []


def remove_song(user_id: int, index: int) -> bool:
    data = playlists.find_one({"user_id": user_id})

    if not data or index < 0 or index >= len(data.get("songs", [])):
        return False

    songs = data["songs"]
    songs.pop(index)

    playlists.update_one(
        {"user_id": user_id},
        {"$set": {"songs": songs}}
    )
    return True


def clear_playlist(user_id: int):
    playlists.delete_one({"user_id": user_id})

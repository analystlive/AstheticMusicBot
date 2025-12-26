import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client["aesthetic_music_bot"]

# collections
playlists = db["playlists"]
sudo_users = db["sudo_users"]

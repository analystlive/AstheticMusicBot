# Simple language system (runtime)
# Default: English

languages = {
    "en": {
        "welcome": "Welcome to our family",
        "no_permission": "❌ You are not allowed",
        "nothing_playing": "❌ Nothing is playing",
    },
    "hi": {
        "welcome": "हमारे परिवार में आपका स्वागत है",
        "no_permission": "❌ आपको अनुमति नहीं है",
        "nothing_playing": "❌ कुछ भी नहीं चल रहा",
    },
}

# user_id : language
user_lang = {}


def set_lang(user_id: int, lang: str):
    if lang in languages:
        user_lang[user_id] = lang


def get(user_id: int, key: str):
    lang = user_lang.get(user_id, "en")
    return languages.get(lang, {}).get(key, key)

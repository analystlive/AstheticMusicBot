import subprocess


def stream_audio(query: str):
    """
    YouTube se bestaudio stream karta hai
    ffmpeg ke through Telegram VC ke liye optimize karta hai
    """

    ytdlp_cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "-o", "-",
        f"ytsearch:{query}",
    ]

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", "pipe:0",
        "-vn",
        "-ac", "2",
        "-ar", "48000",
        "-c:a", "libopus",
        "-b:a", "160k",
        "-f", "opus",
        "pipe:1",
    ]

    ytdlp = subprocess.Popen(
        ytdlp_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    ffmpeg = subprocess.Popen(
        ffmpeg_cmd,
        stdin=ytdlp.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    return ffmpeg.stdout

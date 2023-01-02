from youtube_dl import YoutubeDL
from pathlib import Path


def download(url, tfn) -> Path:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tfn + ".%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    if Path(tfn).exists():
        return tfn
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if info["duration"] <= 20 * 60:
            ydl.download([url])
    return info, Path(str(tfn) + ".mp3")

from yt_dlp import YoutubeDL
from pathlib import Path

ydl_opts = lambda tfn: {
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


def download(url, tfn) -> Path:
    with YoutubeDL(ydl_opts(tfn)) as ydl:
        ydl.download([url])


def video_info(url, tfn) -> dict:
    with YoutubeDL(ydl_opts(tfn)) as ydl:
        info = ydl.extract_info(url, download=False)
    # return dict representing the downloaded video info
    return info

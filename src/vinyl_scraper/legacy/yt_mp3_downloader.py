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
    download_path = Path(str(tfn) + ".mp3")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if download_path.exists():
            return info, download_path
        ydl.download([url])
    return info, download_path

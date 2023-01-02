from youtube_dl import YoutubeDL


def download(url, tfn):
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
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if info["duration"] <= 20*60:
            ydl.download([url])
        return info

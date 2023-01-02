from youtube_dl import YoutubeDL


def download(url, tfn):
    ydl_opts = {"outtmpl": tfn + ".%(ext)s"}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if info["duration"] <= 20 * 60:
            ydl.download([url])
        return info

import vinyl_scraper
from vinyl_scraper import iterate_blog_pages, get_song_infos, download_song
from pathlib import Path
import shutil
from vinyl_scraper.legacy.mp3_info_writer import write_info

START_URL = "https://diebesondereplatte.blogspot.com/2022/12/die-besondere-platte-48-mit-simon-dorken.html"


def test_main():
    assert "hello worl" in vinyl_scraper.main()


def test_iterate_blog_pages():
    pages = iterate_blog_pages(START_URL, max_pages=2)
    assert all("http" in page["url"] for page in pages)


def test_song_infos():
    infos = [
        get_song_infos(page) for page in iterate_blog_pages(START_URL, max_pages=1)
    ]
    return len(infos[0]) > 0


def test_download():
    song_info = [
        get_song_infos(page) for page in iterate_blog_pages(START_URL, max_pages=1)
    ][0][0]

    # clean test download dir
    test_download_dir = Path("/home/pi/scm/vinyl_scraper/tests/mp3")
    if test_download_dir.exists():
        shutil.rmtree(test_download_dir)
    test_download_dir.mkdir()

    info, test_download_path = download_song(song_info, test_download_dir)
    assert test_download_path.exists()


def test_write_info():

    song_info = [
        get_song_infos(page) for page in iterate_blog_pages(START_URL, max_pages=1)
    ][0][0]

    # clean test download dir
    test_download_dir = Path("/home/pi/scm/vinyl_scraper/tests/mp3")
    if test_download_dir.exists():
        shutil.rmtree(test_download_dir)
    test_download_dir.mkdir()

    song_info["yt_info"], download_path = download_song(song_info, test_download_dir)

    # edit song info
    song_info["Album"] = "dj_title"
    write_info(song_info, download_path)

    assert download_path.exists()

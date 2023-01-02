import vinyl_scraper
from vinyl_scraper import iterate_blog_pages, get_song_infos, download_song
from pathlib import Path
import shutil


def test_main():
    assert "hello worl" in vinyl_scraper.main()


def test_iterate_blog_pages():
    pages = iterate_blog_pages(vinyl_scraper.START_URL, max_pages=2)
    assert all("http" in page["url"] for page in pages)


def test_song_infos():
    infos = [
        get_song_infos(page)
        for page in iterate_blog_pages(vinyl_scraper.START_URL, max_pages=1)
    ]
    return len(infos[0]) > 0


def test_download():
    song_info = [
        get_song_infos(page)
        for page in iterate_blog_pages(vinyl_scraper.START_URL, max_pages=1)
    ][0][0]

    # clean test download dir
    test_download_dir = Path("/Users/mfuchs/scm/vinyl_scraper/tests/mp3")
    if test_download_dir.exists():
        shutil.rmtree(test_download_dir)
    test_download_dir.mkdir()

    info = download_song(song_info, test_download_dir)
    assert True

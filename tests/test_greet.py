import vinyl_scraper
from vinyl_scraper import iterate_blog_pages, get_song_infos

START_URL = "https://diebesondereplatte.blogspot.com/2022/12/die-besondere-platte-48-mit-simon-dorken.html"


def test_app():
    vinyl_scraper.vinyl_scrape(
        "/home/pi/scm/vinyl_scraper/tests/temp_mp3",
        START_URL,
        "https://diebesondereplatte.blogspot.com/2022/11/next-date-die-besondere-platte-47-mit.html",
    )
    assert True


def test_iterate_blog_pages():
    pages = iterate_blog_pages(START_URL, "", max_pages=2)
    assert all("http" in page["url"] for page in pages)


def test_song_infos():
    infos = [
        get_song_infos(page) for page in iterate_blog_pages(START_URL, max_pages=1)
    ]
    return len(infos[0]) > 0

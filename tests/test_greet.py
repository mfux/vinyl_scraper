import vinyl_scraper
from vinyl_scraper import iterate_blog_pages


def test_main():
    assert "hello worl" in vinyl_scraper.main()


def test_iterate_blog_pages():
    urls = iterate_blog_pages(vinyl_scraper.START_URL, max_pages=2)
    assert all("http" in url for url in urls)

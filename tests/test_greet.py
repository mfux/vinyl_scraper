import vinyl_scraper
from vinyl_scraper import iterate_blog_pages


def test_main():
    assert "hello worl" in vinyl_scraper.main()


def test_iterate_blog_pages():
    text = iterate_blog_pages(vinyl_scraper.START_URL)
    assert False

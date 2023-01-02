from vinyl_scraper.legacy import link_extractor
import requests
from bs4 import BeautifulSoup
import re
import io

START_URL = "https://diebesondereplatte.blogspot.com/2022/12/die-besondere-platte-48-mit-simon-dorken.html"


def next_page(text):
    """This extract the "Older" post"""
    lines = io.StringIO(text)
    return re.findall(r"blog-pager-older-link\' href=\'(.*)\' id", lines.read())[0]


def post(text, soup):
    """This retrieves each post content"""
    lines = io.StringIO(text)
    findID = re.findall(
        r"post-body-(.*)\' itemprop", lines.read()
    )  # This retrieves each post's unique ID-number.
    div = soup.find(id="post-body-" + findID[0])
    return div


def iterate_blog_pages(start_url, max_pages=10):
    # load data
    def text_soup(url):
        r = requests.get(url)
        text = r.text
        soup = BeautifulSoup(text, "lxml")
        return text, soup

    # initialize loop
    text, soup = text_soup(start_url)
    yield {"url": START_URL, "text": text, "soup": soup}
    # loop over pages
    for i in range(max_pages):
        url = next_page(text)
        text, soup = text_soup(url)
        yield {"url": url, "text": text, "soup": soup}


def get_song_infos(page):
    return link_extractor.extract_infos(post(page["text"], page["soup"]))


def main():
    return "hello world"

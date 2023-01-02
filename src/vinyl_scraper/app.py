# from vinyl_scraper.legacy import dbpextract
import requests
from bs4 import BeautifulSoup
import re
import io

START_URL = "https://diebesondereplatte.blogspot.com/2022/12/die-besondere-platte-48-mit-simon-dorken.html"


def next_page(text):
    # This extract the "Older" post
    lines = io.StringIO(text)
    return re.findall(r"blog-pager-older-link\' href=\'(.*)\' id", lines.read())[0]


def iterate_blog_pages(start_url):
    # load data
    def text_soup(url):
        r = requests.get(url)
        text = r.text
        soup = BeautifulSoup(text, "lxml")
        return text, soup

    # initialize loop
    text, soup = text_soup(START_URL)
    result = [START_URL]
    # loop over pages
    for i in range(10):
        url = next_page(text)
        text, soup = text_soup(url)
        result.append(url)

    return result


def main():
    return "hello world"

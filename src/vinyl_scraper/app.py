from vinyl_scraper.legacy import dbpextract
import requests

START_URL = "https://diebesondereplatte.blogspot.com/2022/12/die-besondere-platte-48-mit-simon-dorken.html"


def iterate_blog_pages(start_url):
    r = requests.get(start_url)
    text = r.text
    return text


def main():
    return "hello world"

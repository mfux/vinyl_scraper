from vinyl_scraper.legacy import link_extractor, yt_mp3_downloader
from vinyl_scraper.legacy.dbpextract import get_album
from vinyl_scraper.legacy.mp3_info_writer import write_info
import requests
from bs4 import BeautifulSoup
import re
import io
from pathlib import Path
from time import sleep
import sys
import argparse
from youtube_dl.utils import DownloadError

#########
# Input #
#########


def parse_args(argv):
    """
    Runtime args parser
    """
    parser = argparse.ArgumentParser("""""")

    parser.add_argument(
        "--download-dir",
        help="",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--start-url",
        help="",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--end-url",
        help="",
        type=str,
        required=True,
    )

    args = parser.parse_args(argv[1:])

    return args


#############
# Functions #
#############


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


def iterate_blog_pages(start_url, end_url, max_pages=1000):
    # load data
    def text_soup(url):
        r = requests.get(url)
        text = r.text
        soup = BeautifulSoup(text, "lxml")
        return text, soup

    # initialize loop
    url = start_url
    text, soup = text_soup(url)
    yield {"url": url, "text": text, "soup": soup}
    # loop over pages
    for _ in range(max_pages):
        if url == end_url:
            break
        url = next_page(text)
        text, soup = text_soup(url)
        yield {"url": url, "text": text, "soup": soup}


def get_song_infos(page):
    return link_extractor.extract_infos(post(page["text"], page["soup"]))


def download_song(song_info: dict, download_dir: Path) -> Path:

    download_path = download_dir / song_info["Description"].replace("/", " ")

    info, download_path = yt_mp3_downloader.download(
        song_info["Link"], str(download_path)
    )

    return info, download_path


def vinyl_scrape(download_dir: str, start_url: str, end_url: str) -> int:
    # for each page
    for page in iterate_blog_pages(start_url, end_url):

        # get dj title
        dj_title = get_album(page["url"])

        # for song in page
        for song_info in get_song_infos(page):
            # download song
            try:
                song_info["yt_info"], download_path = download_song(
                    song_info, Path(download_dir)
                )
            except DownloadError:
                continue

            # edit downloaded song info
            song_info["Album"] = dj_title
            write_info(song_info, download_path)

        # throttle requests
        sleep(1)

    return 0


#################
#     MAIN      #
#################


def main():
    # parse args
    args = parse_args(sys.argv)
    return vinyl_scrape(args.download_dir, args.start_url, args.end_url)


if __name__ == "__main__":
    sys.exit(main())

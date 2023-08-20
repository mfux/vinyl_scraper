import requests

"""
This script scrapes a Blogspot blog by iterating back in its history.
Usage:
    1. Set url variable to the Blogspot URL you want as point of departure.
    2. Press CTRL-C when you want to stop it.
Note: Your IP-number may be temporarily banned from the Blogger service if over-used.
Use on your own risk.
"""

import requests
import io
import re
from bs4 import BeautifulSoup
from time import sleep
from vinyl_scraper.legacy.link_extractor import extract_infos
from vinyl_scraper.legacy.yt_mp3_downloader import download
from vinyl_scraper.legacy.mp3_info_writer import write_info
from vinyl_scraper.assets import page_number_artist_map
from pathlib import Path


def get_html(page):
    url = "https://diebesondereplatte.blogspot.com/2018/11/next-date-die-besondere-platte-31-mit.html"
    counter = 0
    tfn = ""
    next_url = url
    while counter < page:
        url = next_url  # This changes the variable in the beginning of the script
        r = requests.get(url)
        file_like_obj = io.StringIO(
            r.text
        )  # Turns the requested output into a file like objet
        lines = file_like_obj.read()

        soup = BeautifulSoup(lines, "lxml")
        findID = re.findall(
            r"post-body-(.*)\' itemprop", lines
        )  # This retrieves each post's unique ID-number.
        # print(findID[0])  # for debugging
        div = soup.find(id="post-body-" + findID[0])  # This retrieves each post content
        # print(div)
        if counter == page - 1:
            tfn = "html/" + str(counter + 1) + ".html"
            with open(tfn, "w") as outputfile:  # open file
                outputfile.write(str(div))  # write to file
        matchObj = re.findall(
            r"blog-pager-older-link\' href=\'(.*)\' id", lines
        )  # This extract the "Older" post
        next_url = matchObj[0]
        print("Next URL for scraping: " + next_url)
        counter += 1  # Update the counter from proper filenames

    return url, tfn


def get_album(url):
    nr_map = page_number_artist_map()
    try:
        dbp_nr = [s for s in url.split("-") if s.isdigit()][-1]
    except IndexError:
        return nr_map["27"]

    try:
        result = nr_map[dbp_nr]
    except KeyError:
        result = nr_map["27"]
    return result


def main():
    for i in range(1, 35):
        if i == 3 or i == 8:
            continue
        tfn = "html/" + str(i) + ".html"
        url, tfn = get_html(i)
        with open(tfn, "r") as f:
            infos = extract_infos(f)

            for info in infos:
                info["Album"] = get_album(url)
                print("File: " + info["Description"] + "...")
                if Path(
                    "mp3/" + info["Description"].replace("/", " ") + ".mp3"
                ).exists():
                    try:
                        write_info(
                            info,
                            "mp3/" + info["Description"].replace("/", " ") + ".mp3",
                        )
                    except (IOError, AttributeError, IndexError):
                        continue
                    continue
                try:
                    yt_info = download(
                        info["Link"], "mp3/" + info["Description"].replace("/", " ")
                    )
                except:
                    continue
                info["yt_info"] = yt_info
                try:
                    write_info(
                        info, "mp3/" + info["Description"].replace("/", " ") + ".mp3"
                    )
                except (IOError, AttributeError, IndexError):
                    continue
                sleep(1)

from bs4 import BeautifulSoup
from pprint import pprint


def has_listen(tag):
    return "listen" in tag.get_text().lower()


def get_description_and_number(a):
    for element in a.next_elements:
        if "." in element or "-" in element:
            i = 0
            while element[i] != ".":
                i += 1
                if i >= len(element):
                    i = 0
                    break
            n = element[:i].strip()
            try:
                num = int(n)
            except ValueError:
                num = 27
            valid_schars = ["–", "-", " ", "(", ")"]
            return [
                "".join(e for e in element[i + 1 :] if e.isalnum() or e in valid_schars)
                .strip()
                .replace("–", "-"),
                num,
            ]
    return "no-description"


def get_link(a):
    return str(a.get("href"))


def get_img(a):
    return a.find_previous(lambda tag: tag.has_attr("href")).get("href")


def extract_infos(soup):
    listen_as = [tag for tag in soup.find_all("a") if has_listen(tag)]
    infos = []
    for a in listen_as:
        info = {
            "Description": get_description_and_number(a)[0],
            "Number": get_description_and_number(a)[1],
            "Link": get_link(a),
            "Image": get_img(a),
        }
        infos.append(info)
    result = infos
    return result

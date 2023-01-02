import eyed3
import urllib.request
from subprocess import check_output
from pathlib import Path


def get_img(link, tfn):
    urllib.request.urlretrieve(link, tfn)
    print("retreived link")
    return tfn


def get_artist(info):
    try:
        if info["yt_info"]["artist"]:
            return info["yt_info"]["artist"].replace("\\", "")
    except KeyError:
        pass

    # extract artist from description
    d = info["Description"]
    d = "".join(
        [char for char in d[:4] if char not in ["."] and not char.isdigit()]
        + list(d)[4:]
    )
    d = d.strip()
    artist = d.split("-")[0].strip()
    return artist


def get_title(info):
    try:
        if info["yt_info"]["title"] and "-" not in info["yt_info"]["title"]:
            return info["yt_info"]["title"].replace("\\", "")
    except KeyError:
        pass
    # extract artist from description
    d = info["Description"]
    d = "".join(
        [char for char in d[:4] if char not in ["."] and not char.isdigit()]
        + list(d)[4:]
    )
    d = d.strip()
    try:
        artist = d.split("-")[1].strip()
    except IndexError:
        artist = "unknown"
    return artist


def write_info(info, tfn, jpeg=False):
    filetype = info["Image"].split(".")[-1]
    img_tfn = "img/" + info["Description"] + "." + filetype
    img_tfn = Path(img_tfn).resolve()
    try:
        get_img(info["Image"], img_tfn)
        r = check_output(
            ["eyeD3", "--add-image", ":".join([str(img_tfn), "FRONT_COVER"]), tfn]
        )
        print(r)
    except:
        pass
    audiofile = eyed3.load(tfn)
    audiofile.tag.artist = get_artist(info)
    audiofile.tag.title = get_title(info)
    audiofile.tag.track_num = info["Number"]
    audiofile.tag.album = info["Album"]
    audiofile.tag.save()

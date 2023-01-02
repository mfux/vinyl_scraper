import re
import nltk

with open("/home/maximilian/Desktop/test/besonderePlattenHTML.txt/dbp.txt") as f:
       raw = f.readlines()

linklines = [line for line in raw if "youtu" in line]
linklines[441]
strippedlines = [re.findall('https.*"', line)[0] for line in linklines]
links = [line[:-17] for line in strippedlines]
links[441] = "https://youtu.be/rNIeuiRnr_k"
links[59] = 'https://youtu.be/ys0HyevZpQg'
links[369] = 'https://youtu.be/jmBNeqNZDDE'
links[-1] = "https://youtu.be/iRgLhEGEetc"
linkIDs = [link[-11:] for link in links]
len(linkIDs)
goodLinks = ["https://youtube.com/v/" + linkID for linkID in linkIDs]
len(goodLinks)
f = open('/home/maximilian/Desktop/test/besonderePlattenHTML.txt/links.txt', 'w')
for link in goodLinks:
    f.write(link + '\n')  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it


playlist_url = "http://www.youtube.com/watch_videos?video_ids="
for linkID in linkIDs:
    playlist_url += linkID + ","

playlist_url

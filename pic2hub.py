#!/usr/bin/env python3

import os
import sys
import time
import subprocess
from urllib.parse import unquote, quote
from asyncio.subprocess import DEVNULL
from PIL import Image
import re

def upload(images):
    for image in images:
        if image.startswith("http"):
            continue
        image = unquote(image)
        if os.path.isfile(image):
            createdate = time.localtime(os.stat(image).st_birthtime)
            year = createdate.tm_year
            month = createdate.tm_mon
            dstpath = f"/Users/waderwu/blog-img/{year}/{month}"
            if not os.path.isdir(dstpath):
                os.makedirs(dstpath)
            imgname = os.path.basename(image)
            webp = f"{dstpath}/{imgname}.webp"
            Image.open(image).convert("RGB").save(webp, "webp")
        else:
            print(f"{image} not found")
        
def getImageOfMd(mdfile):
    if not os.path.isfile(mdfile):
        return []
    basedir = os.path.dirname(mdfile)
    os.chdir(basedir)
    with open(mdfile, "r") as f:
        content = f.read()
    # print(content)
    images = re.findall(r'!\[.*\]\((.*)\)', content)
    print(images)
    for image in images:
        if not image.startswith("http"):
            unquote_image = unquote(image)
            if os.path.isfile(unquote_image):
                createdate = time.localtime(os.stat(unquote_image).st_birthtime)
                year = createdate.tm_year
                month = createdate.tm_mon
                imgname = os.path.basename(unquote_image)
                imgurl = f"https://blog.sometimenaive.com/blog-img/{year}/{month}/{quote(imgname)}.webp"
                content = content.replace(image, imgurl)
            else:
                print(f"{image} not found")
    with open(mdfile, "w") as f:
        f.write(content)
    return images

def getUpdatedFile():
    out = subprocess.check_output(["git", "status", "-s"])
    lines = out.decode().split("\n")[:-1]
    files = []
    for line in lines:
        _, filename = line.split()
        if filename.endswith(".md"):
            files.append(filename)
    return files



if __name__ == "__main__":
    #upload(images)
    files = []
    if (len(sys.argv) > 1) :
        files.append(sys.argv[1]) 
    else:
        files = getUpdatedFile()
    
    print(files)
    for md in files:
        try:
            images = getImageOfMd(md)
            # print(md)
            # print(images)
            upload(images)
        except Exception as e:
            print(e)
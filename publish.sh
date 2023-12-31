#!/bin/bash
echo "upload local img"
python3 pic2hub.py
cd /Users/waderwu/blog-img/
git pull
git add . 
git commit -m 'upload image'
git push
git pull

echo "upload blog"
cd /Users/waderwu/blog/
git add . 
git commit -m "update blog"
git push

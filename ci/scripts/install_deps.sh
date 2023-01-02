#!/bin/bash

# check if virtual environment exists and set up if it doesn't
[ ! -d ".env" ] && python3 -m venv .env

# execute the following commands within the virtual environment
# i.e. install dependencies in virtual environment instead of globally on the executing system
source .env/bin/activate

# update pip in venv
python -m pip install --upgrade pip

# install packaged src code 
pip install --editable .
# puts references to src code in env/lib/python3.9/site-packages/main.egg-link
# the site-packages directory is the where the interpreter will look at first(?) when resolving an import

sudo apt-get install ffmpeg
# brew install ffmpeg

# print package installations in env
echo # print newline

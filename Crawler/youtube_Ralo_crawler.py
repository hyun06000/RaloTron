# URL crawler
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# audio source crawler
import pytube
import os
import re
import subprocess


def get_audio_from_url(url):
    # cf. https://jun-itworld.tistory.com/37?category=954968
    
    # set target url
    youtube_url = "https://www.youtube.com" + url
    
    # make pytube
    yt = pytube.YouTube(youtube_url)
    
    # get video from
    download_dir = './data/'
    downloaded_fname = yt.streams \
                        .filter(only_audio=True) \
                        .order_by("abr") \
                        .first() \
                        .download(download_dir)
    
    ori_fname = downloaded_fname
    new_fname = downloaded_fname[:-5] + ".wav"

    new_fname = re.sub(" ","_",new_fname)
    
    # ffmpeg should be installed
    subprocess.call(["ffmpeg", "-y", "-i", ori_fname, new_fname])
    

# cf. https://pbj0812.tistory.com/255

# Channel Ralo
Ralo_url = "https://www.youtube.com/channel/UCD2YO_A_PVMgMDN9jpRrpVA/videos"

# Headless chrome in CLI
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--no-sandbox')

# run chromedriver with options
w_driver = webdriver.Chrome('./chromedriver', chrome_options = options)

# get page source
w_driver.get(Ralo_url)
page_src = w_driver.page_source

# parsing
soup = BeautifulSoup(page_src,"lxml")
tags = soup.find_all("a", {"href": True})

for i in tags:
    if i.get("href")[:7] == "/watch?":
        get_audio_from_url(i.get("href"))

print("done")

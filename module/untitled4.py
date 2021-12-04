# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 16:19:18 2021

@author: jd025
"""

from linebot.models import FlexSendMessage

import requests
from bs4 import BeautifulSoup
import random
imgs=["https://i.imgur.com/VLPfJzt.jpg","https://i.imgur.com/6ENxTV4.jpg","https://i.imgur.com/BrwvyHu.jpg","https://i.imgur.com/IoPTVBE.jpg","https://i.imgur.com/MWl7oJa.jpg","https://i.imgur.com/1j3qUjh.jpg","https://i.imgur.com/peoFZNN.jpg","https://i.imgur.com/6d1kKIL.jpg"]    

htmllist=[]
namelist=[]
url = "https://tw.stock.yahoo.com/news"
print(url)
html = requests.get(url).text
soup = BeautifulSoup(html, "lxml")

count=0
for i in range(80,110):
    if soup.select('a')[i]['href'][:32] == 'https://tw.stock.yahoo.com/news/':
        htmllist.append(soup.select('a')[i]['href'])
        namelist.append(soup.select('a')[i].text)
print(htmllist)
print(namelist)
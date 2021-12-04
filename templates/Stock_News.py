from linebot.models import FlexSendMessage

import requests
from bs4 import BeautifulSoup
import random
imgs=['https://i.imgur.com/VLPfJzt.jpg','https://i.imgur.com/6ENxTV4.jpg','https://i.imgur.com/BrwvyHu.jpg','https://i.imgur.com/IoPTVBE.jpg','https://i.imgur.com/MWl7oJa.jpg','https://i.imgur.com/1j3qUjh.jpg','https://i.imgur.com/peoFZNN.jpg','https://i.imgur.com/6d1kKIL.jpg']

def single_stock(stockNumber):

    htmllist=[]
    namelist=[]
    url = f'https://tw.stock.yahoo.com/quote/{stockNumber}/news'
    print(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    temp=soup.select("h3")

    #temp[2].select('a')[0]['href']

    for i in range(1,10):
        if temp[i].select('a')[0]['href'][:32] == 'https://tw.stock.yahoo.com/news/':
            htmllist.append(temp[i].select('a')[0]['href'])
            namelist.append(temp[i].select('a')[0].text)
    print(htmllist)
    print(namelist)
    img=imgs[random.randint(0, 7)]
    flex_message1 = FlexSendMessage(

            alt_text="個股新聞",
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": img,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "position": "relative",
                    "margin": "none"
                },
                
       
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": str(stockNumber+"財金新聞"),
                        "weight": "bold",
                        "size": "xl",
                        "style": "normal"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[0],
                        "uri": htmllist[0]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[1],
                        "uri": htmllist[1]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[2],
                        "uri": htmllist[2]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[3],
                        "uri": htmllist[3]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[4],
                        "uri": htmllist[4]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": "更多資訊...",
                        "uri":str(f'https://tw.stock.yahoo.com/quote/{stockNumber}/news')
                    }
                        }
                    ],
                    "flex": 0
                }
                }
        )


    if len(html)>=4:
        return flex_message1
    else: print('發生錯誤')


# 其他財金新聞

def all_stock():
    htmllist=[]
    namelist=[]
    url = "https://tw.stock.yahoo.com/news"
    print(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    for i in range(80,110):
        if soup.select('a')[i]['href'][:32] == 'https://tw.stock.yahoo.com/news/':
            htmllist.append(soup.select('a')[i]['href'])
            namelist.append(soup.select('a')[i].text)
    print(htmllist)
    print(namelist)
    img=imgs[random.randint(0, 7)]
    print(img)
    flex_message = FlexSendMessage(
            alt_text="財金新聞",
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": img,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "fit",
                    "position": "relative",
                    "margin": "none"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "最新消息",
                        "weight": "bold",
                        "size": "xl",
                        "style": "normal"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[0],
                        "uri": htmllist[0]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[1],
                        "uri": htmllist[1]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[2],
                        "uri": htmllist[2]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[3],
                        "uri": htmllist[3]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": namelist[4],
                        "uri": htmllist[4]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": "更多資訊...",
                        "uri":'https://tw.stock.yahoo.com/news'
                    }
                        }
                    ],
                    "flex": 0
                }
                }
        )

    if len(htmllist)>=4:
        return flex_message
    else: print('發生錯誤')

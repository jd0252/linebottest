from linebot.models import FlexSendMessage

import requests
from bs4 import BeautifulSoup
import random
imgs=["https://i.imgur.com/HXz0FaE.jpg","https://i.imgur.com/BrwvyHu.jpg","https://i.imgur.com/IoPTVBE.jpg","https://i.imgur.com/MWl7oJa.jpg","https://i.imgur.com/1j3qUjh.jpg","https://i.imgur.com/peoFZNN.jpg","https://i.imgur.com/6d1kKIL.jpg"]    


    
def single_stock(stockNumber):
    htmllist1=[]
    namelist1=[]
    print(htmllist1,namelist1)
    stock=str(stockNumber).strip("")
    url = "https://tw.stock.yahoo.com/q/h?s="+stock
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    x=soup.find_all('tr')[4]
    y=x.find_all('a')
    for i in y:
        x=str(i)
        z=x.split('"')[1]
        z='https://tw.stock.yahoo.com'+z
        htmllist1.append(z)
        a=x.split('>')
        b=a[1].strip('</a')
        namelist1.append(b)
        print(z,b)
    print(htmllist1,namelist1)
    for i in htmllist1:
        print(len(i))
    img=imgs[random.randint(0, 6)]
    
    flex_message = FlexSendMessage(
            alt_text="個股新聞",
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
                        "text": "財金新聞",
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
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": htmllist1[0],
                        "uri": namelist1[0]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": htmllist1[1],
                        "uri": namelist1[1]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label":q=htmllist1[5],
                        "uri":namelist1[5]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": htmllist1[3],
                        "uri": namelist1[3]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": htmllist1[4],
                        "uri": namelist1[4]
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "xs",
                        "action": {
                        "type": "uri",
                        "label": "更多資訊...",
                        "uri":'https://tw.stock.yahoo.com/q/h?s='+stockNumber
                        }
                    },
                    
                    ],
                    "flex": 0
                }
                }
        )
    if len(htmllist1)>=4:
        return flex_message
    else: print('發生錯誤')   

# 其他財金新聞
    
def all_stock():
    htmllist=[]
    namelist=[]
    url = 'https://tw.stock.yahoo.com/news'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    x=soup.find_all('a',class_='D(ib) Ov(h) Whs(nw) C($c-primary-text) C($c-active-text):h Td(n) Fz(16px) Tov(e) W($ABUHeroListItemWidth) Maw(265px)')
    for i  in x:
        z=str(i)
        a=z.split('href=')[1]
        a=a.strip('</a>').strip('"')
        z=str(i)
        a=z.split('href=')[1]
        a=a.strip('</a>')
        a=a.split('>')
        html='https://tw.stock.yahoo.com'+a[0].strip('"')
        htmllist.append(html)
        namelist.append(a[1])
    img=imgs[random.randint(0, 6)]
    for i in htmllist:
        print(len(i))
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
  
    





def stocknews(stocksymbol):
    try:
        print('1456')
        stock=str(stocksymbol).strip("")
        url = "https://tw.stock.yahoo.com/q/h?s="+stock
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        x=soup.findAll('tr')[4]
        y=x.find_all('a')
        htmllist2=[]
        namelist2=[]
        for i  in y:
            x=str(i)
            z=x.split('"')[1]
            z='https://tw.stock.yahoo.com'+z
            htmllist2.append(z)
    
            a=x.split('>')
            b=a[1].strip('</a')
            namelist2.append(b)
        if len(htmllist2)>=4:
           return namelist2,htmllist2
        else: print('發生錯誤')
    except:
        print('發生錯誤')
        
    

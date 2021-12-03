# -*- coding: utf-8 -*-
''' 
即時股價
'''
import requests
import datetime
import json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pandas_datareader as pdr
#import Imgur
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
import datetime
from imgurpython import ImgurClient

#from matplotlib.font_manager import FontProperties # 設定字體
#font_path = matplotlib.font_manager.FontProperties(fontsize=40)#fname='msjh.ttf'
#plt.rcParams['font.sans-serif'] = ['SimHei']


client_id = '07f1098efd49fcb'
client_secret = 'c802e2b89ad38a83341f53148a41058c65a65d42'
album_id = '817ZzND'
access_token = '0409f8c9d920da65fc8bb9c3ec5b029c4dc4869c'
refresh_token = 'dd279237af22c09c879a84105e209e13bff5e227'


#fname=r"C:\Users\jd025\Fin\linebotInvoice\module\msjh.ttf"



def get_stock_name(stockNumber):
    try:
        stockNumber='2330'
        url = f'https://histock.tw/stock/chips.aspx?no={stockNumber}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        stock_name=soup.title.string.split(" ")[0]
        return stock_name
    except:
        return "no"
    
    
def getprice(stockNumber):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no": return "股票代碼錯誤!"
    content = ""
    stock = pdr.DataReader(stockNumber+'.TW', 'yahoo',  end=datetime.datetime.now())
    date = stock.index[-1]
    price = '%.2f ' % stock["Close"][-1] # 近日之收盤價
    last_price = '%.2f ' % stock["Close"][-2] # 前一日之收盤價
    spread_price = '%.2f ' % (float(price) - float(last_price)) # 價差
    spread_ratio = '%.2f ' % (float(spread_price) / float(last_price)) # 漲跌幅
    spread_price = spread_price.replace("-",'▽ ') if last_price > price else '△ ' + spread_price
    spread_ratio = spread_ratio.replace("-",'▽ ') if  last_price > price else '△ ' + spread_ratio
    open_price = str('%.2f ' % stock["Open"][-1]) # 近日之開盤價
    high_price = str('%.2f ' % stock["High"][-1])# 近日之盤中高點
    low_price = str('%.2f ' % stock["Low"][-1]) # 近日之盤中低點
    price_five = stock.tail(5)["Close"] # 近五日之收盤價
    stockAverage = str('%.2f ' % pd.to_numeric(price_five).mean())  # 計算近五日平均價格
    stockSTD = str('%.2f ' % pd.to_numeric(price_five).std())   # 計算近五日標準差  
    content += f"回報編號{stockNumber}{stock_name}的股價\n--------------\n日期: {date}\n最新收盤價: {price}\n開盤價{open_price}\n最高價: \
    {high_price}\n最低價: {low_price}\n價差: {spread_price} 漲跌幅: {spread_ratio}\n近五日平均價格: {stockAverage}\n近五日標準差: {stockSTD}\n" 
    return content

# --------- 畫近一年股價走勢圖
def stock_trend(stockNumber):
    stock_name = get_stock_name(stockNumber)
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber+'.TW', 'yahoo', start= year+"-"+month,end=end)
    plt.figure(figsize=(20, 12))
    plt.plot(stock["Close"], '-' , label="Close")
    plt.plot(stock["High"], '-' , label="High")
    plt.plot(stock["Low"], '-' , label="Low")
    plt.title(stockNumber + ' Annual trend of closing price',loc='center', fontsize=60,fontweight='bold')#, fontproperties=font_path)# loc->title的位置
    plt.xlabel('Date', fontsize=40)#, fontproperties=font_path)
    plt.ylabel('Price', fontsize=40)#, fontproperties=font_path)
    plt.grid(True, axis='y') # 網格線
    plt.legend(fontsize=20)#, prop=font_path)
    plt.savefig(stockNumber+'stock_trend.png') #存檔
    print('作圖ing')
    plt.show()
    #plt.close() 
    return showImgur(str(stockNumber+'stock_trend'))
#股票收益率: 代表股票在一天交易中的價值變化百分比
    



def show_return(stockNumber):
    stock_name = get_stock_name(stockNumber)
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber+'.TW', 'yahoo', start= year+"-"+month,end=end)
    print(stock)
    stock['Returns'] = stock['Close'].pct_change()
    print(stock['Returns'])
    stock_return = stock['Returns'].dropna()
    print(stock_return)
    plt.figure(figsize=(20, 12))
    plt.plot(stock_return, label="Return")
    plt.title(stockNumber + '  Annual trend of return ',loc='center', fontsize=60,fontweight='bold')#,, fontproperties=font_path)# loc->title的位置
    plt.xlabel('Date', fontsize=40)#, fontproperties=font_path)
    plt.ylabel('Return', fontsize=40)#, fontproperties=font_path)
    plt.grid(True, axis='y') # 網格線
    plt.legend(fontsize=20)#, prop=font_path)
    plt.savefig(stockNumber+'show_return') #存檔
    #plt.show()
    #plt.close()
    return showImgur(str(stockNumber+'show_return'))

# --------- 畫  股價震盪圖
def show_fluctuation(stockNumber):
    
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber+'.TW', 'yahoo', start= year+"-"+month,end=end)
    stock['stock_fluctuation'] = stock["High"] - stock["Low"]
    max_value = max(stock['stock_fluctuation'][:]) # 最大價差
    min_value = min(stock['stock_fluctuation'][:]) # 最小價差
    plt.figure(figsize=(20, 12))
    plt.plot(stock['stock_fluctuation'], '-' , label="Volatility", color="orange")
    plt.title(stockNumber + 'Annual volatility of closing price',loc='center', fontsize=60,fontweight='bold')#, fontproperties=font_path)# loc->title的位置
    plt.xlabel('Date', fontsize=40)#, fontproperties=font_path)
    plt.ylabel('Price', fontsize=40)#, fontproperties=font_path)
    plt.grid(True, axis='y') # 網格線
    plt.legend(fontsize=20)#, prop= font_path)
    plt.savefig(stockNumber + 'show_fluctuation') #存檔
    print('123')
    plt.show()
    #plt.close() 
    return showImgur(stockNumber + 'show_fluctuation')


def showImgur(fileName):
        print('連接imgur')
        # 連接imgur
        client= ImgurClient(client_id, client_secret, access_token, refresh_token)
    
        # 連接需要的參數
        config = {
            'album': album_id, # 相簿名稱
            'name': fileName, # 圖片名稱
            'title': fileName, # 圖片標題
            'description': str(datetime.date.today()) # 備註，這邊打日期時間
            }
        
        # 開始上傳檔案
        try:
            print("[log:INFO]Uploading image... ")
            imgurl = client.upload_from_path(fileName+'.png', config=config, anon=False)['link']
            #string to dict
            print("[log:INFO]Done upload. ")
            print(imgurl)
        except :
            # 如果失敗回傳"失敗"這張圖
            imgurl = 'https://i.imgur.com/M7UAm4J.jpg'
            print("[log:ERROR]Unable upload ! ")
            
        
        return imgurl


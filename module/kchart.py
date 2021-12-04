# basic
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import datetime
from imgurpython import ImgurClient
# get data
import pandas_datareader as pdr

# visual
import matplotlib
import matplotlib.pyplot as plt
#import mpl_finance as mpf
import pandas_datareader as pdr
# import seaborn as sns 
from bs4 import BeautifulSoup
#time
import datetime as datetime

#talib
import talib
import pandas as pd
import requests,datetime

client_id = '07f1098efd49fcb'
client_secret = 'c802e2b89ad38a83341f53148a41058c65a65d42'
album_id = '817ZzND'
access_token = '0409f8c9d920da65fc8bb9c3ec5b029c4dc4869c'
refresh_token = 'dd279237af22c09c879a84105e209e13bff5e227'

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
        except :
            # 如果失敗回傳"失敗"這張圖
            imgurl = 'https://i.imgur.com/M7UAm4J.jpg'
            print("[log:ERROR]Unable upload ! ")
            
        
        return imgurl


def get_stock_name(stockNumber):
    try:
        url = f'https://histock.tw/stock/chips.aspx?no={stockNumber}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        stock_name=soup.title.string.split(" ")[0]
        return stock_name
    except:
        return "no"


def draw_kchart(stockNumber):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no": return "股票代碼錯誤!"
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber + '.TW', 'yahoo', start= year+"-"+month,end=end)
    stock.index = stock.index.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    #KD
    stock['k'], stock['d'] = talib.STOCH(stock['High'], stock['Low'], stock['Close'])
    stock['k'].fillna(value=0, inplace=True)
    stock['d'].fillna(value=0, inplace=True)
    sma_5 = talib.SMA(np.array(stock['Close']), 5)
    sma_10 = talib.SMA(np.array(stock['Close']), 10)
    sma_20 = talib.SMA(np.array(stock['Close']), 20)
    sma_30 = talib.SMA(np.array(stock['Close']), 30)
    fig = plt.figure(figsize=(20, 10))#,facecolor='black')
    fig.suptitle(stockNumber,fontsize=70)
    ax = fig.add_axes([0.1,0.5,0.75,0.4])
    plt.title("Open:"+str(round(stock['Open'][-1], 2))+"  Close:"+str(round(stock['Close'][-1], 2))+"\n High:" +str(round(stock['High'][-1] ,2))+"    Low:"+str(round(stock['Low'][-1], 2)),fontsize="25",fontweight='bold',bbox=dict(facecolor='yellow',edgecolor='red',alpha=0.65),loc='left')
    plt.title("Date:"+stock.index[-1],fontsize="20",fontweight='bold',loc="right")
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')

    ax2 = fig.add_axes([0.1,0.3,0.75,0.20])
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    ax.plot(stock['Close'], label='Close')
    ax.plot(sma_5, label='5MA')
    ax.plot(sma_20, label='20MA')
    ax.plot(sma_30, label='30MA')

    ax2.plot(stock['k'], label='K')
    ax2.plot(stock['d'], label='D')
    ax2.set_xticks(range(0, len(stock.index),10))
    ax2.set_xticklabels(stock.index[::10],fontsize="10", rotation=25)
    
    
    ax.legend( fontsize=20)
    ax2.legend(fontsize='16',loc ='upper left')
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    plt.gcf()
    plt.savefig("Kchrat.png",bbox_inches='tight',dpi=300,pad_inches=0.0)
    plt.show()
    #plt.close()
    return showImgur("Kchrat")

def draw_MACDchart(stockNumber):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no": return "股票代碼錯誤!"
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber + '.TW', 'yahoo', start= year+"-"+month,end=end)
    stock.index = stock.index.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    #MACD
    stock['MACD'],stock['MACDsignal'],stock['MACDhist'] = talib.MACD(stock['Close'],fastperiod=6, slowperiod=12, signalperiod=9)
    stock['MACD'].fillna(value=0, inplace=True)
    stock['MACDsignal'].fillna(value=0, inplace=True)
    
    
    
    sma_5 = talib.SMA(np.array(stock['Close']), 5)
    sma_10 = talib.SMA(np.array(stock['Close']), 10)
    sma_20 = talib.SMA(np.array(stock['Close']), 20)
    sma_30 = talib.SMA(np.array(stock['Close']), 30)
    fig = plt.figure(figsize=(20, 10))#,facecolor='black')
    fig.suptitle(stockNumber,fontsize=70)
        
    ax = fig.add_axes([0.1,0.5,0.75,0.4])
    plt.title("Open:"+str(round(stock['Open'][-1], 2))+"  Close:"+str(round(stock['Close'][-1], 2))+"\n High:" +str(round(stock['High'][-1] ,2))+"    Low:"+str(round(stock['Low'][-1], 2)),fontsize="25",fontweight='bold',bbox=dict(facecolor='yellow',edgecolor='red',alpha=0.65),loc='left')
    plt.title("Date:"+stock.index[-1],fontsize="20",fontweight='bold',loc="right")
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    ax.plot(stock['Close'], label='Close')
    ax.plot(sma_5, label='5MA')
    ax.plot(sma_20, label='20MA')
    ax.plot(sma_30, label='30MA')
    
    ax2 = fig.add_axes([0.1,0.3,0.75,0.20])
    
    ax2.plot(stock['MACD'], label='MACD')
    ax2.plot(stock['MACDsignal'], label='MACDsignal')
    ax2.fill_between(stock.index,0,stock['MACDhist'])
    ax2.set_xticks(range(0, len(stock.index),10))
    ax2.set_xticklabels(stock.index[::10],fontsize="10", rotation=25)
    
    

    ax.legend( fontsize=20);
    ax2.legend(fontsize=15,loc ='upper left');
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    plt.gcf()
    plt.savefig("MACDchrat.png",bbox_inches='tight',dpi=300,pad_inches=0.0)
    plt.show()
    #plt.close()
    return showImgur("MACDchrat")


def draw_RSIchart(stockNumber):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no": return "股票代碼錯誤!"
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber + '.TW', 'yahoo', start= year+"-"+month,end=end)
    stock.index = stock.index.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    #MACD
    stock['MACD'],stock['MACDsignal'],stock['MACDhist'] = talib.MACD(stock['Close'],fastperiod=6, slowperiod=12, signalperiod=9)
    stock['MACD'].fillna(value=0, inplace=True)
    stock['MACDsignal'].fillna(value=0, inplace=True)
    
    
    
    sma_5 = talib.SMA(np.array(stock['Close']), 5)
    sma_10 = talib.SMA(np.array(stock['Close']), 10)
    sma_20 = talib.SMA(np.array(stock['Close']), 20)
    sma_30 = talib.SMA(np.array(stock['Close']), 30)
    fig = plt.figure(figsize=(20, 10))#,facecolor='black')
    fig.suptitle(stockNumber,fontsize=70)
    
    
    
    
    ax = fig.add_axes([0.1,0.5,0.75,0.4])
    plt.title("Open:"+str(round(stock['Open'][-1], 2))+"  Close:"+str(round(stock['Close'][-1], 2))+"\n High:" +str(round(stock['High'][-1] ,2))+"    Low:"+str(round(stock['Low'][-1], 2)),fontsize="25",fontweight='bold',bbox=dict(facecolor='yellow',edgecolor='red',alpha=0.65),loc='left')
    plt.title("Date:"+stock.index[-1],fontsize="20",fontweight='bold',loc="right")
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')

    
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    #ax3 = fig.add_axes([0.1,0.03,0.75,0.20])
    #mpf.candlestick2_ochl(ax, stock['Open'], stock['Close'], stock['High'],stock['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
    
    ax.plot(stock['Close'], label='Close')
    ax.plot(sma_5, label='5MA')
    ax.plot(sma_20, label='20MA')
    ax.plot(sma_30, label='30MA')
    
    ax2 = fig.add_axes([0.1,0.3,0.75,0.20])
    stock['RSI']  =talib.RSI(stock['Close'],timeperiod=12)
    ax2.plot(stock['RSI'], label='RSI')
    
    
    line = plt.axhline(80, color= 'r', linewidth=2, linestyle="-" ,label='RSI80')
    line.set_dashes((20,2))
    line1 = plt.axhline(30, color= 'g', linewidth=2, linestyle="-" ,label='RSI30')
    line1.set_dashes((20,2))
    
    
    ax2.set_xticks(range(0, len(stock.index),10))
    ax2.set_xticklabels(stock.index[::10],fontsize="10", rotation=25)
    
    
    ax.legend( fontsize=20);
    ax2.legend(fontsize=15,loc ='upper left');
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    plt.gcf()
    plt.savefig("RSIchrat.png",bbox_inches='tight',dpi=300,pad_inches=0.0)
    plt.show()
    #plt.close()
    return showImgur("RSIchrat")
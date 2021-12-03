''' 
三大法人買賣超
'''
#繪圖用

import requests
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd


# 三大法人買賣超(純文字敘述)
def institutional_investors(stockNumber):
    stockNumber=str(stockNumber)
    x= requests.get("https://www.twse.com.tw/fund/T86")
    soup = BeautifulSoup(x.text, "html.parser")
    title=str(soup).split(',')[2].split('"')[3]
    r = requests.get('https://www.twse.com.tw/fund/T86?response=csv&date&selectType=ALLBUT0999')
    df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any') 
        
    columns = len(df["證券代號"])-1
    for i in range(columns):
        if str(df["證券代號"][i])[0]=='=':
            df["證券代號"][i]=df["證券代號"][i].split('"')[1]  
        stockCode = df["證券代號"][i]
        if stockCode == stockNumber: # or len(df["證券代號"][i])>4 and stockCode = df["證券代號"][i][:-1]:
             
            #print(df["證券代號"][i])
            content = df["證券名稱"][i]+stockNumber+ "\n"+title+ "\n\n"+ "外陸資買進張數(不含外資自營商): " + str(round(int(df["外陸資買進股數(不含外資自營商)"][i].replace(',',''))/1000))+"張\n"
            content += "外陸資賣出張數(不含外資自營商): " + str(round(int(df["外陸資賣出股數(不含外資自營商)"][i].replace(',',''))/1000))+"張\n"
            content += "外陸資買賣超張數(不含外資自營商): " + str(round(int(df["外陸資買賣超股數(不含外資自營商)"][i].replace(',',''))/1000))+"張\n--------------------------\n"
            content += "投信買進張數: " + str(round(int(df["投信買進股數"][i].replace(',',''))/1000))+"張\n"
            content += "投信賣出張數: " + str(round(int(df["投信賣出股數"][i].replace(',',''))/1000))+"張\n"
            content += "投信買賣超張數: " + str(round(int(df["投信買賣超股數"][i].replace(',',''))/1000))+"張\n--------------------------\n"
            content += "自營商買進張數(自行買賣): " + str(round(int(df["自營商買進股數(自行買賣)"][i].replace(',',''))/1000))+"張\n"
            content += "自營商賣出張數(自行買賣): " + str(round(int(df["自營商賣出股數(自行買賣)"][i].replace(',',''))/1000))+"張\n"
            content += "自營商買賣超張數(自行買賣): " + str(round(int(df["自營商買賣超股數(自行買賣)"][i].replace(',',''))/1000))+"張\n--------------------------\n"
            content += "自營商買進張數(避險): " + str(round(int(df["自營商買進股數(避險)"][i].replace(',',''))/1000))+"張\n"
            content += "自營商賣出張數(避險): " + str(round(int(df["自營商賣出股數(避險)"][i].replace(',',''))/1000))+"張\n"
            content += "自營商買賣超張數(避險): " + str(round(int(df["自營商買賣超股數(避險)"][i].replace(',',''))/1000))+"張\n\n"
            content += "--------------------------\n"+"三大法人買賣超張數:" + str(round(int(df["三大法人買賣超股數"][i].replace(',',''))/1000))+"張\n--------------------------"
            content += "\n\n資料來源:台灣證卷交易所"
            print(content)
            return content
    

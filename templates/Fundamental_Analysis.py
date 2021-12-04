'''
基本面三大能力評估所需的值: 經營能力、獲利能力、償債能力
'''
import requests
import pandas as pd
import numpy as np
import datetime

import pandas
import numpy as np

def get_three_index(stockNumber):
    url='http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcra/zcra_'+stockNumber+'.djhtm'
    basic=pandas.read_html(url)
   
    #經營能力
    a = [] # 
    b = [] # 
    c = []  # 
    d = []  # 
    
    #償債能力
    NAV = []# Net Asset Value，簡稱NAV
    DR = [] # Debt Ratio
    
    #獲利能力
    ROA = [] # ROA(B)稅後息前折舊前
    EPS = [] # 每股盈餘
    ROE = [] # ROE(A)─稅後 股東權益報酬率 
    PB=[]    #股價淨值比(PB比)
    

    
    
    for i in range(0,len(basic[2][0])):
        if basic[2][0][i]=='ROA(B)稅後息前折舊前':
            ROA.append(basic[2][0][i])
            ROA.append(basic[2][1][i])
            ROA.append(basic[2][2][i])
            ROA.append(basic[2][3][i])
            
        if basic[2][0][i][:6]=='ROE(A)':
            ROE.append(basic[2][0][i])
            ROE.append(basic[2][1][i])
            ROE.append(basic[2][2][i])
            ROE.append(basic[2][3][i])
            
        if basic[2][0][i]=='每股淨值(F)(TSE公告數)':
            PB.append(basic[2][0][i])
            PB.append(basic[2][1][i])
            PB.append(basic[2][2][i])
            PB.append(basic[2][3][i])
        
        if basic[2][0][i]=='每股盈餘':
            EPS.append(basic[2][0][i])
            EPS.append(basic[2][1][i])
            EPS.append(basic[2][2][i])
            EPS.append(basic[2][3][i])
        
        if basic[2][0][i][:4]=='經營能力':
            
            a.append(basic[2][0][i+3])
            a.append(basic[2][1][i+3])
            a.append(basic[2][2][i+3])
            a.append(basic[2][3][i+3])
            
            b.append(basic[2][0][i+4])
            b.append(basic[2][1][i+4])
            b.append(basic[2][2][i+4])
            b.append(basic[2][3][i+4])
            
            c.append(basic[2][0][i+5])
            c.append(basic[2][1][i+5])
            c.append(basic[2][2][i+5])
            c.append(basic[2][3][i+5])
            
            d.append(basic[2][0][i+6])
            d.append(basic[2][1][i+6])
            d.append(basic[2][2][i+6])
            d.append(basic[2][3][i+6])
        
        if basic[2][0][i]=='淨值/資產':
            NAV.append(basic[2][0][i])
            NAV.append(basic[2][1][i])
            NAV.append(basic[2][2][i])
            NAV.append(basic[2][3][i])
            
        if basic[2][0][i]=='負債比率％':
            DR.append(basic[2][0][i])
            DR.append(basic[2][1][i])
            DR.append(basic[2][2][i])
            DR.append(basic[2][3][i])

        
    print(ROA,ROE,PB,EPS,a,b,c,d,NAV,DR)
    return ROA,ROE,PB,EPS,a,b,c,d,NAV,DR



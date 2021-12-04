from linebot.models import *

#return ROA,ROE,PB,EPS,a,b,c,d,NAV,DR
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
            PB.append(basic[2][0][i][:7])
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


# 基本面- 經營能力
def operating_ability(stockNumber, stockName):
    content = get_three_index(stockNumber)
    a = content[4]  # 
    b = content[5] # 
    c = content[6] # 
    d = content[7] # 
    flex_message = FlexSendMessage(
            alt_text="經營能力",
            contents={
                    "type": "bubble",
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": stockName, # 替換成股票名稱
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": "經營能力",
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "期別",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "2019",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "2018",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "2017",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": a[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(a[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(a[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(a[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": b[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(b[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(b[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(b[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": c[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(c[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(c[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(c[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": d[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(d[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(d[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(d[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            }
                            ]
                        }
                        ]
                    }
            }
    )
    return flex_message
#return ROA,ROE,PB,EPS,a,b,c,d,NAV,DR
# 基本面- 償債能力
def debt_ability(stockNumber, stockName):
    content = get_three_index(stockNumber)
    NAV = content[8]  # Net Asset Value，簡稱NAV
    DR = content[9] # Debt Ratio
    flex_message = FlexSendMessage(
            alt_text="償債能力",
            contents={
                "type": "bubble",
                "styles": {
                    "footer": {
                    "separator": True
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": stockName,
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "償債能力",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "期別",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "2019",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#555555",
                                "align": "end"
                            },
                            {
                                "type": "text",
                                "text": "2018",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#555555",
                                "align": "end"
                            },
                            {
                                "type": "text",
                                "text": "2017",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#555555",
                                "align": "end"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": NAV[0],
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(NAV[1]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            },
                            {
                                "type": "text",
                                "text": str(NAV[2]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            },
                            {
                                "type": "text",
                                "text": str(NAV[3]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": DR[0],
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(DR[1]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            },
                            {
                                "type": "text",
                                "text": str(DR[2]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            },
                            {
                                "type": "text",
                                "text": str(DR[3]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        }
                        ]
                    }
                    ]
                }
                }
    )
    return flex_message
#return ROA,ROE,PB,EPS,a,b,c,d,NAV,DR
# 基本面- 獲利能力
def profit_ability(stockNumber, stockName):
    content = get_three_index(stockNumber)
    EPS = content[3] # 每股盈餘
    ROE = content[1] # 股東權益報酬率
    ROA = content[0]
    PB = content[2]
    flex_message = FlexSendMessage(
            alt_text="獲利能力",
            contents={
                "type": "bubble",
                "styles": {
                    "footer": {
                    "separator": True
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": stockName,
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "獲利能力",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "期別",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "2019",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "2018",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "2017",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#555555",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": PB[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(PB[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(PB[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(PB[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": EPS[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(EPS[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(EPS[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(EPS[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": ROE[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(ROE[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(ROE[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(ROE[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": ROA[0],
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(ROA[1]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(ROA[2]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": str(ROA[3]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            
                        ]
                    }
                    ]
                }
            }
    )
    return flex_message

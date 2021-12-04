from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage
from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction
import time
import twder
import requests
import random

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from invoiceapi.models import users
    
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
x=['https://www.youtube.com/watch?v=qDncY4XN_ks',
           'https://www.youtube.com/watch?v=8VUzuGyBj6Q',
           'https://www.youtube.com/watch?v=KJwST8ohFEM',
           'https://www.youtube.com/watch?v=OELBqvwXOBw',
           'https://www.youtube.com/watch?v=WLCmIlzIFZI&t=2340s'
           'https://www.youtube.com/watch?v=_nDYQq1s5ig',
           'https://www.youtube.com/watch?v=3cVPtlqEaBg',
           'https://www.youtube.com/watch?v=uQU0IT0Q0is',
           '給不了你']




def sendinvoiceUse(event):  #使用說明
    try:
        text1 ='''
1. 「對獎」功能會提示使用者輸入發票最後三碼，若最後三碼有中獎，就提示使用者輸入發票前五碼。
2. 「前期中獎號碼」功能會顯示前兩期發票中獎號碼。
3. 「本期中獎號碼」功能會顯示最近一期發票中獎號碼。
               '''
        message = TextSendMessage(
            text=text1,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="對獎", text="@輸入發票最後三碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="本期中獎號碼", text="@顯示本期中獎號碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="前期中獎號碼", text="@顯示前期中獎號碼")
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



def showCurrent(event):
    try:
        content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
        tree = ET.fromstring(content.text)  #解析XML
        items = list(tree.iter(tag='item'))  #取得item標籤內容
        title = items[0][0].text  #期別
        ptext = items[0][3].text  #中獎號碼
        ptext = ptext.replace('<p>','').replace('</p>','\n')
        message = title + '月\n' + ptext[:-1]  #ptext[:-1]為移除最後一個\n
        msg = TextSendMessage(
            text=message,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="對獎", text="@輸入發票最後三碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="前期中獎號碼", text="@顯示前期中獎號碼")
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,msg)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='讀取發票號碼發生錯誤！'))

def showOld(event):
    try:
        content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
        tree = ET.fromstring(content.text)  #解析XML
        items = list(tree.iter(tag='item'))  #取得item標籤內容
        message = ''
        for i in range(1,3):
            title = items[i][0].text  #期別
            ptext = items[i][3].text  #中獎號碼
            ptext = ptext.replace('<p>','').replace('</p>','\n')
            message = message + title + '月\n' + ptext + '\n'
        message = message[:-2]
        
        msg = TextSendMessage(
            text=message,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="對獎", text="@輸入發票最後三碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="本期中獎號碼", text="@顯示本期中獎號碼")
                    ),
                   
                ]
            )
        )
        
        
        line_bot_api.reply_message(event.reply_token,msg)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='讀取發票號碼發生錯誤！'))

def show3digit(event, mtext, userid):
    try:
        content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
        tree = ET.fromstring(content.text)
        items = list(tree.iter(tag='item'))  #取得item標籤內容
        ptext = items[0][3].text  #中獎號碼
        ptext = ptext.replace('<p>','').replace('</p>','')
        temlist = ptext.split('：')
        prizelist = []  #特別獎或特獎後三碼
        prizelist.append(temlist[1][5:8])
        prizelist.append(temlist[2][5:8])
        prize6list1 = []  #頭獎後三碼六獎中獎號碼
        for i in range(3):
            prize6list1.append(temlist[3][9*i+5:9*i+8])
        prize6list2 = temlist[4].split('、')  #增開六獎
        unit = users.objects.get(uid=userid)
        unit.state = 'no'
        unit.save()
        if mtext in prizelist:
            message = '符合特別獎或特獎後三碼，請繼續輸入發票前五碼！'
            unit = users.objects.get(uid=userid)
            unit.state = 'special'
            unit.save()
        elif mtext in prize6list1:
            message = '恭喜！至少中六獎，請繼續輸入發票前五碼！'
            unit = users.objects.get(uid=userid)
            unit.state = 'head'
            unit.save()
        elif mtext in prize6list2:
            message = '恭喜！此張發票中了六獎！'
        else:
            message = '很可惜，未中獎。請輸入下一張發票最後三碼。'
        msg = TextSendMessage(
            text=message,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="查看本期中獎號碼", text="@顯示本期中獎號碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="查看前期中獎號碼", text="@顯示前期中獎號碼")
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,msg)     
    except:
        msg = TextSendMessage(
            text='模式文字檔讀取錯誤！',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="查看本期中獎號碼", text="@顯示本期中獎號碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="查看前期中獎號碼", text="@顯示前期中獎號碼")
                    ),
                   ]
                  )
            )
        line_bot_api.reply_message(event.reply_token,msg)
        
        
        
        
        

def show5digit(event, mtext, userid):
    try:
        
        unit = users.objects.get(uid=userid)
        mode = unit.state
        if mode == 'no':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請先輸入發票最後三碼！'))
        else:
            try:
                content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
                tree = ET.fromstring(content.text)  #解析DOM
                items = list(tree.iter(tag='item'))  #取得item標籤內容
                ptext = items[0][3].text  #中獎號碼
                ptext = ptext.replace('<p>','').replace('</p>','')
                temlist = ptext.split('：')
                special1 = temlist[1][0:5]  #特別獎前五碼
                special2 = temlist[2][0:5]  #特獎前五碼
                prizehead = []  #頭獎前五碼
                for i in range(3):
                    prizehead.append(temlist[3][9*i:9*i+5])
                sflag = False  #記錄是否中特別獎或特獎
                if mode=='special' and mtext==special1:
                    message = '恭喜！此張發票中了特別獎！'
                    sflag = True
                elif mode=='special' and mtext==special2:
                    message = '恭喜！此張發票中了特獎！'
                    sflag = True
                if mode=='special' and sflag==False:
                    message = '很可惜，未中獎。請輸入下一張發票最後三碼。'
                elif mode=='head' and sflag==False:
                    if checkhead(mtext, prizehead[0], prizehead[1], prizehead[2]):
                        message = '恭喜！此張發票中了頭獎！'
                    elif checkhead(mtext[1:5], prizehead[0][1:5], prizehead[1][1:5], prizehead[2][1:5]):
                        message = '恭喜！此張發票中了二獎！'
                    elif checkhead(mtext[2:5], prizehead[0][2:5], prizehead[1][2:5], prizehead[2][2:5]):
                        message = '恭喜！此張發票中了三獎！'
                    elif checkhead(mtext[3:5], prizehead[0][3:5], prizehead[1][3:5], prizehead[2][3:5]):
                        message = '恭喜！此張發票中了四獎！'
                    elif checkhead(mtext[4], prizehead[0][4], prizehead[1][4], prizehead[2][4]):
                        message = '恭喜！此張發票中了五獎！'
                    else:
                        message = '恭喜！此張發票中了六獎！'
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
                unit = users.objects.get(uid=userid)
                unit.state = 'no'
                unit.save()
            except:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='讀取發票號碼發生錯誤！'))
            msg = TextSendMessage(
            text=message,
            quick_reply=QuickReply(
                items=[
                
                    QuickReplyButton(
                        action=MessageAction(label="查看本期中獎號碼", text="@顯示本期中獎號碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="查看前期中獎號碼", text="@顯示前期中獎號碼")
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,msg)     
    except:
        unit = users.objects.get(uid=userid)
        unit.state = 'no'
        unit.save()
        msg = TextSendMessage(
            text='模式文字檔讀取錯誤！',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="查看本期中獎號碼", text="@顯示本期中獎號碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="查看前期中獎號碼", text="@顯示前期中獎號碼")
                    ),
                   ]
                  )
            )
        line_bot_api.reply_message(event.reply_token,msg)

def checkhead(mtext, str1, str2, str3):
    return (mtext==str1 or mtext==str2 or mtext==str3)


def sendexchangrUse(event):  #快速選單
    try:
        
        text1='''
1. 使用按鍵上方快速選單選擇外幣。
2. 查詢其他外幣輸入: $+'外幣國別'
例如:$美金、$加幣、$HKD

外幣一覽表:
美金:USD      港幣:HKD
英鎊:GBP      日圓:JPY
瑞郎:CHF      紐幣:NZD
泰幣:THB      歐元:EUR
韓元:KRW      人民幣:CNY  
南非幣:ZAR    瑞典幣:SEK   
印尼幣:IDR    越南盾:VND
越南幣:VND    馬來幣:MYR  
新加坡幣:SGD  瑞士法郎:CHF
加拿大幣:CAD  菲國比索:PHP
 '''
        message = TextSendMessage(
            text=text1,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="美金", text="$USD")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="港幣", text="$HKD")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="人民幣", text="$CNY")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="所有匯率", text="$所有匯率")
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))




#event.reply_token,



def exchange(mtext,event):  #快速選單
    try:
        print(mtext)
        
        currencies = {'美金':'USD','美元':'USD','港幣':'HKD','英鎊':'GBP','澳幣':'AUD','加拿大幣':'CAD',\
                  '加幣':'CAD','新加坡幣':'SGD','新幣':'SGD','瑞士法郎':'CHF','瑞郎':'CHF','日圓':'JPY',\
                  '日幣':'JPY','南非幣':'ZAR','瑞典幣':'SEK','紐元':'NZD','紐幣':'NZD','泰幣':'THB',\
                  '泰銖':'THB','菲國比索':'PHP','菲律賓幣':'PHP','印尼幣':'IDR','歐元':'EUR','韓元':'KRW',\
                  '韓幣':'KRW','越南盾':'VND','越南幣':'VND','馬來幣':'MYR','人民幣':'CNY' }
        keys = currencies.keys()
        tlist = ['查詢時間','現金買入', '現金賣出', '即期買入', '即期賣出']
        
        if mtext in currencies:
            currency = twder.now(currencies[mtext])
            name=mtext
            name_en=currencies[mtext]
        elif mtext in currencies.values():
            currency = twder.now(mtext)
            name=list (currencies.keys()) [list (currencies.values()).index (mtext)]
            name_en=mtext
        
        print(currency)
        now_time = str(currency[0])# 銀行現金買入價格
        
        buying_cash = "無資料" if  currency[1] == '-' else str(float(currency[1])) # 銀行現金賣出價格
        sold_cash =   "無資料" if  currency[2] == '-' else str(float(currency[2])) # 銀行即期買入價格       
        buying_spot = "無資料" if  currency[3] == '-' else str(float(currency[3])) # 銀行即期買入價格     
        sold_spot =   "無資料" if  currency[4] == '-' else str(float(currency[4])) # 銀行即期賣出價格 

        msg =name+name_en+'匯率\n' +  "最新掛牌時間為: " + now_time + '\n ---------- \n 現金買入價格: ' + buying_cash + '\n 現金賣出價格: ' + str(sold_cash) + '\n 即期買入價格: ' + buying_spot + '\n 即期賣出價格: '  +  sold_spot + '\n \n'+'資料來源:台灣銀行新台幣匯率報價'
        
        message = TextSendMessage(
            text=msg,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="再來一次美金?", text="$USD")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="再來一次港幣?", text="$HKD")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="再來一次人民幣?", text="$CNY")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="再來一次所有匯率?", text="$所有匯率")
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def exchange_all(event):  #快速選單
    try:
        currencies = {  'USD':'美金','HKD':'港幣' ,'GBP':'英鎊' ,'AUD':'澳幣','JPY':'日幣','NZD':'紐幣', 'THB':'泰幣',
                'EUR':'歐元','KRW':'韓元', 'IDR': '印尼幣', 'ZAR':'南非幣' ,'SEK': '瑞典幣', 'VND':'越南幣',
                'MYR': '馬來幣', 'CNY':'人民幣' , 'PHP':'菲律賓幣','CAD':'加拿大幣' ,'SGD':'新加坡幣','CHF': '瑞士法郎',
                }

        msg=''
        currency = twder.now_all()
        source='資料來源:台灣銀行新台幣匯率報價'
        for key in currencies:
            now_time = str(currency[key][0])# 銀行現金買入價格
            buying_cash = "無資料" if  currency[key][1] == '-' else str(float(currency[key][1])) # 銀行現金賣出價格
            sold_cash =   "無資料" if  currency[key][2] == '-' else str(float(currency[key][2])) # 銀行即期買入價格       
            buying_spot = "無資料" if  currency[key][3] == '-' else str(float(currency[key][3])) # 銀行即期買入價格     
            sold_spot =   "無資料" if  currency[key][4] == '-' else str(float(currency[key][4])) # 銀行即期賣出價格
            data = currencies[key]+'匯率\n' + '---------- \n現金買入價格: ' + buying_cash + '\n現金賣出價格: ' + str(sold_cash) + '\n即期買入價格: ' + buying_spot + '\n即期賣出價格: '  +  sold_spot + '\n \n'    
            msg+=str(data)
            
        time=str("最新掛牌時間為: " + now_time +'\n')
        total=time+msg+source
        print(total)
        message = TextSendMessage(
            text=str(total),
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="再來一次美金?", text="$USD")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="再來一次港幣?", text="$HKD")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="再來一次人民幣?", text="$CNY")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="再來一次所有匯率?", text="$所有匯率")
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



def sendStockUse(event):  #使用說明
    try:
        text1 ='''1. 使用按鍵上方快速選單選擇新聞。
2. 查詢其他股票新聞輸入: N+'股票代號'
例如:N2330、N0050、N3008。
               '''
        
          
        message = TextSendMessage(
            text=text1,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="最新消息", text="@最新消息")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="個股新聞", text="請輸入N+'股票代號")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="來一點台積電新聞?", text="N2330")
                    ),
                     QuickReplyButton(
                        action=MessageAction(label="不管什麼都給我來一點就是了", text=x[random.randint(0,8)])
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))





def sendStock(event):  #使用說明
    try:
        text1 ='''1.進入選單輸入股票代號 S+'股票代號'
   Ex:S2330、S3008、S0050
               '''
        message = TextSendMessage(
            text=text1,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="最新消息", text="@最新消息")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="個股新聞", text="請輸入N+'股票代號")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="來一點台積電新聞?", text="N2330")
                    ),
                     QuickReplyButton(
                        action=MessageAction(label="不管什麼都給我來一點就是了", text=x[random.randint(0,8)])
                    ),
                   
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))









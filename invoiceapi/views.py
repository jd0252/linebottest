from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,ImageSendMessage
from invoiceapi.models import users


from templates import Stock_News,Stock,fundamental_ability



import re
from pymongo import MongoClient
import pymongo
import urllib.parse
import requests
from module import func,stockprice,Institutional_Investors,kchart
from flask import Flask, request, abort

        
        
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                userid = event.source.user_id
                if not users.objects.filter(uid=userid).exists():
                    unit = users.objects.create(uid=userid, state='no')
                    unit.save()
                mtext = event.message.text
                if mtext == '@發票使用說明':
                    func.sendinvoiceUse(event)
                    

                    
                elif mtext == '@顯示本期中獎號碼':
                    func.showCurrent(event)

                elif mtext == '@顯示前期中獎號碼':
                    func.showOld(event)

                elif mtext == '@輸入發票最後三碼':
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入發票最後三碼進行對獎！'))
                elif len(mtext) == 3 and mtext.isdigit():
                    func.show3digit(event, mtext, userid)

                elif len(mtext) == 5 and mtext.isdigit():
                    func.show5digit(event, mtext, userid)

                
                elif mtext == '@匯率使用說明':
                    func.sendexchangrUse(event)
                    
                elif mtext == '$所有匯率':
                    func.exchange_all(event)                  
                
                elif re.match('[$]', mtext):
                    currency = str(mtext[1:]).replace(" ", "")
                    func.exchange(currency,event)
                
                elif mtext == '@股市使用說明':
                    func.sendStock(event)
                
                elif mtext == '@個股新聞使用說明':
                    func.sendStockUse(event)
                    
                    
                elif mtext == '@最新消息':
                    try:                       
                        content = Stock_News.all_stock()                      
                        line_bot_api.reply_message(event.reply_token,content)
                    except:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
                        
                elif re.match(r'N\w'  , mtext): # 個股新聞
                    stockNumber = mtext[1:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Stock_News.single_stock(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[content,btn_msg])
                elif re.match(r'三大面向分析\w' , mtext):
                    stockNumber = mtext[6:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    content  = Stock.stock_ananlysis_menu(stockNumber)
                    line_bot_api.reply_message(event.reply_token, content)
                    return 0    
                        
                elif re.match(r'#\w' , mtext): #查詢某檔股票
                    stockNumber = mtext[1:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content_text = stockprice.getprice(stockNumber)
                        content = Stock.stock_reply(stockNumber, content_text)
                        line_bot_api.reply_message(event.reply_token, content)
                        return 0
                elif re.match(r'P\w' ,mtext):
                    stockNumber = mtext[1:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockNumber == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        trend_imgurl = stockprice.stock_trend(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[ImageSendMessage(original_content_url=trend_imgurl, preview_image_url=trend_imgurl),btn_msg])
                                    
                    return 0
                elif re.match(r'F\w' , mtext):
                    stockNumber = mtext[1:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockNumber == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Institutional_Investors.institutional_investors(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=content),btn_msg])                   
                    return 0
                
                elif re.match(r'K\w', mtext):
                    stockNumber = mtext[1:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Stock.kchart_msg + "\n" +Stock.kd_msg
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage('稍等一下,快出乃了... K線圖繪製中...(約10秒)\n\n\n'+content))
                        k_imgurl = kchart.draw_kchart(stockNumber)
                        line_bot_api.push_message(userid, [ImageSendMessage(original_content_url=k_imgurl, preview_image_url=k_imgurl),btn_msg])
                        return 0
                elif re.match(r'MACD\w', mtext):
                    stockNumber = mtext[4:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Stock.kchart_msg + "\n" +Stock.macd_msg
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage('稍等一下, MACD線圖繪製中...(約10秒)\n\n\n'+content))
                        MACD_imgurl = kchart.draw_MACDchart(stockNumber)
                        line_bot_api.push_message(userid, [ImageSendMessage(original_content_url=MACD_imgurl, preview_image_url=MACD_imgurl),btn_msg])
                        return 0
                elif re.match(r'RSI\w' , mtext):
                    stockNumber = mtext[3:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Stock.kchart_msg + "\n" +Stock.rsi_msg
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage('稍等一下, RSI線圖繪製中...(約10秒)\n\n\n'+content))
                        RSI_imgurl = kchart.draw_RSIchart(stockNumber)
                        line_bot_api.push_message(userid, [ImageSendMessage(original_content_url=RSI_imgurl, preview_image_url=RSI_imgurl),btn_msg])
                   
                        return 0
                elif re.match(r'收益率\w', mtext):
                    stockNumber = mtext[3:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        return_imgurl = stockprice.show_return(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.push_message(userid,[ImageSendMessage(original_content_url=return_imgurl, preview_image_url=return_imgurl),btn_msg])                  
                    return 0
                elif re.match(r'股票基本面\w', mtext):###########
                    stockNumber = mtext[5:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Stock.stock_fundation_analysis(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[content,btn_msg])                  
                    return 0
                
                elif re.match(r'S\w', mtext):
                    stockNumber = mtext[1:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Stock.stock_ananlysis_menu(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[content,btn_msg])                  
                    return 0
                elif re.match(r'股票技術面\w', mtext):
                    stockNumber = mtext[5:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Stock.stock_tec_analysis(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[content,btn_msg])                  
                    return 0
                
                elif re.match(r'經營能力\w', mtext):
                    stockNumber = mtext[4:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no":line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = fundamental_ability.operating_ability(stockNumber,stockName)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[content,btn_msg])  

                elif re.match(r'償債能力\w', mtext):
                    stockNumber = mtext[4:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no":line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = fundamental_ability.debt_ability(stockNumber,stockName)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[content,btn_msg])  
                        
                       
                elif re.match(r'獲利能力\w', mtext):
                    stockNumber = mtext[4:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    if stockName == "no":line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = fundamental_ability.profit_ability(stockNumber,stockName)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        print('456')
                        line_bot_api.reply_message(event.reply_token,[content,btn_msg]) 
                        
                elif re.match(r'股票籌碼面\w', mtext):
                    stockNumber = mtext[5:].replace(" ", "")
                    stockName = stockprice.get_stock_name(stockNumber)
                    print(stockName)
                    if stockNumber == "no": line_bot_api.reply_message(event.reply_token,(TextSendMessage("股票代碼錯誤")))
                    else:
                        content = Institutional_Investors.institutional_investors(stockNumber)
                        btn_msg = Stock.stock_reply_other(stockNumber)
                        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=content),btn_msg])                   
                    return 0
                
                
                
        return HttpResponse()

    else:
        return HttpResponseBadRequest()

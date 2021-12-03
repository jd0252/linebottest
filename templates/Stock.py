# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 22:11:48 2020

@author: jd025
"""
from linebot.models import *

# from linebot.models import TextSendMessage, FlexSendMessage, QuickReplyButton, QuickReply, MessageAction,TemplateSendMessage,ImageCarouselColumn, ImageCarouselTemplate, TextMessage



#=============================================
# 其他教學(與查詢的訊息一同送出)
kchart_msg =  "每一根K線都由四個價格組成：開盤價、最高價、最低價、收盤價。如果收盤價比開盤價高，會畫出陽線(紅K)，反之，如果收盤價比開盤價低，就會畫出陰線(綠K)。"
macd_msg =  "MACD是對長期(MACD)與短期(DIF)的移動平均線，加以雙重平滑處理，用來判斷買賣股票的時機與訊號。當快線向上突破慢線/柱線由負轉正時，即為買進訊號；當快線向下跌破慢線/柱線由正轉負時，即為賣出訊號。"
kd_msg = 'KD指標取9天內的最高和最低，來反應股價整體的動能。當KD指標的K值由下往上突破D值，建議買進；當KD指標的K值由上往下跌破D值時，建議賣出。\n'\
+'KD指標>80以上為"高檔超買"，KD<20以下為"低檔超賣"，一旦KD值到達了上述的超買區或超跌區連續三天，即為KD鈍化。\n\n' \
+'當股票高檔鈍化時，表示非常的強勢，通常會再漲的機會就會變得非常高。\n'\
+'當股票低檔鈍化時，表示非常的弱勢，通常會再跌的機會就會變得非常高。'

rsi_msg='RSI是可看出股價相對強弱的指標，以某段時間股價、平均漲幅與平均跌幅所計算出來的數值\n1.RSI大於 80 時，為超買訊號，市場過熱，要準備開始跌了。\n2.RSI小於 20 時，為超賣訊號，市場過冷，要準備開始漲了。'
bband_msg =  "布林通道:\n由布林上軌（壓力線）、布林中軌（20MA）與布林下軌（支撐線）所組成。若股價碰到上軌有可能會下跌，往中軌靠近；若股價碰到下軌可能會上漲，往中軌靠近。"
maxdd_msg =  "最大回撤:\n是過去最大的資金回檔，也就是過去所經歷最大的風險。可以將MaxDD當作準備資金的參考值，也能評量一個策略在目前市場表現的狀況，若出現連續虧損已經超過歷史的 MaxDD，則要考慮這個策略在市場上是否仍然有效。"
#=============================================



# 股票 quick reply(給#代碼指令)
def stock_reply(stockNumber, content_text):
    text_message = TextSendMessage(
                                text = content_text ,
                               quick_reply=QuickReply(
                                   items=[
                                        QuickReplyButton(
                                                action=MessageAction(
                                                    label="走勢圖", 
                                                    text="P"+stockNumber,
                                                )
                                       ),
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="K線圖", 
                                                    text="K"+stockNumber
                                                )
                                       ),
                                       QuickReplyButton(#???
                                                action=MessageAction(
                                                    label="法人", 
                                                    text="F"+stockNumber
                                                )
                                       ),
                                       
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="新聞", 
                                                    text= "N"+stockNumber
                                                )
                                       ),
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="年收益率", 
                                                    text= "收益率" + stockNumber
                                                )
                                       ),
                                ]
                            ))
    return text_message


def stock_reply_other(stockNumber):
    content_text = "想知道更多?"
    text_message = TextSendMessage(
                                text = content_text ,
                               quick_reply=QuickReply(
                                   items=[
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="即時股價", 
                                                    text="#"+stockNumber,
                                                )
                                       ),
                                       
                                        QuickReplyButton(
                                                action=MessageAction(
                                                    label="走勢圖", 
                                                    text="P"+stockNumber,
                                                )
                                       ),
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="K線圖", 
                                                    text="K"+stockNumber
                                                )
                                       ),
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="法人", 
                                                    text="F"+stockNumber
                                                )
                                       ),
                                       
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="新聞", 
                                                    text= "N"+stockNumber
                                                )
                                       ),
                                       QuickReplyButton(
                                                action=MessageAction(
                                                    label="年收益率", 
                                                    text= "收益率" + stockNumber
                                                )
                                       ),
                                ]
                            ))
    return text_message

# 股票三大面向分析(查詢股價配合quick repay)
def stock_ananlysis_menu(stockNumber):
    flex_message = FlexSendMessage(
            alt_text=stockNumber+"股票三大面向分析",
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/5F4Q3c7.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": stockNumber+"股票三大面向分析",
                        "weight": "bold",
                        "size": "lg"
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
                        "type": "message",
                        "label": "股票技術面",
                        "text": "股票技術面" + stockNumber
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "股票基本面",
                            "text": "股票基本面" + stockNumber
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "股票籌碼面" ,
                            "text": "股票籌碼面" + stockNumber
                        }
                    }
                    ],
                    "flex": 0
                }
            }
        )
    return flex_message
# 股票技術面分析
def stock_tec_analysis(stockNumber):
    flex_message = FlexSendMessage(
            alt_text=stockNumber+"股票技術面",
            contents={
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/Iu9ArZq.jpg",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": stockNumber+"股票技術面",
                            "weight": "bold",
                            "size": "xl",
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
                            "type": "message",
                            "label": "股票K線圖",
                            "text": "K" + stockNumber
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "股票MACD指標",
                            "text": "MACD" + stockNumber
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "股票RSI指標",
                            "text": "RSI" + stockNumber
                            }
                        },
                        
                        ],
                        "flex": 0,
                        "margin": "none"
                    }
            }
    )
    return flex_message
#  股票基本面分析
def stock_fundation_analysis(stockNumber):
    flex_message = FlexSendMessage(
            alt_text=stockNumber+"股票基本面",
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/eoKkepb.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": stockNumber+"股票基本面",
                        "weight": "bold",
                        "size": "xl"
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
                        "type": "message",
                        "label": "股票償債能力",
                        "text": "償債能力"+stockNumber
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": "股票經營能力",
                        "text": "經營能力"+stockNumber
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "股票獲利能力",
                        "text": "獲利能力"+stockNumber
                        }
                    }
                    ],
                    "flex": 0,
                    "margin": "none"
                }
            }
    )
    return flex_message



    



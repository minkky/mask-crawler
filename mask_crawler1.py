# -*- coding: utf-8 -*- 
import requests
import time
from bs4 import BeautifulSoup
import telegram
import re, sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('token.txt', 'r') as token:
    token = token.readline()
my_token = token
bot = telegram.Bot(token=my_token)
chat_id = bot.getUpdates()[-1].message.chat.id 

mask_site = 'https://smartstore.naver.com/gonggami/products/4705579501'
mask_site = 'https://smartstore.naver.com/aer-shop/products/4792484420'
if __name__ == '__main__':
    latest_notice = ''
    
    while True:
        req = requests.get(mask_site)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        post = soup.find("div", {"class":"prd_type3"})
        try:
            content = post.text.strip().split('.')[0]
        except:
            bot.sendMessage(chat_id, 'something happend')
        else:
            if content != '이 상품은 현재 구매하실 수 없는 상품입니다':
                text = '[구매 가능]\n'
                text += mask_site
                bot.sendMessage(chat_id, text)
        time.sleep(60)
    

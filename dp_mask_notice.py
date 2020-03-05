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

notice_site = ''
mask_site = ''
if __name__ == '__main__':
    latest_notice = ''
    
    while True:
        req = requests.get(notice_site)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        post = soup.find("div", {"class":"se_textView"})
        notice_content = post.text.strip()
        notice_content = notice_content.encode('euc-kr','ignore').decode('euc-kr')
        r = re.compile('\d{8}\s*[APap][mM]\s*\d*:\d*')
        notice_date = r.search(notice_content).group()
        
        if latest_notice != notice_date:
            latest_notice = notice_date
            text = '[새로운 공지]\n' + notice_site + '\n\n'
            text += notice_content.split('------')[0]
            text += '\n\n판매 사이트: ' + mask_site
            bot.sendMessage(chat_id, text)
            print('latest notice date: ' + notice_date)
            
        time.sleep(60)
    

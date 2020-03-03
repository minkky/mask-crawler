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
mask_site = 'https://coronamask.kr/'
if __name__ == '__main__':
    latest_names = []
    while True:
        req = requests.get(mask_site)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all("div", {"class": "relative w-full border-r border-gray-400 border-l-0 border-t border-b bg-white rounded-b-none rounded-r p-4 flex flex-col justify-between leading-normal"} )
        candidates = []
        for post, p in zip(soup.find_all("div", {"class": "relative w-full border-r border-gray-400 border-l-0 border-t border-b bg-white rounded-b-none rounded-r p-4 flex flex-col justify-between leading-normal"}), soup.find_all("p", {"class":"text-gray-900 leading-none mb-2"})):
            #print(post.a.attrs["href"], post.div.text, p.text.strip())
            candidate_name = post.div.text
            candidates.append(candidate_name)
            candidate_link = post.a.attrs["href"]
            candidate_date = p.text.strip()
            
            if candidate_date.find("예정") != -1 or candidate_date.find("미정") != -1 :
                continue
            if candidate_name in latest_names:
                continue
            else:
                latest_names.append(candidate_name)
                text= '[new mask]\n' + candidate_name + '\n' + candidate_date + '\n' + candidate_link
                bot.sendMessage(chat_id, text)
        for name in latest_names:
        	if name in candidates:
        		continue
        	else:
        		latest_names.remove(name)

        time.sleep(60)


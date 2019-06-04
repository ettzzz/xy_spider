#!/usr/bin/env python3

'''
xianyu mornitor
spider.py
'''

#import requests_html
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os



#results should be like [{'gtx970~￥880.00':'hisurl'},{'charger~￥400.00':'herurl'}]

class xianyu_spider(): 
    def __init__(self):
        self.batch_size = 1000
        self.batch_memory = []
        self.useful_items = []
        self.max_attempts = 10
        self.pages = 5
        self.failure_counter = 0
        self.path = os.path.realpath('run.py').split('run.py')[0]
        self.base_url = 'https://s.2.taobao.com/list'
        self.header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) \
          AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'}
        

    def build_pool(self, item_obj): 
#        title = item_obj.find('h4.item-title', first = True).text
#        link = item_obj.find('div.item-info > h4 > a', first = True).attrs['href']
#        price = item_obj.find('span.price > em', first = True).text
        
        title = item_obj.select('h4.item-title')[0].text
        link = item_obj.select('div.item-info > h4 > a')[0]['href']
        price = item_obj.select('span.price > em')[0].text
        cache_dict = {str(title+'~￥'+price):'https:'+link}
        return cache_dict
        
    

    def use_filter(self, category, item_obj): #easy text games
        judgement = False
        
#        description = item_obj.find('div.item-description', first = True).text
        description = item_obj.select('div.item-description')[0].text
        title = item_obj.select('h4.item-title')[0].text
        
        if any(each_kw in description for each_kw in category['keywords']):
            judgement = True
        if any(each_sw in description for each_sw in category['stopwords']):
            judgement = False
        if any(each_sw in title for each_sw in category['stopwords']):
            judgement = False
            
        if judgement:
            self.useful_items.append(self.build_pool(item_obj))
            
    
    
    def spider(self, category): #all about spidering, including retry, exception, deduplication(by batch_memory), 
                                #write into pools, 
        for page in range(self.pages):
            api_params = {
#                'spm':'2007.1000337.0.0.2c9f8b24CgddrV',
                'st_edtime':'1',
                'ist':'0',
                '_input_charset':'utf8',
                'start':category['price_boundary'][0],
                'end':category['price_boundary'][-1],
                'q':category['search_word'],
                'page':str(page+1),
                }
            for _ in range(self.max_attempts):
                try:
                    r = requests.get(self.base_url, headers = self.header, params = api_params, timeout = 15)
#                    r = requests_html.HTMLSession().get(self.base_url, headers = self.header, params = api_params, timeout = 15)
                except:
                    self.failure_counter += 1
                    continue # timeout
                    
                if r.status_code == 200 and '亲，你太潮了' not in r.text and '被挤爆了' not in r.text:
                    print('Succuss @ {}'.format(r.url))
#                    items = r.html.find('#J_ItemListsContainer > ul > li') # 20 items per page
#                    for each_item in items:
#                        number = each_item.find('div.item-info > h4 > a', first = True).attrs['href'].split('id=')[-1]
                    
                    html = BeautifulSoup(r.text, 'html.parser')
                    items = html.select('#J_ItemListsContainer > ul > li')
                    for each_item in items:
                        uid = each_item.select('div.item-info > h4 > a')[0]['href'].split('id=')[-1] 
                        if uid in self.batch_memory:
                            break
                        else:
                            self.use_filter(category, each_item)
                            if len(self.batch_memory) <= self.batch_size:
                                self.batch_memory.insert(0, uid)
                            else:
                                deprecated_var = self.batch_memory.pop()
                                self.batch_memory.insert(0, uid)
                    break
                else:
                    time.sleep(6) #200 but jammed / 504
                
       

    def clean_cache(self, category): #only use when one notification is delivered
        if category == 'pool':
            self.useful_items = []
        elif category == 'failure_counter':
            self.failure_counter = 0
        else:
            print('Bug from clean_cache(): Wrong category')
        
    
    def notify_trigger(self, threshold):
        if len(self.useful_items) > threshold:
            return True
        else:
            return False
        
    def add_split(self, category):
        self.useful_items.append(category['search_word'])
        
    def save_memory(self):
        cache_csv = pd.DataFrame(self.batch_memory)
        cache_csv.to_csv(self.path+'cache_memory.csv', index = False)

    def read_memory(self):
        cache_list = pd.read_csv(self.path+'cache_memory.csv')
        self.batch_memory = list(map(str, list(cache_list['0'])))


if __name__ == "__main__":
    categories = [
#        {'search_word':'gtx970', 'price_boundary':[550, 750], 'keywords':['冰龙','超级冰龙','红龙','名人堂','龙骑士','至尊','烈焰'], 'stopwords':['回收','收','高价','网吧']},
        {'search_word':'gtx960', 'price_boundary':[250, 350], 'keywords':['冰龙','超级冰龙','红龙','名人堂','龙骑士','至尊','烈焰'], 'stopwords':['回收','收','高价','网吧']},
#        {'search_word':'gx450', 'price_boundary':[100, 300], 'keywords':['酷冷','450'], 'stopwords':['回收','收','高价']},
#        {'search_word':'amd专用条 ddr3', 'price_boundary':[50, 100], 'keywords':['amd','8100','专用'], 'stopwords':['回收','收','高价','金士顿']},
#        {'search_word':'ps4 slim', 'price_boundary':[1200, 1600], 'keywords':['自用','pro'], 'stopwords':['回收','收','高价','求']},
        ]
    agent = xianyu_spider()
    try:
         agent.read_memory()
    except:
        pass
    
#    for each_category in categories:
    each_category = categories[0]
    agent.add_split(each_category)
    agent.spider(each_category)

'''
xianyu mornitor
run.py
'''
import time
from bs4_spider import xianyu_spider
from notify import tell_my_bot



categories = [
#        {'search_word':'gtx970', 'price_boundary':[550, 750], 'keywords':['冰龙','超级冰龙','红龙','名人堂','龙骑士','至尊','烈焰'], 'stopwords':['回收','收','高价','网吧']},
        {'search_word':'gtx960', 'price_boundary':[250, 350], 'keywords':['冰龙','超级冰龙','红龙','名人堂','龙骑士','至尊','烈焰'], 'stopwords':['回收','收','高价','网吧']},
#        {'search_word':'gx450', 'price_boundary':[100, 300], 'keywords':['酷冷','450'], 'stopwords':['回收','收','高价']},
#        {'search_word':'amd专用条 ddr3', 'price_boundary':[50, 100], 'keywords':['amd','8100','专用'], 'stopwords':['回收','收','高价','金士顿']},
#        {'search_word':'ps4 slim', 'price_boundary':[1200, 1600], 'keywords':['自用','pro'], 'stopwords':['回收','收','高价','求']},
        ]


def main():
    messager = tell_my_bot()
    agent = xianyu_spider()
    
    while True:
        try:
            agent.read_memory()
        except:
            pass
        
        for each_category in categories:
            agent.add_split(each_category)
            agent.spider(each_category)
            
        if agent.notify_trigger(threshold = len(categories)):
            agent.save_memory()
            messager.send_to_me(agent.useful_items, 'good_news')
            
        agent.clean_cache('pool')
        
        if agent.failure_counter > 100:
            messager.send_to_me(agent.useful_items, 'bad_news')
            agent.clean_cache('failure_counter')
        
        time.sleep(3600)
#        break
    

if __name__ == '__main__':
    main()


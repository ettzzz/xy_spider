'''
xianyu mornitor
notify.py
'''

import requests
# example:
'''
https://api.telegram.org/bot781431817:AAEt1G2VaqMyu4OARKLnufp6eqBnHz6zORU/
sendMessage?chat_id=476917241&
text=hereiswhatyougot%0a%3Ca%20href=%22http://www.google.com/%22%3Einline%20URL%3C/a%3E&parse_mode=HTML
'''
# and url transfer https://blog.csdn.net/Tangzongyu123/article/details/75224468

# remember to replace such as & to &amp

#results should be like [{'gtx970~￥880.00':'hisurl'},{'charger~￥400.00':'herurl'}]


class tell_my_bot():
    
    def __init__(self):
        # we need a results pool here
        self.token = '781431817:AAEt1G2VaqMyu4OARKLnufp6eqBnHz6zORU'
        self.chat_id = '476917241'
        self.api_base = 'https://api.telegram.org/bot{}/sendMessage'.format(self.token)
        self.header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) \
          AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'}
        
    
    def build_html_message(self, kv_pair): #designed for xianyu only, consists of name and price
        try:
            for k, v in kv_pair.items():    
                text = '<a href="{}">{}</a>'.format(v, k) 
                
        except:
            text = 'HTML message Error'
        return text
    
    def send_to_me(self, spider_eggs, news): #write an api and send it to telegram server
        if news == 'good_news':
            for each_useful_item in spider_eggs:
                if type(each_useful_item) == dict:
                    bot_params = {
                        'chat_id':self.chat_id,
                        'text':self.build_html_message(each_useful_item),
                        'disable_web_page_preview':'True',
                        'parse_mode':'HTML',
                        }
                else:
                    bot_params = {
                        'chat_id':self.chat_id,
                        'disable_web_page_preview':'True',
                        'text':'-----------↓ 关键词:{} ↓------------'.format(each_useful_item),
                        }
                requests.get(self.api_base, headers = self.header, params = bot_params)
        elif news == 'bad_news':
            bot_params = {
                    'chat_id':self.chat_id,
                    'text':'ATTENTION: Failure counter has reached threshold!',
                    }
            requests.get(self.api_base, headers = self.header, params = bot_params)
        else:
            pass


from bs4 import BeautifulSoup
import re
import time
import requests
import json
import traceback
from urllib import parse

class Infos(object):
    def __init__(self, cookies):
        self.sess = requests.Session()
        self.cookies = cookies
        self.charge_url = 'http://portal.xcc.edu.cn/pnull.portal?rar=0.7839039938375213&.pmn=view&action=showItem&.ia=false&.pen=pe564&itemId=193&childId=321&page='
        self.financial_url = 'http://portal.xcc.edu.cn/pnull.portal?rar=0.3525903705726091&.pmn=view&action=showItem&.ia=false&.pen=pe564&itemId=193&childId=361&page='
        self.req = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            }
    
    def school_card(self, page):
        try:
            req = self.sess.get(self.charge_url + page, headers=self.headers,cookies=self.cookies)
            table = BeautifulSoup(req.text, 'lxml').find('table')
            trs = table.find_all('tr')
            num = table.find('div',class_='page_nav').find_all('i')[0].get_text()
            nowpage = table.find('div',class_='page_nav').find_all('i')[1].get_text()
            pages = table.find('div',class_='page_nav').find_all('i')[2].get_text()
            if int(nowpage) > int(pages):
                return {'err':"没有下一页了"}
            res = {
                'num': int(num),
                'sta': nowpage + "/" + pages,
                'xh': trs[1].find_all('td')[0].get_text().strip(),
                'name': trs[1].find_all('td')[1].get_text().strip(),
                'list': [{
                    'money': trs[i].find_all('td')[2].get_text().strip(),
                    'type': trs[i].find_all('td')[3].get_text().strip(),
                    'date': trs[i].find_all('td')[4].get_text().strip()
                }for i in range(1,len(trs)-1)]
            }
            return res
        except Exception:
            traceback.print_exc()
        
    def financial(self, page):
        try:
            req = self.sess.get((self.financial_url + page).encode('utf-8'), headers=self.headers,cookies=self.cookies)
            table = BeautifulSoup(req.text, 'lxml').find('table')
            trs = table.find_all('tr')
            num = table.find('div',class_='page_nav').find_all('i')[0].get_text()
            nowpage = table.find('div',class_='page_nav').find_all('i')[1].get_text()
            pages = table.find('div',class_='page_nav').find_all('i')[2].get_text()
            if int(nowpage) > int(pages):
                return {'err':"没有下一页了"}
            res = {
                'num': int(num),
                'sta': nowpage + "/" + pages,
                'xh': trs[1].find_all('td')[0].get_text().strip(),
                'name': trs[1].find_all('td')[1].get_text().strip(),
                'college': trs[1].find_all('td')[2].get_text().strip(),
                'major': trs[1].find_all('td')[3].get_text().strip(),
                'class': trs[1].find_all('td')[4].get_text().strip(),
                'list': [{
                    'date': trs[i].find_all('td')[5].get_text().strip(),
                    'type': trs[i].find_all('td')[6].get_text().strip(),
                    'sm': trs[i].find_all('td')[7].get_text().strip(),
                    'tm': trs[i].find_all('td')[8].get_text().strip(),
                    'rm': trs[i].find_all('td')[9].get_text().strip()
                }for i in range(1,len(trs)-1)]
            }
            return res
        except Exception:
            traceback.print_exc()
from bs4 import BeautifulSoup
import re
import time
import requests
import json
import traceback
from urllib import parse

class PLogin(object):
    def __init__(self):
        self.login_url = 'http://ids.xcc.edu.cn/authserver/login?service=http%3A%2F%2Fportal.xcc.edu.cn%2Findex.portal'
        self.library_url = 'http://ids.xcc.edu.cn/authserver/login?service=http%3A%2F%2Fopac.xcc.edu.cn%3A8080%2Freader%2Fhwthau.php'
        self.st_url = ''
        self.index_url = 'http://portal.xcc.edu.cn/index.portal'
        self.sess = requests.Session()
        self.cookies = ''
        self.req = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            }
    
    def plogin(self, username, password):
        try:
            req = self.sess.get(self.login_url, headers=self.headers,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            soup = BeautifulSoup(req.text, 'lxml')
            lt = soup.find('input',{"name":"lt"}).get("value")
            # print('lt:'+lt)
            execution = soup.find('input',{"name":"execution"}).get("value")
            # print('execution:'+execution)
            eventId = soup.find('input',{"name":"_eventId"}).get("value")
            # print('eventId:'+eventId)
            self.cookies = self.sess.cookies
            login_data = {
                'username': username,
                'password': password,
                'lt': lt,
                'execution': execution,
                '_eventId': eventId,
                'rmShown': "1"
            }
            self.req = self.sess.post(self.login_url, headers=self.headers,cookies=self.cookies,
                                    data=login_data,allow_redirects=False)
            JSESSIONID = requests.utils.dict_from_cookiejar(self.cookies)["JSESSIONID"]
            try:
                CASTGC = requests.utils.dict_from_cookiejar(self.cookies)["CASTGC"]
            except Exception as e:
                return {'err':"用户名或密码错误"}
            self.st_url = self.req.headers['Location']
            self.sess.get(self.st_url)
            return {'JSESSIONID':JSESSIONID,'CASTGC':CASTGC}
        except Exception:
            traceback.print_exc()

    def login(self, username, password):
        try:
            req = self.sess.get(self.login_url, headers=self.headers,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            soup = BeautifulSoup(req.text, 'lxml')
            lt = soup.find('input',{"name":"lt"}).get("value")
            # print('lt:'+lt)
            execution = soup.find('input',{"name":"execution"}).get("value")
            # print('execution:'+execution)
            eventId = soup.find('input',{"name":"_eventId"}).get("value")
            # print('eventId:'+eventId)
            self.cookies = self.sess.cookies
            login_data = {
                'username': username,
                'password': password,
                'lt': lt,
                'execution': execution,
                '_eventId': eventId,
                'rmShown': "1"
            }
            self.req = self.sess.post(self.login_url, headers=self.headers,cookies=self.cookies,
                                    data=login_data,allow_redirects=False,
                                    proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            JSESSIONID = requests.utils.dict_from_cookiejar(self.cookies)["JSESSIONID"]
            try:
                CASTGC = requests.utils.dict_from_cookiejar(self.cookies)["CASTGC"]
            except Exception as e:
                return {'err':"用户名或密码错误"}
            self.st_url = self.req.headers['Location']
            self.sess.get(self.st_url,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            # 图书馆cookies部分
            self.req = self.sess.post(self.library_url, headers=self.headers,cookies=self.cookies,allow_redirects=False,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            self.st_url = self.req.headers['Location']
            ST = parse.urlparse(self.st_url).query[7:]
            self.sess.get(self.st_url,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            return {'JSESSIONID':JSESSIONID,'CASTGC':CASTGC,'PHPSESSID':ST}
        except Exception:
            traceback.print_exc()
        
from bs4 import BeautifulSoup
import re
import time
import requests
import json
import traceback
from urllib import parse

class Personal(object):
    def __init__(self, cookies):
        self.login_url = 'http://ids.xcc.edu.cn/authserver/login?service=http%3A%2F%2Fopac.xcc.edu.cn%3A8080%2Freader%2Fhwthau.php'
        self.st_url = ''
        self.index_url = 'http://opac.xcc.edu.cn:8080/reader/redr_info.php'
        self.info_url = 'http://opac.xcc.edu.cn:8080/reader/redr_info_rule.php'
        self.booklist_url = 'http://opac.xcc.edu.cn:8080/reader/book_lst.php'
        self.bookhist_url = 'http://opac.xcc.edu.cn:8080/reader/book_hist.php'
        self.bookdetail_url = 'http://opac.xcc.edu.cn:8080/opac/item.php?marc_no='
        self.paylist_url = 'http://opac.xcc.edu.cn:8080/reader/account.php'
        self.paydetail_url = 'http://opac.xcc.edu.cn:8080/reader/fine_pec.php'
        self.sess = requests.Session()
        self.cookies = {'PHPSESSID':cookies['PHPSESSID']}
        self.req = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            }
    
    def get_info(self):
        try:
            index_req = self.sess.get(self.index_url, headers=self.headers,cookies=self.cookies,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            index_soup = BeautifulSoup(index_req.text, 'lxml')
            access_list = []
            for a in index_soup.find_all(class_="bigger-170"):
                access_list.append(a.get_text())
            max_borrow = access_list[0].strip()
            max_order = access_list[1].strip()
            max_trust = access_list[2].strip()
            percent = index_soup.find(class_="Num").get_text()
            info_req = self.sess.get(self.info_url, headers=self.headers,cookies=self.cookies,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            info_soup = BeautifulSoup(info_req.text,'lxml')
            table = info_soup.find('div',{'id':"mylib_info"})
            info_list = []
            for i in range(0,9):
                tr = table.find_all('tr')[i]
                list = re.findall(r'：(.*)',tr.text)
                for j in list:
                    info_list.append(j)
            res = {
                'name':info_list[0],
                'license_start':info_list[4],
                'license_work':info_list[5],
                'license_end':info_list[3],
                'max_borrow':max_borrow,
                'max_order':max_order,
                'max_trust':max_trust,
                'overdue':index_soup.find_all('span',class_='infobox-data-number')[0].get_text(),
                'type':info_list[9],
                'level':info_list[10],
                'since':info_list[11],
                'breaks':info_list[12],
                'break_money':info_list[13],
                'sex':info_list[20],
                'deposit':info_list[27],
                'charge':info_list[28],
                'percent':percent
            }
            return res
        except Exception:
            traceback.print_exc()

    def book_list(self):
        try:
            booklist_req = self.sess.get(self.booklist_url, headers=self.headers,cookies=self.cookies,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            booklist_soup = BeautifulSoup(booklist_req.text,'lxml')
            if booklist_soup.find(class_='iconerr') is not None:
                return {'err':"当前无借阅"}
            table = booklist_soup.find('table')
            trs = table.find_all('tr')
            res = {
                'now': booklist_soup.find('div',id='mylib_content').find('p',style='margin:10px auto;').find_all('b')[0].get_text().strip(),
                'max': booklist_soup.find('div',id='mylib_content').find('p',style='margin:10px auto;').find_all('b')[1].get_text().strip(),
                'list':[{
                    'barcode':trs[i].find_all('td')[0].get_text(),
                    'book_name':trs[i].find_all('td')[1].a.get_text(),
                    'marc_no':trs[i].find_all('td')[1].a["href"][25:],
                    'bdate':trs[i].find_all('td')[2].get_text(),
                    'sdate':trs[i].find_all('td')[3].get_text().strip(),
                    'cnum':trs[i].find_all('td')[4].get_text(),
                    'location':trs[i].find_all('td')[5].get_text()
                }for i in range(1,len(trs))]
            }
            return res
        except Exception:
            traceback.print_exc()
    
    def book_hist(self):
        try:
            bookhist_req = self.sess.post(self.bookhist_url, headers=self.headers,cookies=self.cookies,data={'para_string':"all"},proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            bookhist_soup = BeautifulSoup(bookhist_req.text,'lxml')
            if bookhist_soup.find(class_='iconerr') is not None:
                return {'err':"无历史借阅"}
            table = bookhist_soup.find('table')
            trs = table.find_all('tr')
            res = [{
                'index':trs[i].find_all('td')[0].get_text(),
                'barcode':trs[i].find_all('td')[1].get_text(),
                'book_name':trs[i].find_all('td')[2].a.get_text(),
                'marc_no':trs[i].find_all('td')[2].a["href"][25:],
                'author':trs[i].find_all('td')[3].get_text(),
                'start_time':trs[i].find_all('td')[4].get_text(),
                'back_time':trs[i].find_all('td')[5].get_text(),
                'location':trs[i].find_all('td')[6].get_text()
            }for i in range(1,len(trs))]
            return res
        except Exception:
            traceback.print_exc()
    
    def paylist(self):
        try:
            paylist_req = self.sess.post(self.paylist_url, headers=self.headers,cookies=self.cookies,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            paylist_soup = BeautifulSoup(paylist_req.text, 'lxml')
            if paylist_soup.find(class_='iconerr') is not None:
                return {'err':"无账目清单"}
            table = paylist_soup.find('table')
            trs = table.find_all('tr')
            sta = "".join(trs[len(trs)-1].find_all('td')[0].get_text().strip().split())
            res = {
                'sta':sta[sta.find(':')+1:][:sta[sta.find(':')+1:].find('(')],
                'list':[{
                    'date':trs[i].find_all('td')[0].get_text().strip(),
                    'type':trs[i].find_all('td')[1].get_text().strip(),
                    'bm':trs[i].find_all('td')[2].get_text().strip(),
                    'sm':trs[i].find_all('td')[3].get_text().strip(),
                    'way':trs[i].find_all('td')[4].get_text().strip(),
                    'bill':trs[i].find_all('td')[5].get_text().strip()
                }for i in range(1,len(trs)-1)]
            }
            return res
        except Exception:
            traceback.print_exc()
    
    def paydetail(self):
        try:
            paydetail_req = self.sess.post(self.paydetail_url, headers=self.headers,cookies=self.cookies,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            paydetail_soup = BeautifulSoup(paydetail_req.text, 'lxml')
            # status = 1
            for i in paydetail_soup.find_all(class_='iconerr'):
                # if "违章记录" not in i.get_text():
                #     # status = 0
                #     return {'err':"有违章记录，请联系管理员"}
                if "欠款记录为空" in i.get_text():
                    # status = 0
                    return {'err':"无缴费记录"}
            table = paydetail_soup.find('h2',text='欠款信息').find_next_sibling()
            trs = table.find_all('tr')
            res = [{
                    'barcode':trs[i].find_all('td')[0].get_text().strip(),
                    'position':trs[i].find_all('td')[1].get_text().strip(),
                    'book_name':trs[i].find_all('td')[2].a.get_text().strip(),
                    'marc_no':trs[i].find_all('td')[2].a["href"][25:],
                    'author':trs[i].find_all('td')[3].get_text().strip(),
                    'bd':trs[i].find_all('td')[4].get_text().strip(),
                    'sd':trs[i].find_all('td')[5].get_text().strip(),
                    'location':trs[i].find_all('td')[6].get_text().strip(),
                    'sp':trs[i].find_all('td')[7].get_text().strip(),
                    'ap':trs[i].find_all('td')[8].get_text().strip(),
                    'sta':trs[i].find_all('td')[9].get_text().strip()
                }for i in range(1,len(trs))]
            return res
        except Exception:
            traceback.print_exc()

class Search(object):
    def __init__(self):
        self.search_url = 'http://opac.xcc.edu.cn:8080/opac/openlink.php?onlylendable=yes&'
        self.bookdetail_url = 'http://opac.xcc.edu.cn:8080/opac/item.php?marc_no='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            }
    
    def search_book(self,type,content,page):
        try:
            search_result_req = requests.get(self.search_url + type + "=" + content + "&page=" + page, headers=self.headers,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            search_result_soup = BeautifulSoup(search_result_req.text,'lxml')
            mainbox = search_result_soup.find('div',id='content')
            num = mainbox.find('strong',class_='red').get_text()
            search_list = mainbox.find('ol',id='search_book_list').find_all('li')
            try:
                pages = mainbox.find('span',class_='num_prev').find('font',color='black').get_text()
            except:
                pages = "1"
            res = {
                'type': type,
                'content': content,
                'num': num,
                'page': page,
                'pages': pages,
                'list': [{
                    'type': search_list[i].h3.span.get_text(),
                    'title': search_list[i].h3.a.get_text()[search_list[i].h3.a.get_text().find('.')+1:],
                    'author': [text.strip() for text in search_list[i].p.find_all(text=True) if text.parent.name !='span' and text.strip()][0],
                    'code': [text.strip() for text in search_list[i].h3.find_all(text=True) if text.parent.name !='span' and text.parent.name != 'a' and text.strip()][0],
                    'publish': "".join([text.strip() for text in search_list[i].p.find_all(text=True) if text.parent.name !='span' and text.strip()][1].split()),
                    'marc_no': search_list[i].h3.a['href'][17:],
                    'status': re.findall(r'：(\d*)',search_list[i].p.span.get_text())
                }for i in range(0,len(search_list))]
            }
            return res
        except Exception:
            traceback.print_exc()

    def book_detail(self,marc_no):
        try:
            bookdetail_req = requests.get(self.bookdetail_url + marc_no, headers=self.headers,proxies={'http':'http://47.103.26.218:2589'},timeout=5)
            bookdetail_soup = BeautifulSoup(bookdetail_req.text,'lxml')
            bookdetail_info = bookdetail_soup.find(id='item_detail')
            bookdetail_status = bookdetail_soup.find('table',id='item')
            dls = bookdetail_info.find_all('dl')
            trs = bookdetail_status.find_all('tr')
            res = {'isbn':[],'author_oth':[]}
            for i in range(0,len(dls)):
                if "题名/责任者" in dls[i].dt.get_text():
                    res['title'] = dls[i].dd.a.get_text()
                    res['hole'] = dls[i].dd.get_text()
                if "出版发行项" in dls[i].dt.get_text():
                    res['imprint'] = dls[i].dd.get_text()
                if "ISBN及定价" in dls[i].dt.get_text():
                    res['isbn'].append(dls[i].dd.get_text())
                if "载体形态项" in dls[i].dt.get_text():
                    res['physical'] = dls[i].dd.get_text()
                if "其它题名" in dls[i].dt.get_text():
                    res['title_oth'] = dls[i].dd.a.get_text()
                if  dls[i].dt.get_text() == "个人责任者:":
                    res['author'] = dls[i].dd.a.get_text()
                if  dls[i].dt.get_text() == "个人次要责任者:":
                    res['author_oth'].append(dls[i].dd.a.get_text())
                if "学科主题" in dls[i].dt.get_text():
                    res['category'] = dls[i].dd.get_text()
                if "中图法分类号" in dls[i].dt.get_text():
                    res['position'] = dls[i].dd.a.get_text()
                if "一般附注" in dls[i].dt.get_text():
                    res['notes'] = dls[i].dd.get_text()
                if "责任者附注" in dls[i].dt.get_text():
                    res['author_notes'] = dls[i].dd.get_text()
                if "提要文摘附注" in dls[i].dt.get_text():
                    res['contents'] = dls[i].dd.get_text()
            res['status'] = [{
                'position':trs[j].find_all('td')[0].get_text(),
                'code':trs[j].find_all('td')[1].get_text(),
                'date':"".join(trs[j].find_all('td')[2].get_text().split()),
                'library':trs[j].find_all('td')[3].get_text().strip(),
                'about':trs[j].find_all('td')[3].get('title'),
                'now':trs[j].find_all('td')[4].get_text(),
            }for j in range(1,len(trs))]
            return res
        except Exception:
            traceback.print_exc()
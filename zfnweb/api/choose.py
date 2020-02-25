# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import time
import requests
import json
from urllib import parse
from requests import exceptions


class Xuanke(object):
    def __init__(self, base_url, cookies):
        self.base_url = base_url
        self.headers = {
            'Referer': base_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        self.cookies = cookies
        with open('config.json',mode='r',encoding='utf-8') as f:
            config = json.loads(f.read())
        self.proxies = {
            'http':config["proxy"]
        }
        self.nowyear = str(int(time.strftime("%Y", time.localtime())) - 1)
        self.nowterm = config["nowterm"]
    
    def get_choosed(self):
        """获取已选课程信息"""
        try:
            choosed_url = parse.urljoin(self.base_url,'/xsxk/zzxkyzb_cxZzxkYzbChoosedDisplay.html?gnmkdm=N253512')
            data = {
                'xkxnm': self.nowyear,
                'xkxqm': self.nowterm
            }
            try:
                res = requests.post(choosed_url, data = data, headers = self.headers, cookies=self.cookies, proxies=self.proxies, timeout=(5,15))
            except exceptions.Timeout as e:
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=已选超时&desp=' + str(e))
                return {'err':'Connect Timeout'}
            jres = res.json()
            res_dict = {
                'courseNumber':len(jres), #已选课程数
                'items':[{
                    'courseTitle':i["kcmc"],
                    'courseCategory':i["kklxmc"],
                    'teacher':(re.findall(r"/(.*?)/",i["jsxx"]))[0],
                    'teacher_id':(re.findall(r"(.*?\d+)/",i["jsxx"]))[0],
                    'classId':i["jxb_id"],
                    'classVolume':int(i["jxbrs"]),
                    'classPeople':int(i["yxzrs"]),
                    'courseRoom':(i["jxdd"].split('<br/>'))[0] if '<br/>' in i["jxdd"] else i["jxdd"],
                    'courseId':i["kch"],
                    'courseTime':(i["sksj"].split('<br/>'))[0] + '、' + (i["sksj"].split('<br/>'))[1] if '<br/>' in i["sksj"] else i["sksj"],
                    'credit':float(i["xf"]),
                    'chooseSelf':int(i["zixf"]),
                    'waiting':i["sxbj"]
                    } for i in jres]
            }
            return res_dict
        except Exception as e:
            print(e)
    
    def get_bkk_list(self,bkk):
        """获取板块课选课列表"""
        try:
            """获取head_data"""
            sessions = requests.Session()
            url_data1 = parse.urljoin(self.base_url,'/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default')
            data1 = sessions.get(url_data1, headers = self.headers, cookies=self.cookies, proxies=self.proxies, timeout=(5,15))
            data1.encoding = data1.apparent_encoding
            soup = BeautifulSoup(data1.text,'html.parser')

            gotCredit_list = []
            for gotCredit_content in soup.find_all('font',color=re.compile('red')):
                gotCredit_list.append(gotCredit_content)
            gotCredit = gotCredit_list[2].string

            kklxdm_list = []
            xkkz_id_list = []
            for tab_content in soup.find_all('a',role=re.compile('tab')):
                onclick_content = tab_content.get('onclick')
                r = re.findall(r"'(.*?)'",str(onclick_content))
                kklxdm_list.append(r[0].strip())
                xkkz_id_list.append(r[1].strip())
            tab_list = [(kklxdm_list[0],xkkz_id_list[0]),(kklxdm_list[1],xkkz_id_list[1]),(kklxdm_list[2],xkkz_id_list[2])]
            tab_list = [('bkk1_kklxdm',kklxdm_list[0]),('bkk2_kklxdm',kklxdm_list[1]),('bkk3_kklxdm',kklxdm_list[2]),('bkk1_xkkz_id',xkkz_id_list[0]),('bkk2_xkkz_id',xkkz_id_list[1]),('bkk3_xkkz_id',xkkz_id_list[2])]
            tab_dict = dict(tab_list)

            data1_dict = {}
            data1_list = []
            for data1_content in soup.find_all('input',type=re.compile('hidden')):
                name = data1_content.get('name')
                value = data1_content.get('value')
                data1_list.append((str(name),str(value)))
            data1_dict = dict(data1_list)
            data1_dict.update(gotCredit=gotCredit)
            data1_dict.update(tab_dict)

            url_data2 = parse.urljoin(self.base_url,'/xsxk/zzxkyzb_cxZzxkYzbDisplay.html?gnmkdm=N253512')
            data2_data = {
                'xkkz_id': data1_dict["bkk" + bkk + "_xkkz_id"],
                'xszxzt': '1',
                'kspage': '0'
            }
            data2 = sessions.post(url_data2, headers=self.headers, data = data2_data, cookies=self.cookies, proxies=self.proxies, timeout=(5,15))
            data2.encoding = data2.apparent_encoding
            soup2 = BeautifulSoup(data2.text,'html.parser')
            data2_list = []
            for data2_content in soup2.find_all('input',type=re.compile('hidden')):
                name = data2_content.get('name')
                value = data2_content.get('value')
                data2_list.append((str(name),str(value)))
            data2_dict = dict(data2_list)
            data1_dict.update(data2_dict)
            #print(data2_dict)
            head_data = data1_dict
            
            """获取课程列表"""
            url_kch = parse.urljoin(self.base_url,'/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512')
            url_bkk = parse.urljoin(self.base_url,'/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512')
            kch_data = {
                'bklx_id': head_data["bklx_id"],
                'xqh_id': head_data["xqh_id"],
                'zyfx_id': head_data["zyfx_id"],
                'njdm_id': head_data["njdm_id"],
                'bh_id': head_data["bh_id"],
                'xbm': head_data["xbm"],
                'xslbdm': head_data["xslbdm"],
                'ccdm': head_data["ccdm"],
                'xsbj': head_data["xsbj"],
                'xkxnm': self.nowyear,
                'xkxqm': self.nowterm,
                'kklxdm': head_data["bkk" + bkk + "_kklxdm"],
                'kkbk': head_data["kkbk"],
                'rwlx': head_data["rwlx"],
                'kspage': '1',
                'jspage': '10'
            }
            kch_res = sessions.post(url_kch, headers=self.headers, data = kch_data, cookies=self.cookies, proxies=self.proxies, timeout=(5,15))
            jkch_res = kch_res.json()
            bkk_data = {
                'bklx_id': head_data["bklx_id"],
                'xkxnm': self.nowyear,
                'xkxqm': self.nowterm,
                'xkkz_id': head_data["bkk" + bkk + "_xkkz_id"],
                'xqh_id': head_data["xqh_id"],
                'zyfx_id': head_data["zyfx_id"],
                'njdm_id': head_data["njdm_id"],
                'bh_id': head_data["bh_id"],
                'xbm': head_data["xbm"],
                'xslbdm': head_data["xslbdm"],
                'ccdm': head_data["ccdm"],
                'xsbj': head_data["xsbj"],
                'kklxdm': head_data["bkk" + bkk + "_kklxdm"],
                'kch_id': jkch_res["tmpList"][0]["kch_id"],
                'kkbk': head_data["kkbk"],
                'rwlx': head_data["rwlx"],
                'zyh_id': head_data["zyh_id"]
            }
            bkk_res = sessions.post(url_bkk, headers=self.headers, data = bkk_data, cookies=self.cookies, proxies=self.proxies, timeout=(5,15))
            jbkk_res = bkk_res.json()
            if bkk != '3' and (len(jkch_res["tmpList"]) != len(jbkk_res)):
                res_dict = {'error':'ErrorLength'}
                return res_dict
            list1 = jkch_res["tmpList"]
            list2 = jbkk_res
            for i in range(0,len(list1)):
                list1[i].update(list2[i])

            res_dict = {
                'courseNumber':len(list1),
                'items':[{
                    'courseTitle':j["kcmc"],
                    'teacher':(re.findall(r"/(.*?)/",j["jsxx"]))[0],
                    'teacher_id':(re.findall(r"(.*?\d+)/",j["jsxx"]))[0],
                    'classId':j["jxb_id"],
                    'doId':j["do_jxb_id"],
                    'classVolume':int(j["jxbrl"]),
                    'classPeople':int(j["yxzrs"]),
                    'courseRoom':(j["jxdd"].split('<br/>'))[0] if '<br/>' in j["jxdd"] else j["jxdd"],
                    'courseId':j["kch_id"],
                    'courseTime':(j["sksj"].split('<br/>'))[0] + '、' + (j["sksj"].split('<br/>'))[1] if '<br/>' in j["sksj"] else j["sksj"],
                    'credit':float(j["xf"]),
                    }for j in list1]
            }
            return res_dict

        except Exception as e:
            print(e)

    #def choose(self,bkk,classId):
    #    list_data = self.get_bkk_list(bkk)
    #    url_choose = parse.urljoin(self.base_url)
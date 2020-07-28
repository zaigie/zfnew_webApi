# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import time
import requests
import json
from urllib import parse
from requests import exceptions

with open('config.json', mode='r', encoding='utf-8') as f:
    config = json.loads(f.read())


class GetInfo(object):
    def __init__(self, base_url, cookies):
        self.base_url = base_url
        self.headers = {
            'Referer': base_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        self.cookies = cookies
        if config["proxy"] == "none":
            self.proxies = None
        else:
            self.proxies = {
                'http': config["proxy"]
            }

    @staticmethod
    def calTime(args):
        """根据config.json返回上下课时间"""
        num1 = str(args[0])
        num2 = str(args[1])
        k1 = config["TimesUp"][num1]
        k2 = config["TimesDown"][num2]
        r = k1 + '~' + k2
        return r

    @staticmethod
    def upTime(args):
        """根据config.json计算上课时间"""
        num1 = str(args[0])
        k1 = config["TimesUp"][num1]
        return k1

    @staticmethod
    def listTime(args):
        """返回该课程为第几节到第几节"""
        num1 = int(args[0])
        num2 = int(args[1])
        itemList = []
        for i in range(num1, num2+1):
            itemList.append(i)
        return itemList

    @staticmethod
    def term_cn(xh, year, term):
        """计算培养方案具体学期"""
        if year is None or term is None:
            return "未知"
        grade = "None"
        nj = int(xh[0:2])
        xnm = int(year[2:4])
        xqm = int(term)
        if xnm == nj:
            if xqm == 1:
                grade = '大一上'
            elif xqm == 2:
                grade = '大一下'
        elif xnm == nj + 1:
            if xqm == 1:
                grade = '大二上'
            elif xqm == 2:
                grade = '大二下'
        elif xnm == nj + 2:
            if xqm == 1:
                grade = '大三上'
            elif xqm == 2:
                grade = '大三下'
        elif xnm == nj + 3:
            if xqm == 1:
                grade = '大四上'
            elif xqm == 2:
                grade = '大四下'
        return grade

    @staticmethod
    def calWeeks(args):
        """返回课程所含周列表"""
        if len(args) == 1:
            num = int(args[0])
            firstlist = [num]
            return firstlist
        elif len(args) == 2:
            k1 = int(args[0])
            k2 = int(args[1])
            r = []
            for n in range(k1, k2 + 1):
                r.append(n)
            return r
        elif len(args) == 3:
            k12 = int(args[0])
            k22 = int(args[1])
            r2 = []
            for n2 in range(k12, k22 + 1):
                r2.append(n2)
            r2.append(int(args[2]))
            return r2
        elif len(args) == 4:
            num1 = int(args[0])
            num2 = int(args[1])
            num3 = int(args[2])
            num4 = int(args[3])
            clist = []
            for i in range(num1, num2 + 1):
                clist.append(i)
            for j in range(num3, num4 + 1):
                clist.append(j)
            return clist
        else:
            return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

    def get_pinfo(self):
        """获取个人信息"""
        url = parse.urljoin(self.base_url, '/xsxxxggl/xsxxwh_cxCkDgxsxx.html?gnmkdm=N100801')
        try:
            res = requests.get(url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, timeout=(5, 10))
        except exceptions.Timeout as e:
            ServerChan = config["ServerChan"]
            text = "个人信息超时"
            if ServerChan is "none":
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
            else:
                requests.get(ServerChan + 'text=' + text + '&desp=' + str(e))
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
        jres = res.json()
        # print(jres)
        res_dict = {
            'name': '无' if jres.get('xm') is None else jres.get('xm'),
            'studentId': '无' if jres.get('xh') is None else jres.get('xh'),
            'birthDay': '无' if jres.get('csrq') is None else jres.get('csrq'),
            'idNumber': '无' if jres.get('zjhm') is None else jres.get('zjhm'),
            'candidateNumber': '无' if jres.get('ksh') is None else jres.get('ksh'),
            'status': '无' if jres.get('xjztdm') is None else jres.get('xjztdm'),
            'collegeName': jres.get('jg_id') if jres.get('zsjg_id') is None else jres.get('zsjg_id'),
            'majorName': jres.get('zyh_id') if jres.get('zszyh_id') is None else jres.get('zszyh_id'),
            'className': jres.get('xjztdm') if jres.get('bh_id') is None else jres.get('bh_id'),
            'entryDate': '无' if jres.get('rxrq') is None else jres.get('rxrq'),
            'graduationSchool': '无' if jres.get('byzx') is None else jres.get('byzx'),
            'domicile': '无' if jres.get('jg') is None else jres.get('jg'),
            'phoneNumber': '无' if jres.get('sjhm') is None else jres.get('sjhm'),
            'parentsNumber': '无' if jres.get('gddh') is None else jres.get('gddh'),
            'email': '无' if jres.get('dzyx') is None else jres.get('dzyx'),
            'politicalStatus': '无' if jres.get('zzmmm') is None else jres.get('zzmmm'),
            'national': '无' if jres.get('mzm') is None else jres.get('mzm'),
            'education': '无' if jres.get('pyccdm') is None else jres.get('pyccdm'),
            'postalCode': '无' if jres.get('yzbm') is None else jres.get('yzbm'),
            'grade': int(jres.get('xh')[0:2])
        }
        return res_dict

    def get_now_class(self):
        """获取当前班级"""
        url = parse.urljoin(self.base_url, '/xsxxxggl/xsxxwh_cxCkDgxsxx.html?gnmkdm=N100801')
        try:
            res = requests.get(url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, timeout=(5, 10))
        except exceptions.Timeout as e:
            ServerChan = config["ServerChan"]
            text = "个人信息超时"
            if ServerChan is "none":
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
            else:
                requests.get(ServerChan + 'text=' + text + '&desp=' + str(e))
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
        jres = res.json()
        return jres.get('xjztdm') if jres.get('bh_id') is None else jres.get('bh_id')

    def cat_by_courseid(self, courseid):
        """根据课程号获取类别"""
        url = parse.urljoin(self.base_url, '/jxjhgl/common_cxKcJbxx.html?id='+ courseid)
        res = requests.get(url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, timeout=(5, 10))
        soup = BeautifulSoup(res.text, 'html.parser')
        th_list = soup.find_all('th')
        data_list = []
        for content in th_list:
            if (content.text).strip() != "":
                data_list.append((content.text).strip())
        try:
            return data_list[5]
        except exceptions.Timeout as e:
            print(str(e))
            return '未知类别'

    def gpa_only(self):
        url_main = parse.urljoin(self.base_url, '/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&layout=default')
        mainr = requests.get(url_main, headers=self.headers, cookies=self.cookies, proxies=self.proxies,
                            timeout=(5, 10))
        mainr.encoding = mainr.apparent_encoding
        soup = BeautifulSoup(mainr.text, 'html.parser')
        allc_str = []
        for allc in soup.find_all('font', size=re.compile('2px')):
            allc_str.append(allc.get_text())
        gpa = float(allc_str[2])
        try:
            if gpa != "":
                return gpa
            else:
                return "init"
        except exceptions.Timeout as e:
            print(str(e))
            return "init"

    def get_study(self, xh):
        """获取学业情况"""
        sessions = requests.Session()

        url_main = parse.urljoin(self.base_url, '/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&layout=default')
        url_info = parse.urljoin(self.base_url, '/xsxy/xsxyqk_cxJxzxjhxfyqKcxx.html?gnmkdm=N105515')
        try:
            mainr = sessions.get(url_main, headers=self.headers, cookies=self.cookies, proxies=self.proxies,
                                 timeout=(5, 10))
        except exceptions.Timeout as e:
            ServerChan = config["ServerChan"]
            text = "学业超时"
            if ServerChan == "none":
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
            else:
                requests.get(ServerChan + 'text=' + text + '&desp=' + str(e))
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
        mainr.encoding = mainr.apparent_encoding
        soup = BeautifulSoup(mainr.text, 'html.parser')

        allc_str = []
        for allc in soup.find_all('font', size=re.compile('2px')):
            allc_str.append(allc.get_text())
        gpa = float(allc_str[2])
        allc_num = re.findall(r"\d+", allc_str[3])
        allc_num2 = re.findall(r"\d+", allc_str[5])
        allc_num.append(allc_num2[0])
        ipa = int(allc_num[0])
        ipp = int(allc_num[1])
        ipf = int(allc_num[2])
        ipn = int(allc_num[3])
        ipi = int(allc_num[4])
        allc_num3 = re.findall(r"\d+", allc_str[6])
        allc_num4 = re.findall(r"\d+", allc_str[7])
        opp = int(allc_num3[0])
        opf = int(allc_num4[0])

        id_find = re.findall(r"xfyqjd_id='(.*)' jdkcsx='1' leaf=''", str(soup))
        idList = list({}.fromkeys(id_find).keys())
        tsid = "None"
        tzid = "None"
        zyid = "None"
        qtid = "None"
        if xh[0:2] != '19':  # 本校特色，19级因更改了培养方案导致id非体系，可根据自己学校的返回更改
            # match = '20' + xh[0:6]
            for i in idList:
                if re.findall(r"tsjy", i):
                    tsid = i[0:14]
                elif re.findall(r"tzjy", i):
                    tzid = i[0:14]
                elif re.findall(r"zyjy", i):
                    zyid = i[0:14]
                elif re.findall(r"qtkcxfyq", i):
                    qtid = i
        else:
            tsid = idList[0]
            tzid = idList[2]
            zyid = idList[1]
            qtid = idList[3]

        res_ts = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': tsid}, cookies=self.cookies,
                               proxies=self.proxies, timeout=(5, 10))
        res_tz = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': tzid}, cookies=self.cookies,
                               proxies=self.proxies, timeout=(5, 10))
        res_zy = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': zyid}, cookies=self.cookies,
                               proxies=self.proxies, timeout=(5, 10))
        res_qt = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': qtid}, cookies=self.cookies,
                               proxies=self.proxies, timeout=(5, 10))

        ts_point_find = re.findall(r"通识教育&nbsp;要求学分:(\d+\.\d+)&nbsp;获得学分:(\d+\.\d+)&nbsp;&nbsp;未获得学分:(\d+\.\d+)&nbsp",
                                   str(soup))
        ts_point_list = list(list({}.fromkeys(ts_point_find).keys())[0])  # 先得到元组再拆开转换成列表
        ts_point = {
            'tsr': ts_point_list[0],
            'tsg': ts_point_list[1],
            'tsn': ts_point_list[2]
        }
        tz_point_find = re.findall(r"拓展教育&nbsp;要求学分:(\d+\.\d+)&nbsp;获得学分:(\d+\.\d+)&nbsp;&nbsp;未获得学分:(\d+\.\d+)&nbsp",
                                   str(soup))
        tz_point_list = list(list({}.fromkeys(tz_point_find).keys())[0])
        tz_point = {
            'tzr': tz_point_list[0],
            'tzg': tz_point_list[1],
            'tzn': tz_point_list[2]
        }
        zy_point_find = re.findall(r"专业教育&nbsp;要求学分:(\d+\.\d+)&nbsp;获得学分:(\d+\.\d+)&nbsp;&nbsp;未获得学分:(\d+\.\d+)&nbsp",
                                   str(soup))
        zy_point_list = list(list({}.fromkeys(zy_point_find).keys())[0])
        zy_point = {
            'zyr': zy_point_list[0],
            'zyg': zy_point_list[1],
            'zyn': zy_point_list[2]
        }
        res_main = {
            'gpa': gpa,  # 平均学分绩点GPA
            'ipa': ipa,  # 计划内总课程数
            'ipp': ipp,  # 计划内已过课程数
            'ipf': ipf,  # 计划内未过课程数
            'ipn': ipn,  # 计划内未修课程数
            'ipi': ipi,  # 计划内在读课程数
            'opp': opp,  # 计划外已过课程数
            'opf': opf,  # 计划外未过课程数
            'tsData': {
                'tsPoint': ts_point,  # 通识教育学分情况
                'tsItems': [{
                    'courseTitle': j.get('KCMC'),
                    'courseId': j.get('KCH'),
                    'courseSituation': j.get('XDZT'),
                    'courseTerm': self.term_cn(xh, j.get('JYXDXNM'), j.get('JYXDXQMC')),
                    'courseCategory': '无' if j.get('KCLBMC') is None else j.get('KCLBMC'),
                    'courseAttribution': '无' if j.get('KCXZMC') is None else j.get('KCXZMC'),
                    'maxGrade': ' ' if j.get('MAXCJ') is None else j.get('MAXCJ'),
                    'credit': ' ' if j.get('XF') is None else format(float(j.get('XF')),'.1f'),
                    'gradePoint': ' ' if j.get('JD') is None else format(float(j.get('JD')),'.1f'),
                } for j in res_ts.json()],  # 通识教育修读情况
            },
            'tzdata': {
                'tzPoint': tz_point,  # 拓展教育学分情况
                'tzItems': [{
                    'courseTitle': k.get('KCMC'),
                    'courseId': k.get('KCH'),
                    'courseSituation': k.get("XDZT"),
                    'courseTerm': self.term_cn(xh, k.get("JYXDXNM"), k.get("JYXDXQMC")),
                    'courseCategory': '无' if k.get('KCLBMC') is None else k.get('KCLBMC'),
                    'courseAttribution': '无' if k.get('KCXZMC') is None else k.get('KCXZMC'),
                    'maxGrade': ' ' if k.get('MAXCJ') is None else k.get("MAXCJ"),
                    'credit': ' ' if k.get('XF') is None else format(float(k.get("XF")),'.1f'),
                    'gradePoint': ' ' if k.get('JD') is None else format(float(k.get("JD")),'.1f'),
                } for k in res_tz.json()],  # 拓展教育修读情况
            },
            'zydata': {
                'zyPoint': zy_point,  # 专业教育学分情况
                'zyItems': [{
                    'courseTitle': l.get("KCMC"),
                    'courseId': l.get("KCH"),
                    'courseSituation': l.get("XDZT"),
                    'courseTerm': self.term_cn(xh, l.get("JYXDXNM"), l.get("JYXDXQMC")),
                    'courseCategory': '无' if l.get('KCLBMC') is None else l.get('KCLBMC'),
                    'courseAttribution': '无' if l.get('KCXZMC') is None else l.get('KCXZMC'),
                    'maxGrade': ' ' if l.get('MAXCJ') is None else l.get("MAXCJ"),
                    'credit': ' ' if l.get('XF') is None else format(float(l.get("XF")),'.1f'),
                    'gradePoint': ' ' if l.get('JD') is None else format(float(l.get("JD")),'.1f'),
                } for l in res_zy.json()],  # 专业教育修读情况
            },
            'qtdata': {
                'qtPoint': '{}',  # 其它课程学分情况
                'qtItems': [{
                    'courseTitle': m.get("KCMC"),
                    'courseId': m.get("KCH"),
                    'courseSituation': m.get("XDZT"),
                    'courseTerm': self.term_cn(xh, m["XNM"], m["XQMMC"]),
                    # 'courseCategory': ' ' if m.get('KCLBMC') is None else m.get('KCLBMC'),
                    'courseCategory': self.cat_by_courseid(m.get("KCH")),
                    'courseAttribution': ' ' if m.get('KCXZMC') is None else m.get('KCXZMC'),
                    'maxGrade': ' ' if m.get('MAXCJ') is None else m.get("MAXCJ"),
                    'credit': ' ' if m.get('XF') is None else format(float(m.get("XF")),'.1f'),
                    'gradePoint': ' ' if m.get('JD') is None else format(float(m.get("JD")),'.1f'),
                } for m in res_qt.json()],  # 其它课程修读情况
            },
        }

        return res_main

    def get_message(self):
        """获取消息"""
        url = parse.urljoin(self.base_url, '/xtgl/index_cxDbsy.html?doType=query')
        data = {
            'sfyy': '0',  # 是否已阅，未阅未1，已阅为2
            'flag': '1',
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': '1000',  # 最多条数
            'queryModel.currentPage': '1',  # 当前页数
            'queryModel.sortName': 'cjsj',
            'queryModel.sortOrder': 'desc',  # 时间倒序, asc正序
            'time': '0'
        }
        try:
            res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies, proxies=self.proxies,
                                timeout=(5, 10))
        except exceptions.Timeout as e:
            ServerChan = config["ServerChan"]
            text = "消息超时"
            if ServerChan == "none":
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
            else:
                requests.get(ServerChan + 'text=' + text + '&desp=' + str(e))
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
        jres = res.json()
        res_list = [{'message': i.get('xxnr'), 'ctime': i.get('cjsj')} for i in jres.get('items')]
        return res_list

    def get_grade(self, year, term):
        """获取成绩"""
        url = parse.urljoin(self.base_url, '/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        elif term == '0':
            term = ''
        else:
            term = config["nowterm"]
            #return {'err': 'Error Term'}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12, 整个学年为空''
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        try:
            res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies, proxies=self.proxies,
                                timeout=(5, 10))
        except exceptions.Timeout as e:
            ServerChan = config["ServerChan"]
            text = "成绩超时"
            if ServerChan == "none":
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
            else:
                requests.get(ServerChan + 'text=' + text + '&desp=' + str(e))
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
        jres = res.json()
        if jres.get('items'):  # 防止数据出错items为空
            res_dict = {
                'name': jres['items'][0]['xm'],
                'gpa': self.gpa_only(),
                'studentId': jres['items'][0]['xh'],
                'schoolYear': jres['items'][0]['xnm'],
                'schoolTerm': jres['items'][0]['xqmmc'],
                'err': 'ok',
                'course': [{
                    'courseTitle': i.get('kcmc'),
                    'teacher': i.get('jsxm'),
                    'courseId': i.get('kch_id'),
                    'className': '无' if i.get('jxbmc') is None else i.get('jxbmc'),
                    'courseNature': '无' if i.get('kcxzmc') is None else i.get('kcxzmc'),
                    'credit': '无' if i.get('xf') is None else format(float(i.get('xf')),'.1f'),
                    'grade': ' ' if i.get('cj') is None else i.get('cj'),
                    'gradePoint': ' ' if i.get('jd') is None else format(float(i.get('jd')),'.1f'),
                    'gradeNature': i.get('ksxz'),
                    'startCollege': '无' if i.get('kkbmmc') is None else i.get('kkbmmc'),
                    'courseMark': i.get('kcbj'),
                    'courseCategory': '无' if i.get('kclbmc') is None else i.get('kclbmc'),
                    'courseAttribution': '无' if i.get('kcgsmc') is None else i.get('kcgsmc')
                } for i in jres.get('items')]}
            return res_dict
        else:
            return {'err': '看起来你这学期好像还没有出成绩，点击顶栏也看看以前的吧~'}

    def get_schedule(self, year, term):
        """获取课程表信息"""
        url = parse.urljoin(self.base_url, '/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            term = config["nowterm"]
            # print('Please enter the correct term value！！！ ("1" or "2")')
            # return {'err': 'Error Term'}
        data = {
            'xnm': year,
            'xqm': term
        }
        try:
            res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies, proxies=self.proxies,
                                timeout=(5, 10))
        except exceptions.Timeout as e:
            ServerChan = config["ServerChan"]
            text = "课表超时"
            if ServerChan == "none":
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
            else:
                requests.get(ServerChan + 'text=' + text + '&desp=' + str(e))
                return {'err': '请求超时，鉴于教务系统特色，已帮你尝试重新登录，重试几次，还不行请麻烦你自行重新登录，或者在关于里面反馈！当然，也可能是教务系统挂了~'}
        jres = res.json()

        res_dict = {
            'name': jres['xsxx']['XM'],
            'studentId': jres['xsxx']['XH'],
            'schoolYear': jres['xsxx']['XNM'],
            'schoolTerm': jres['xsxx']['XQMMC'],
            'normalCourse': [{
                'courseTitle': i.get('kcmc'),
                'courseTitleShort': i.get('kcmc')[0:12] + '..' if len(i.get('kcmc')) > 12 else i.get('kcmc'),
                'teacher': '无' if i.get('xm') is None else i.get('xm'),
                'courseId': i.get('kch_id'),
                'courseWeekday': i.get('xqj'),
                'courseSection': i.get('jc'),
                'includeSection': self.listTime(re.findall(r"(\d+)", i['jc'])),
                'upTime': self.upTime(re.findall(r"(\d+)", i['jc'])),
                'courseTime': self.calTime(re.findall(r"(\d+)", i['jc'])),
                'courseWeek': i.get('zcd'),
                'includeWeeks': self.calWeeks(re.findall(r"(\d+)", i['zcd'])),
                # 'inNowWeek': 1 if int(config["nowWeekI"]) in self.calWeeks(re.findall(r"(\d+)", i['zcd'])) else 0,
                'exam': i.get('khfsmc'),
                'campus': i.get('xqmc'),
                'courseRoom': i.get('cdmc'),
                'className': i.get('jxbmc'),
                'hoursComposition': i.get('kcxszc'),
                'weeklyHours': i.get('zhxs'),
                'totalHours': i.get('zxs'),
                'credit': '0.0' if i.get('xf') == '无' else format(float(i.get('xf')),'.1f')
            } for i in jres['kbList']],
            # 'otherCourses': [i['qtkcgs'] for i in jres['sjkList']]
        }
        return res_dict

    # def get_notice(self):
    #   """获取通知"""
    #    url_0 = parse.urljoin(self.base_url, '/xtgl/index_cxNews.html?localeKey=zh_CN&gnmkdm=index')
    #    url_1 = parse.urljoin(self.base_url, 'xtgl/index_cxAreaTwo.html?localeKey=zh_CN&gnmkdm=index')
    #    res_list = []
    #    url_list = []

    #    res_0 = requests.get(url_0, headers=self.headers, cookies=self.cookies)
    #    res_1 = requests.get(url_1, headers=self.headers, cookies=self.cookies)
    #    soup_0 = BeautifulSoup(res_0.text, 'lxml')
    #    soup_1 = BeautifulSoup(res_1.text, 'lxml')
    #    url_list += [i['href'] for i in soup_0.select('a[href^="/xtgl/"]')]
    #    url_list += [i['href'] for i in soup_1.select('a[href^="/xtgl/"]')]

    #    for u in url_list:
    #        _res = requests.get(self.base_url + u, headers=self.headers, cookies=self.cookies)
    #        _soup = BeautifulSoup(_res.text, 'lxml')
    #        title = _soup.find(attrs={'class': 'text-center'}).string
    #        info = [i.string for i in _soup.select_one('[class="text-center news_title1"]').find_all('span')]
    #        publisher = re.search(r'：(.*)', info[0]).group(1)
    #        ctime = re.search(r'：(.*)', info[1]).group(1)
    #        vnum = re.search(r'：(.*)', info[2]).group(1)
    #        detailed = _soup.find(attrs={'class': 'news_con'})
    #        content = ''.join(list(detailed.strings))
    #        doc_urls = [self.base_url + i['href'][2:] for i in detailed.select('a[href^=".."]')]
    #        res_list.append({
    #            'title': title,
    #            'publisher': publisher,
    #            'ctime': ctime,
    #            'vnum': vnum,
    #            'content': content,
    #            'doc_urls': doc_urls
    #        })
    #    return res_list

    # def get_classroom(self):
    #     """获取空教室信息"""
    #     url = parse.urljoin(self.base_url, '/cdjy/cdjy_cxKxcdlb.html?gnmkdm=N2155&layout=default')
    #     data = {
    #         'fwzt': 'cx',
    #         'xqh_id': '1',
    #         'xnm': '2019',
    #         'xqm': '3',
    #         'cdlb_id': '',
    #         'cdejlb_id': '',
    #         'qszws': '',
    #         'jszws': '',
    #         'cdmc': '',
    #         'lh': '',
    #         'qssd': '',
    #         'jssd': '',
    #         'qssj': '',
    #         'jssj': '',
    #         'jyfs': '0',
    #         'cdjylx': '',
    #         'zcd': '256',
    #         'xqj': '3',
    #         'jcd': '9',
    #         '_search': 'false',
    #         'nd': '1571744696313',
    #         'queryModel.showCount': '50',  # 最多条数
    #         'queryModel.currentPage': '1',
    #         'queryModel.sortName': 'cdbh',
    #         'queryModel.sortOrder': 'asc',
    #         'time': '1'
    #     }
    #     res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
    #     return res

    # def get_exam(self, year, term):
    #    """获取考试信息"""
    #    url = parse.urljoin(self.base_url, '/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105')
    #    if term == '1':  # 修改检测学期
    #        term = '3'
    #    elif term == '2':
    #        term = '12'
    #    else:
    #        print('Please enter the correct term value！！！ ("1" or "2")')
    #        return {}
    #    data = {
    #        'xnm': year,  # 学年数
    #        'xqm': term,  # 学期数，第一学期为3，第二学期为12
    #        '_search': 'false',
    #        'nd': int(time.time() * 1000),
    #        'queryModel.showCount': '100',  # 每页最多条数
    #        'queryModel.currentPage': '1',
    #        'queryModel.sortName': '',
    #        'queryModel.sortOrder': 'asc',
    #        'time': '0'  # 查询次数
    #    }
    #    res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
    #    jres = res.json()
    #    if jres.get('items'):  # 防止数据出错items为空
    #        res_dict = {
    #            'name': jres['items'][0]['xm'],
    #            'studentId': jres['items'][0]['xh'],
    #            'schoolYear': jres['items'][0]['xnmc'][:4],
    #            'schoolTerm': jres['items'][0]['xqmmc'],
    #            'exams': [{
    #                'courseTitle': i['kcmc'],
    #                'teacher': i['jsxx'],
    #                'courseId': i['kch'],
    #                'reworkMark': i['cxbj'],
    #                'selfeditingMark': i['zxbj'],
    #                'examName': i['ksmc'],
    #                'paperId': i['sjbh'],
    #                'examTime': i['kssj'],
    #                'eaxmLocation': i['cdmc'],
    #                'campus': i['xqmc'],
    #                'examSeatNumber': i['zwh']
    #            } for i in jres['items']]}
    #        return res_dict
    #    else:
    #        return {}

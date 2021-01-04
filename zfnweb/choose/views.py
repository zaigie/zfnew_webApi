import datetime
import os
import time

import json
import requests
from api import Xuanke, Login
from django.http import HttpResponse
from info.models import Students
from mp.models import Config

with open('config.json', mode='r', encoding='utf-8') as f:
    config = json.loads(f.read())
base_url = config["base_url"]

def index():
    return HttpResponse('choose_index here')

def cacheData(xh, filename):
    docurl = 'data/' + str(xh)[0:2] + '/' + str(xh) + '/'
    fileurl = docurl + str(filename) + '.json'
    if not os.path.exists(docurl):
        os.makedirs(docurl)
    else:
        if not os.path.exists(fileurl):
            return
        else:
            with open(fileurl, mode='r', encoding='utf-8') as o:
                result = json.loads(o.read())
                return result

def newData(xh, filename, content):
    docurl = 'data/' + str(xh)[0:2] + '/' + str(xh) + '/'
    fileurl = docurl + str(filename) + '.json'
    if not os.path.exists(docurl):
        os.makedirs(docurl)
        with open(fileurl, mode='w', encoding='utf-8') as n:
            n.write(content)
    else:
        with open(fileurl, mode='w', encoding='utf-8') as n:
            n.write(content)
    # if not os.path.exists(fileurl):
    #     with open(fileurl, mode='w', encoding='utf-8') as n:
    #         n.write(content)

def writeLog(content):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'mylogs/' + date + '.log'
    if not os.path.exists(filename):
        with open(filename, mode='w', encoding='utf-8') as n:
            n.write('【%s】的日志记录' % date)
    with open(filename, mode='a', encoding='utf-8') as l:
        l.write('\n%s' % content)


def update_cookies(xh, pswd):
    try:
        stu = Students.objects.get(studentId=int(xh))
        startTime = time.time()
        content = ('【%s】[%s]更新cookies' % (datetime.datetime.now().strftime('%H:%M:%S'), stu.name))
        writeLog(content)
        # print('原cookies：')
        # print('{JSESSIONID:%s,route:%s}' % (stu.JSESSIONID,stu.route))
        lgn = Login(base_url=base_url)
        lgn.login(xh, pswd)
        if lgn.runcode == 1:
            cookies = lgn.cookies
            # person = Xuanke(base_url=base_url, cookies=cookies)
            NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
            nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
            updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute,
                                                              updateTime=updateTime)
            endTime = time.time()
            spendTime = endTime - startTime
            # print('新cookies:')
            content = ('【%s】更新cookies成功，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'), spendTime))
            writeLog(content)
            # print(requests.utils.dict_from_cookiejar(cookies))
            return cookies
        else:
            content = ('【%s】[%s]更新cookies时网络或其他错误！' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse(json.dumps({'err':'网络或token问题'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
    except Exception as e:
        ServerChan = config["ServerChan"]
        text = "更新cookies未知错误"
        if ServerChan == "none":
            return HttpResponse(json.dumps({'err':'更新cookies未知错误'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            requests.get(ServerChan + 'text=' + text + '&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
            return HttpResponse(json.dumps({'err':'更新cookies未知错误'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")


def get_choosed(request):
    """已选课程"""
    myconfig = Config.objects.all().first()
    year = (myconfig.nChoose)[0:4]
    term = (myconfig.nChoose)[4:]
    if term == "1":
        term = "3"
    elif term == "2":
        term = "12"
    if myconfig.apichange:
        data = {
            'xh':request.POST.get("xh"),
            'pswd':request.POST.get("pswd"),
            'refresh':request.POST.get("refresh")
        }
        res = requests.post(url=myconfig.otherapi+"/choose/choosed",data=data)
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if myconfig.maintenance:
        return HttpResponse(json.dumps({'err':'教务系统出错维护中，请静待教务系统恢复正常！'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if request.method == 'POST':
        if request.POST:
            xh = request.POST.get("xh")
            pswd = request.POST.get("pswd")
            refresh = request.POST.get("refresh")
        else:
            return HttpResponse(json.dumps({'err':'请提交正确的post数据'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问已选课程' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse(json.dumps({'err':'还未登录，请重新登录！'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            stu = Students.objects.get(studentId=int(xh))
        if refresh == "no":
            filename = ('Choosed')
            cache = cacheData(xh, filename)
            if cache is not None:
                # print('cache')
                print('【%s】查看了已选缓存' % stu.name)
                return HttpResponse(json.dumps(cache, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
            else:
                pass
        try:
            startTime = time.time()
            print('【%s】查看了已选' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID': JSESSIONID,
                'route': route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = Xuanke(base_url=base_url, cookies=cookies, year=year, term=term)
            choosed = person.get_choosed()
            endTime = time.time()
            spendTime = endTime - startTime
            if choosed is None:
                content = ('【%s】[%s]访问已选课程出错' % (datetime.datetime.now().strftime('%H:%M:%S'), stu.name))
                writeLog(content)
                sta = update_cookies(xh, pswd)
                person = Xuanke(base_url=base_url, cookies=sta, year=year, term=term)
                nchoosed = person.get_choosed()

                filename = ('Choosed')
                newData(xh, filename, json.dumps(nchoosed, ensure_ascii=False))

                return HttpResponse(json.dumps(nchoosed, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
            elif choosed.get('err'):
                ServerChan = config["ServerChan"]
                text = choosed.get('err')
                if ServerChan == "none":
                    return HttpResponse(json.dumps({'err':text}, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                else:
                    requests.get(ServerChan + 'text=' + text)
                    return HttpResponse(json.dumps({'err':'已选课程未知错误'}, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
            else:
                content = ('【%s】[%s]访问了已选课程，耗时%.2fs' % (
                    datetime.datetime.now().strftime('%H:%M:%S'), stu.name, spendTime))
                writeLog(content)

                filename = ('Choosed')
                newData(xh, filename, json.dumps(choosed, ensure_ascii=False))

                return HttpResponse(json.dumps(choosed, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
        except Exception as e:
            # print(e)
            ServerChan = config["ServerChan"]
            text = "已选课程未知错误"
            if ServerChan == "none":
                return HttpResponse(json.dumps({'err':'已选课程未知错误'}, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
            else:
                requests.get(ServerChan + 'text=' + text + '&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
                return HttpResponse(json.dumps({'err':'已选课程未知错误'}, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'err':'请使用post并提交正确数据'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")


def get_bkk_list(request):
    """板块课（通识选修课）"""
    myconfig = Config.objects.all().first()
    year = (myconfig.nChoose)[0:4]
    term = (myconfig.nChoose)[4:]
    if term == "1":
        term = "3"
    elif term == "2":
        term = "12"
    if myconfig.apichange:
        data = {
            'xh':request.POST.get("xh"),
            'pswd':request.POST.get("pswd"),
            'bkk':request.POST.get("bkk")
        }
        res = requests.post(url=myconfig.otherapi+"/choose/bkk",data=data)
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if myconfig.maintenance:
        return HttpResponse(json.dumps({'err':'教务系统出错维护中，请静待教务系统恢复正常！'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if request.method == 'POST':
        if request.POST:
            xh = request.POST.get("xh")
            pswd = request.POST.get("pswd")
            bkk = request.POST.get("bkk")
        else:
            return HttpResponse(json.dumps({'err':'请提交正确的post数据'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问板块课' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse(json.dumps({'err':'还未登录，请重新登录！'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            startTime = time.time()
            print('【%s】查看了板块课' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID': JSESSIONID,
                'route': route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = Xuanke(base_url=base_url, cookies=cookies, year=year, term=term)
            bkk_list = person.get_bkk_list(bkk)
            endTime = time.time()
            spendTime = endTime - startTime
            if spendTime > 30:
                ServerChan = config["ServerChan"]
                text = "板块课超时"
                if ServerChan == "none":
                    return HttpResponse(json.dumps({'err':'板块课超时'}, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                else:
                    requests.get(ServerChan + 'text=' + text)
                    return HttpResponse(json.dumps({'err':'板块课超时'}, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
            content = ('【%s】[%s]访问了板块课，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'), stu.name, spendTime))
            writeLog(content)
            return HttpResponse(json.dumps(bkk_list, ensure_ascii=False), content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问板块课出错' % (datetime.datetime.now().strftime('%H:%M:%S'), stu.name))
            writeLog(content)
            sta = update_cookies(xh, pswd)
            person = Xuanke(base_url=base_url, cookies=sta, year=year, term=term)
            bkk_list = person.get_bkk_list(bkk)
            return HttpResponse(json.dumps(bkk_list, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'err':'请使用post并提交正确数据'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")


def choose(request):
    """选课"""
    myconfig = Config.objects.all().first()
    year = (myconfig.nChoose)[0:4]
    term = (myconfig.nChoose)[4:]
    if term == "1":
        term = "3"
    elif term == "2":
        term = "12"
    if myconfig.apichange:
        data = {
            'xh':request.POST.get("xh"),
            'pswd':request.POST.get("pswd"),
            'doId':request.POST.get("doId"),
            'kcId':request.POST.get("kcId"),
            'kklxdm':request.POST.get("kklxdm")
        }
        res = requests.post(url=myconfig.otherapi+"/choose/choose",data=data)
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if myconfig.maintenance:
        return HttpResponse(json.dumps({'err':'教务系统出错维护中，请静待教务系统恢复正常！'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if request.method == 'POST':
        if request.POST:
            xh = request.POST.get("xh")
            pswd = request.POST.get("pswd")
            doId = request.POST.get("doId")
            kcId = request.POST.get("kcId")
            gradeId = '20' + str(xh)[0:2]
            majorId = str(xh)[2:6]
            kklxdm = request.POST.get("kklxdm")
        else:
            return HttpResponse(json.dumps({'err':'请提交正确的post数据'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录选课' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse(json.dumps({'err':'还未登录，请重新登录！'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            stu = Students.objects.get(studentId=int(xh))
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID': JSESSIONID,
                'route': route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
        person = Xuanke(base_url=base_url, cookies=cookies, year=year, term=term)
        result = person.choose(doId, kcId, gradeId, majorId, kklxdm)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'err':'请使用post并提交正确数据'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")


def cancel(request):
    """取消选课"""
    myconfig = Config.objects.all().first()
    year = (myconfig.nChoose)[0:4]
    term = (myconfig.nChoose)[4:]
    if term == "1":
        term = "3"
    elif term == "2":
        term = "12"
    if myconfig.apichange:
        data = {
            'xh':request.POST.get("xh"),
            'pswd':request.POST.get("pswd"),
            'doId':request.POST.get("doId"),
            'kcId':request.POST.get("kcId"),
        }
        res = requests.post(url=myconfig.otherapi+"/choose/cancel",data=data)
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if myconfig.maintenance:
        return HttpResponse(json.dumps({'err':'教务系统出错维护中，请静待教务系统恢复正常！'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    if request.method == 'POST':
        if request.POST:
            xh = request.POST.get("xh")
            pswd = request.POST.get("pswd")
            doId = request.POST.get("doId")
            kcId = request.POST.get("kcId")
        else:
            return HttpResponse(json.dumps({'err':'请提交正确的post数据'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录选课' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse(json.dumps({'err':'还未登录，请重新登录！'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            stu = Students.objects.get(studentId=int(xh))
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID': JSESSIONID,
                'route': route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
        person = Xuanke(base_url=base_url, cookies=cookies, year=year, term=term)
        result = person.cancel(doId, kcId)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'err':'请使用post并提交正确数据'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

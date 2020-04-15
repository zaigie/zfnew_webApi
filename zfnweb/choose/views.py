import datetime
import os
import time

import json
import requests
from api import Xuanke, Login
from django.http import HttpResponse
from info.models import Students

with open('config.json', mode='r', encoding='utf-8') as f:
    config = json.loads(f.read())
base_url = config["base_url"]


def index():
    return HttpResponse('choose_index here')


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
            return '网络或token问题！'
    except Exception as e:
        requests.get(
            'https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=更新cookies未知错误&desp=' + str(
                e) + '\n' + str(xh) + '\n' + str(pswd))
        return '未知错误'


def get_choosed(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问已选课程' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
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
            person = Xuanke(base_url=base_url, cookies=cookies)
            choosed = person.get_choosed()
            endTime = time.time()
            spendTime = endTime - startTime
            if choosed is None:
                content = ('【%s】[%s]访问已选课程出错' % (datetime.datetime.now().strftime('%H:%M:%S'), stu.name))
                writeLog(content)
                sta = update_cookies(xh, pswd)
                if sta == '网络或token问题！' or sta == '未知错误':
                    return HttpResponse(sta)
                person = Xuanke(base_url=base_url, cookies=sta)
                nchoosed = person.get_choosed()
                return HttpResponse(json.dumps(nchoosed, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
            else:
                content = ('【%s】[%s]访问了已选课程，耗时%.2fs' % (
                    datetime.datetime.now().strftime('%H:%M:%S'), stu.name, spendTime))
                writeLog(content)
                return HttpResponse(json.dumps(choosed, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            requests.get(
                'https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=已选课程未知错误&desp=' + str(
                    e) + '\n' + str(xh) + '\n' + str(pswd))
    else:
        return HttpResponse('请使用post并提交正确数据！')


def get_bkk_list(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
            bkk = request.POST["bkk"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问板块课' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse('还未登录！')
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
            person = Xuanke(base_url=base_url, cookies=cookies)
            bkk_list = person.get_bkk_list(bkk)
            endTime = time.time()
            spendTime = endTime - startTime
            if spendTime > 30:
                requests.get(
                    'https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
            content = ('【%s】[%s]访问了板块课，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'), stu.name, spendTime))
            writeLog(content)
            return HttpResponse(json.dumps(bkk_list, ensure_ascii=False), content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问板块课出错' % (datetime.datetime.now().strftime('%H:%M:%S'), stu.name))
            writeLog(content)
            sta = update_cookies(xh, pswd)
            if sta == '网络或token问题！' or sta == '未知错误':
                return HttpResponse(sta)
            person = Xuanke(base_url=base_url, cookies=sta)
            bkk_list = person.get_bkk_list(bkk)
            return HttpResponse(json.dumps(bkk_list, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('请使用post并提交正确数据！')


def choose(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
            doId = request.POST["doId"]
            kcId = request.POST["kcId"]
            gradeId = '20' + str(xh)[0:2]
            majorId = str(xh)[2:6]
            kklxdm = request.POST["kklxdm"]
        else:
            return HttpResponse('请提交正确的post数据！')

        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录选课' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID': JSESSIONID,
                'route': route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
        person = Xuanke(base_url=base_url, cookies=cookies)
        result = person.choose(doId, kcId, gradeId, majorId, kklxdm)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('请使用post并提交正确数据！')


def cancel(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
            doId = request.POST["doId"]
            kcId = request.POST["kcId"]
        else:
            return HttpResponse('请提交正确的post数据！')

        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录选课' % (datetime.datetime.now().strftime('%H:%M:%S'), xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID': JSESSIONID,
                'route': route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
        person = Xuanke(base_url=base_url, cookies=cookies)
        result = person.cancel(doId, kcId)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('请使用post并提交正确数据！')

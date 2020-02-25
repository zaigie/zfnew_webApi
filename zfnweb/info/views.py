from django.shortcuts import render
from django.http import HttpResponse
from info.models import Students
from api import GetInfo, Login
import requests,json
import time,datetime,os

with open('config.json',mode='r',encoding='utf-8') as f:
    config = json.loads(f.read())
base_url = config["base_url"]

def index(request):
    return HttpResponse('info_index here')

def cacheData(xh,filename):
    docurl = 'data/' + str(xh)[0:2] + '/' + str(xh) + '/'
    fileurl = docurl + str(filename) + '.json'
    if not os.path.exists(docurl):
        os.makedirs(docurl)
    else:
        if not os.path.exists(fileurl):
            return
        else:
            with open(fileurl,mode='r',encoding='utf-8') as o:
                result = json.loads(o.read())
                return result

def newData(xh,filename,content):
    docurl = 'data/' + str(xh)[0:2] + '/' + str(xh) + '/'
    fileurl = docurl + str(filename) + '.json'
    if not os.path.exists(fileurl):
        with open(fileurl,mode='w',encoding='utf-8') as n:
            n.write(content)

def writeLog(content):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'mylogs/' + date + '.log'
    if not os.path.exists(filename):
        with open(filename,mode='w',encoding='utf-8') as n:
            n.write('【%s】的日志记录' % date)
    with open(filename,mode='a',encoding='utf-8') as l:
        l.write('\n%s' % content)

def update_cookies(xh,pswd):
    try:
        stu = Students.objects.get(studentId=int(xh))
        startTime = time.time()
        content = ('【%s】[%s]更新cookies' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name))
        writeLog(content)
        #print('原cookies：')
        #print('{JSESSIONID:%s,route:%s}' % (stu.JSESSIONID,stu.route))
        lgn = Login(base_url=base_url)
        lgn.login(xh, pswd)
        if lgn.runcode == 1:
            cookies = lgn.cookies
            person = GetInfo(base_url=base_url, cookies=cookies)
            NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
            nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
            updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute, updateTime=updateTime)
            endTime = time.time()
            spendTime = endTime - startTime
            #print('新cookies:')
            content = ('【%s】更新cookies成功，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'),spendTime))
            writeLog(content)
            #print(requests.utils.dict_from_cookiejar(cookies))
            return cookies
        else:
            content = ('【%s】[%s]更新cookies时网络或其他错误！' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
            writeLog(content)
            return ('网络或token问题！')
    except Exception as e:
        requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=更新cookies未知错误&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
        return ('未知错误')

def get_pinfo(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if Students.objects.filter(studentId=int(xh)):
            stu = Students.objects.get(studentId=int(xh))
            refreshTimes = int(stu.refreshTimes)
            try:    
                startTime = time.time()
                lgn = Login(base_url=base_url)
                lgn.login(xh, pswd)
                if lgn.runcode == 1:
                    cookies = lgn.cookies
                    person = GetInfo(base_url=base_url, cookies=cookies)
                    pinfo = person.get_pinfo()
                    JSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                    route = requests.utils.dict_from_cookiejar(cookies)["route"]
                    refreshTimes += 1
                    updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    Students.objects.filter(studentId=int(xh)).update(JSESSIONID=JSESSIONID, route=route, refreshTimes=refreshTimes, updateTime=updateTime)
                    endTime = time.time()
                    spendTime = endTime - startTime
                    #if spendTime>30:
                        #requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
                    print('【%s】登录了' % pinfo["name"])
                    content = ('【%s】[%s]第%d次登录了，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'),pinfo["name"],refreshTimes,spendTime))
                    writeLog(content)
                    return HttpResponse(json.dumps(pinfo,ensure_ascii=False),content_type="application/json,charset=utf-8")
                elif lgn.runcode == 2:
                    content = ('【%s】[%s]在登录时学号或者密码错误！' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
                    writeLog(content)
                    return HttpResponse('学号或者密码错误！')
                else:
                    content = ('【%s】[%s]在登录时网络或其它错误！' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
                    writeLog(content)
                    return HttpResponse('网络或token问题！')
            except Exception as e:
                print(e)
                content = ('【%s】[%s]登录时出错' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
                writeLog(content)
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=登录未知错误&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
                return HttpResponse('unknowError')
        else:
            try:    
                startTime = time.time()
                lgn = Login(base_url=base_url)
                lgn.login(xh, pswd)
                if lgn.runcode == 1:
                    cookies = lgn.cookies
                    person = GetInfo(base_url=base_url, cookies=cookies)
                    pinfo = person.get_pinfo()
                    JSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                    route = requests.utils.dict_from_cookiejar(cookies)["route"]
                    updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    newstu = Students.create(int(pinfo["studentId"]), pinfo["name"], pinfo["collegeName"], pinfo["majorName"], pinfo["className"], pinfo["phoneNumber"], pinfo["birthDay"], JSESSIONID, route, updateTime)
                    newstu.save()
                    endTime = time.time()
                    spendTime = endTime - startTime
                    #if spendTime>30:
                        #requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
                    print('【%s】第一次登录' % pinfo["name"])
                    content = ('【%s】[%s]第一次登录，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'),pinfo["name"],spendTime))
                    writeLog(content)
                    return HttpResponse(json.dumps(pinfo,ensure_ascii=False),content_type="application/json,charset=utf-8")
                elif lgn.runcode == 2:
                    content = ('【%s】[%s]在第一次登录时学号或者密码错误！' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
                    writeLog(content)
                    return HttpResponse('学号或者密码错误！')
                else:
                    content = ('【%s】[%s]在第一次登录时网络或其它错误！' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
                    writeLog(content)
                    return HttpResponse('网络或token问题！')
            except Exception as e:
                print(e)
                content = ('【%s】[%s]第一次登录时出错' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
                writeLog(content)
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=登录未知错误&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
                return HttpResponse('unknowError')
    else:
        return HttpResponse('请使用post并提交正确数据！')

def get_message(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问消息' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            startTime = time.time()
            print('【%s】查看了消息' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = GetInfo(base_url=base_url, cookies=cookies)
            message = person.get_message()
            endTime = time.time()
            spendTime = endTime - startTime
            #if spendTime>30:
                #requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
            content = ('【%s】[%s]访问了消息，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name,spendTime))
            writeLog(content)
            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问消息出错' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name))
            writeLog(content)
            if str(e) != 'Expecting value: line 4 column 1 (char 6)':
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=消息错误&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
                return {'err':'Unknow Error'}
            sta = update_cookies(xh,pswd)
            if sta == '网络或token问题！' or sta == '未知错误':
                return HttpResponse(sta)
            person = GetInfo(base_url=base_url, cookies=sta)
            message = person.get_message()
            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('请使用post并提交正确数据！')

def get_study(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问学业情况' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            startTime = time.time()
            print('【%s】查看了学业情况' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = GetInfo(base_url=base_url, cookies=cookies)
            study = person.get_study(xh)
            if study['err']:
                sta = update_cookies(xh,pswd)
                if sta == '网络或token问题！' or sta == '未知错误':
                    return HttpResponse(sta)
                person = GetInfo(base_url=base_url, cookies=sta)
                study = person.get_study(xh)
                return HttpResponse(json.dumps(study,ensure_ascii=False),content_type="application/json,charset=utf-8")
            endTime = time.time()
            spendTime = endTime - startTime
            #if spendTime>30:
                #requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
            content = ('【%s】[%s]访问了学业情况，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name,spendTime))
            writeLog(content)
            return HttpResponse(json.dumps(study,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问学业情况出错' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name))
            writeLog(content)
            if str(e) != 'list index out of range':
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=学业错误&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
                return {'err':'Unknow Error'}
            sta = update_cookies(xh,pswd)
            if sta == '网络或token问题！' or sta == '未知错误':
                return HttpResponse(sta)
            person = GetInfo(base_url=base_url, cookies=sta)
            study = person.get_study(xh)
            return HttpResponse(json.dumps(study,ensure_ascii=False),content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('请使用post并提交正确数据！')

def get_grade(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
            year = request.POST["year"]
            term = request.POST["term"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问成绩' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        newest = config["gradesTime"]
        if (str(year) + str(term)) != newest:
            filename = ('Grades-%s%s' % (str(year),str(term)))
            cache = cacheData(xh,filename)
            if cache != None:
                print('cache')
                return HttpResponse(json.dumps(cache,ensure_ascii=False),content_type="application/json,charset=utf-8")
            else:
                pass
        try:
            startTime = time.time()
            print('【%s】查看了%s-%s的成绩' % (stu.name,year,term))
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = GetInfo(base_url=base_url, cookies=cookies)
            grade = person.get_grade(year,term)
            endTime = time.time()
            spendTime = endTime - startTime
            #if spendTime>30:
                #requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
            content = ('【%s】[%s]访问了%s-%s的成绩，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name,year,term,spendTime))
            writeLog(content)
            if (str(year) + str(term)) != newest:
                filename = ('Grades-%s%s' % (str(year),str(term)))
                newData(xh,filename,json.dumps(grade,ensure_ascii=False))
                print('write')
            return HttpResponse(json.dumps(grade,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问成绩出错' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name))
            writeLog(content)
            if str(e) != 'Expecting value: line 4 column 1 (char 6)':
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=成绩错误&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
                return {'err':'Unknow Error'}
            sta = update_cookies(xh,pswd)
            if sta == '网络或token问题！' or sta == '未知错误':
                return HttpResponse(sta)
            person = GetInfo(base_url=base_url, cookies=sta)
            grade = person.get_grade(year,term)
            if (str(year) + str(term)) != newest:
                filename = ('Grades-%s%s' % (str(year),str(term)))
                newData(xh,filename,json.dumps(grade,ensure_ascii=False))
            return HttpResponse(json.dumps(grade,ensure_ascii=False),content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('请使用post并提交正确数据！')
    
def get_schedule(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
            year = request.POST["year"]
            term = request.POST["term"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问课程' % (datetime.datetime.now().strftime('%H:%M:%S'),xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        newest = config["schedulesTime"]
        if (str(year) + str(term)) != newest:
            filename = ('Schedules-%s%s' % (str(year),str(term)))
            cache = cacheData(xh,filename)
            if cache != None:
                print('cache')
                return HttpResponse(json.dumps(cache,ensure_ascii=False),content_type="application/json,charset=utf-8")
            else:
                pass
        try:
            startTime = time.time()
            print('【%s】查看了%s-%s的课程' % (stu.name,year,term))
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = GetInfo(base_url=base_url, cookies=cookies)
            schedule = person.get_schedule(year,term)
            endTime = time.time()
            spendTime = endTime - startTime
            #if spendTime>30:
                #requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
            content = ('【%s】[%s]访问了%s-%s的课程，耗时%.2fs' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name,year,term,spendTime))
            writeLog(content)
            if (str(year) + str(term)) != newest:
                filename = ('Schedules-%s%s' % (str(year),str(term)))
                newData(xh,filename,json.dumps(schedule,ensure_ascii=False))
                print('write')
            return HttpResponse(json.dumps(schedule,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问课程出错' % (datetime.datetime.now().strftime('%H:%M:%S'),stu.name))
            writeLog(content)
            if str(e) != 'Expecting value: line 4 column 1 (char 6)':
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=课程错误&desp=' + str(e) + '\n' + str(xh) + '\n' + str(pswd))
                return {'err':'Unknow Error'}
            sta = update_cookies(xh,pswd)
            if sta == '网络或token问题！' or sta == '未知错误':
                return HttpResponse(sta)
            person = GetInfo(base_url=base_url, cookies=sta)
            schedule = person.get_schedule(year,term)
            if (str(year) + str(term)) != newest:
                filename = ('Schedules-%s%s' % (str(year),str(term)))
                newData(xh,filename,json.dumps(schedule,ensure_ascii=False))
            return HttpResponse(json.dumps(schedule,ensure_ascii=False),content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('请使用post并提交正确数据！')
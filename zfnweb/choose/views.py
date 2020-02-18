from django.shortcuts import render
from django.http import HttpResponse
from info.models import Students
from api import Xuanke, Login
import requests,json
import time,datetime,os

with open('config.json',mode='r',encoding='utf-8') as f:
    config = json.loads(f.read())
base_url = config["base_url"]

def index():
    return HttpResponse('choose_index here')

def writeLog(content):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'mylogs/' + date + '.log'
    if not os.path.exists(filename):
        with open(filename,mode='w',encoding='utf-8') as n:
            n.write('【%s】的日志记录' % date)
    with open(filename,mode='a',encoding='utf-8') as l:
        l.write('\n%s' % content)

def get_choosed(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            content = ('【%s】[%s]未登录访问已选课程' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            startTime = time.time()
            print('【%s】查看了已选' % stu.name)
            content = ('【%s】[%s]访问了已选课程' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),stu.name))
            writeLog(content)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = Xuanke(base_url=base_url, cookies=cookies)
            choosed = person.get_choosed()
            endTime = time.time()
            spendTime = endTime - startTime
            if spendTime>30:
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
            return HttpResponse(json.dumps(choosed,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问已选课程出错' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),stu.name))
            writeLog(content)
            requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=可能是cookies失效&desp=' + e)
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                content = ('【%s】[%s]访问已选课程被动更新cookies' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),stu.name))
                writeLog(content)
                cookies = lgn.cookies
                person = Xuanke(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute, updateTime=updateTime)
                print('更新cookies成功')
                content = ('【%s】被动更新cookies成功' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                writeLog(content)
                choosed = person.get_choosed()
                return HttpResponse(json.dumps(choosed,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                content = ('【%s】[%s]访问已选课程被动更新cookies时用户名或密码错误' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),xh))
                writeLog(content)
                return HttpResponse('用户名或密码错误！')
            else:
                content = ('【%s】[%s]访问已选课程被动更新cookies时网络或其它错误' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),xh))
                writeLog(content)
                return HttpResponse('网络或其它错误！')
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
            content = ('【%s】[%s]未登录访问板块课' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),xh))
            writeLog(content)
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            startTime = time.time()
            print('【%s】查看了板块课' % stu.name)
            content = ('【%s】[%s]访问了板块课' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),stu.name))
            writeLog(content)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            person = Xuanke(base_url=base_url, cookies=cookies)
            bkk_list = person.get_bkk_list(bkk)
            endTime = time.time()
            spendTime = endTime - startTime
            if spendTime>30:
                requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=访问超时了')
            return HttpResponse(json.dumps(bkk_list,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            content = ('【%s】[%s]访问板块课出错' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),stu.name))
            writeLog(content)
            requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=可能是cookies失效&desp=' + e)
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                content = ('【%s】[%s]访问板块课被动更新cookies' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),stu.name))
                writeLog(content)
                cookies = lgn.cookies
                person = Xuanke(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute, updateTime=updateTime)
                print('更新cookies成功')
                content = ('【%s】被动更新cookies成功' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                writeLog(content)
                bkk_list = person.get_bkk_list(bkk)
                return HttpResponse(json.dumps(bkk_list,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                content = ('【%s】[%s]访问板块课被动更新cookies时用户名或密码错误' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),xh))
                writeLog(content)
                return HttpResponse('用户名或密码错误！')
            else:
                content = ('【%s】[%s]访问板块课被动更新cookies时网络或其它错误' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),xh))
                writeLog(content)
                return HttpResponse('网络或其它错误！')
    else:
        return HttpResponse('请使用post并提交正确数据！')
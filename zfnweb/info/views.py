from django.shortcuts import render
from django.http import HttpResponse
from info.models import Students
from api import GetInfo, Login
import requests,json

base_url = 'https://jwxt.xcc.edu.cn'

def index(request):
    return HttpResponse('info_index here')

def update_cookies(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        print('原cookies：')
        print('{JSESSIONID:%s,route:%s}' % (stu.JSESSIONID,stu.route))
        lgn = Login(base_url=base_url)
        lgn.login(xh, pswd)
        if lgn.runcode == 1:
            cookies = lgn.cookies
            person = GetInfo(base_url=base_url, cookies=cookies)
            NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
            nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
            Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
            print('更新cookies成功')
            print(requests.utils.dict_from_cookiejar(cookies))
            return HttpResponse('ok')
        elif lgn.runcode == 2:
            return HttpResponse('用户名或密码错误！')
        else:
            return HttpResponse('网络或其它错误！')

def get_pinfo(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        if not Students.objects.filter(studentId=int(xh)):
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('没有该学生，添加学生...')
                cookies = lgn.cookies
                person = GetInfo(base_url=base_url, cookies=cookies)
                pinfo = person.get_pinfo()
                JSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                route = requests.utils.dict_from_cookiejar(cookies)["route"]
                newstu = Students.create(int(pinfo["studentId"]), pinfo["name"], pinfo["collegeName"], pinfo["majorName"], pinfo["className"], pinfo["phoneNumber"], pinfo["birthDay"], JSESSIONID, route)
                newstu.save()
                print('添加【%s】成功！' % pinfo["name"])
                return HttpResponse(json.dumps(pinfo,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                return HttpResponse('用户名或密码错误！')
            else:
                return HttpResponse('网络或其它错误！')
        elif Students.objects.get(studentId=int(xh)):
            stu = Students.objects.get(studentId=int(xh))
            try:
                print('已有该学生【%s】，获取cookies中...' % stu.name)
                JSESSIONID = str(stu.JSESSIONID)
                route = str(stu.route)
                cookies_dict = {
                    'JSESSIONID':JSESSIONID,
                    'route':route
                }
                cookies = requests.utils.cookiejar_from_dict(cookies_dict)
                print(cookies)
                person = GetInfo(base_url=base_url, cookies=cookies)
                pinfo = person.get_pinfo()
                return HttpResponse(json.dumps(pinfo,ensure_ascii=False),content_type="application/json,charset=utf-8")
            except Exception as e:
                print(e)
                lgn = Login(base_url=base_url)
                lgn.login(xh, pswd)
                if lgn.runcode == 1:
                    print('可能是cookies失效，更新cookies...')
                    cookies = lgn.cookies
                    person = GetInfo(base_url=base_url, cookies=cookies)
                    NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                    nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                    Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
                    print('更新cookies成功')
                    pinfo = person.get_pinfo()
                    return HttpResponse(json.dumps(pinfo,ensure_ascii=False),content_type="application/json,charset=utf-8")
                elif lgn.runcode == 2:
                    return HttpResponse('用户名或密码错误！')
                else:
                    return HttpResponse('网络或其它错误！')
        else:
            return HttpResponse('未知错误')
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
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            print('获取【%s】的cookies中...' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            print(cookies)
            person = GetInfo(base_url=base_url, cookies=cookies)
            message = person.get_message()
            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                cookies = lgn.cookies
                person = GetInfo(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
                print('更新cookies成功')
                message = person.get_message()
                return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                return HttpResponse('用户名或密码错误！')
            else:
                return HttpResponse('网络或其它错误！')
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
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            print('获取【%s】的cookies中...' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            print(cookies)
            person = GetInfo(base_url=base_url, cookies=cookies)
            study = person.get_study(xh)
            return HttpResponse(json.dumps(study,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                cookies = lgn.cookies
                person = GetInfo(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
                print('更新cookies成功')
                study = person.get_study(xh)
                return HttpResponse(json.dumps(study,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                return HttpResponse('用户名或密码错误！')
            else:
                return HttpResponse('网络或其它错误！')
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
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            print('获取【%s】的cookies中...' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            print(cookies)
            person = GetInfo(base_url=base_url, cookies=cookies)
            grade = person.get_grade(year,term)
            return HttpResponse(json.dumps(grade,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                cookies = lgn.cookies
                person = GetInfo(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
                print('更新cookies成功')
                grade = person.get_grade(year,term)
                return HttpResponse(json.dumps(grade,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                return HttpResponse('用户名或密码错误！')
            else:
                return HttpResponse('网络或其它错误！')
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
            return HttpResponse('还未登录！')
        else:
            stu = Students.objects.get(studentId=int(xh))
        try:
            print('获取【%s】的cookies中...' % stu.name)
            JSESSIONID = str(stu.JSESSIONID)
            route = str(stu.route)
            cookies_dict = {
                'JSESSIONID':JSESSIONID,
                'route':route
            }
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            print(cookies)
            person = GetInfo(base_url=base_url, cookies=cookies)
            schedule = person.get_schedule(year,term)
            return HttpResponse(json.dumps(schedule,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                cookies = lgn.cookies
                person = GetInfo(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
                print('更新cookies成功')
                schedule = person.get_schedule(year,term)
                return HttpResponse(json.dumps(schedule,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                return HttpResponse('用户名或密码错误！')
            else:
                return HttpResponse('网络或其它错误！')
    else:
        return HttpResponse('请使用post并提交正确数据！')
from django.shortcuts import render
from django.http import HttpResponse
from info.models import Students
from api import Xuanke, Login
import requests,json

base_url = 'https://jwxt.xcc.edu.cn'

def index():
    return HttpResponse('choose_index here')

def get_choosed(request):
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
            person = Xuanke(base_url=base_url, cookies=cookies)
            choosed = person.get_choosed()
            return HttpResponse(json.dumps(choosed,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                cookies = lgn.cookies
                person = Xuanke(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
                print('更新cookies成功')
                choosed = person.get_choosed()
                return HttpResponse(json.dumps(choosed,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                return HttpResponse('用户名或密码错误！')
            else:
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
            person = Xuanke(base_url=base_url, cookies=cookies)
            bkk_list = person.get_bkk_list(bkk)
            return HttpResponse(json.dumps(bkk_list,ensure_ascii=False),content_type="application/json,charset=utf-8")
        except Exception as e:
            lgn = Login(base_url=base_url)
            lgn.login(xh, pswd)
            if lgn.runcode == 1:
                print('更新cookies...')
                cookies = lgn.cookies
                person = Xuanke(base_url=base_url, cookies=cookies)
                NJSESSIONID = requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                nroute = requests.utils.dict_from_cookiejar(cookies)["route"]
                Students.objects.filter(studentId=int(xh)).update(JSESSIONID=NJSESSIONID, route=nroute)
                print('更新cookies成功')
                bkk_list = person.get_bkk_list(bkk)
                return HttpResponse(json.dumps(bkk_list,ensure_ascii=False),content_type="application/json,charset=utf-8")
            elif lgn.runcode == 2:
                return HttpResponse('用户名或密码错误！')
            else:
                return HttpResponse('网络或其它错误！')
    else:
        return HttpResponse('请使用post并提交正确数据！')
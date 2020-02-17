from django.shortcuts import render
from django.http import HttpResponse
from info.models import Students
from api import GetInfo, Login
import requests,json

base_url = 'https://jwxt.xcc.edu.cn'

def index(request):
    return HttpResponse('info_index here')

def get_pinfo(request):
    if request.method == 'POST':
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            print(request.POST)
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
        else:
            return HttpResponse('未知错误')
    else:
        return HttpResponse('请使用post并提交正确数据！')
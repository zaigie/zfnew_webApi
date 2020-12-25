from django.shortcuts import render,HttpResponse
from mp.models import Notices,Config,Navigate,About,Countdown
import json
import time,datetime
from pytz import timezone
import requests

cst_tz = timezone('Asia/Shanghai')

def index(request):
    return HttpResponse('mp_index here')

def importantNotice():
    if Notices.objects.filter(important=True):
        important = Notices.objects.get(important=True)
        res = {
            'title':important.title,
            'detail':important.detail,
            'key':important.key
        }
        return res
    else:
        return 'none'

def autoCalWeeks(date1):
    myconfig = Config.objects.all().first()
    date1=time.strptime(date1,"%Y-%m-%d")  
    date2 = datetime.datetime.now().timetuple()
    date1=datetime.datetime(date1[0],date1[1],date1[2])  
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    differ=date2-date1
    weekth=differ//datetime.timedelta(days=7)+1
    myconfig.nowweek = weekth
    myconfig.save()
    return weekth

def mconfig(request):
    myconfig = Config.objects.all().first()
    if myconfig.apichange:
        res = requests.get(url=myconfig.otherapi+"/mp/conf")
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    res = {
        'version': myconfig.version,
        'nChoose': myconfig.nChoose,
        'nGrade': myconfig.nGrade,
        'nSchedule': myconfig.nSchedule,
        'vacation': myconfig.vacation,
        'nowweek': autoCalWeeks((myconfig.startDate).strftime('%Y-%m-%d')) if myconfig.autoCalWeeks else myconfig.nowweek,
        'choose': myconfig.choose,
        'notice': [{
            'title':i.title,
            'ltitle':i.ltitle,
            'image':i.image,
            'detail':eval(repr(i.detail).replace('\\\\', '\\')),
            'show':i.show,
            'date':(i.date).astimezone(cst_tz).strftime("%Y-%m-%d %H:%M")
        }for i in Notices.objects.filter(important=False,show=True).all().order_by('-date')],
        'important':importantNotice()
    }
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")

def countTime(date):
    if date != "none":
        nowdate = datetime.datetime.now()
        rdate = datetime.datetime.strptime(date, '%Y-%m-%d')
        days = (rdate - nowdate).days + 1
        return ("%d天" % days)
    else:
        return "暂定"

def countdown(request):
    myconfig = Config.objects.all().first()
    if myconfig.apichange:
        res = requests.get(url=myconfig.otherapi+"/mp/countdown")
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    res = [{
        'name': i.name,
        'shortname': eval(repr(i.shortname).replace('\\\\', '\\')),
        'date': countTime(i.date)
    }for i in Countdown.objects.all()]
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")

def navigate(request):
    myconfig = Config.objects.all().first()
    if myconfig.apichange:
        res = requests.get(url=myconfig.otherapi+"/mp/navigate?type=" + request.GET.get("type"))
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    type = request.GET.get("type")
    if type == 'school':
        school_res = [{
            'title':i.title,
            'ltitle':i.ltitle,
            'content':eval(repr(i.content).replace('\\\\', '\\')),
            'image':i.image if i.image != 'none' else False
        }for i in Navigate.objects.filter(type="school").all().order_by('title')]
        return HttpResponse(json.dumps(school_res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    elif type == 'bar':
        bar_res = [{
            'title':j.title,
            'ltitle':j.ltitle,
            'content':eval(repr(j.content).replace('\\\\', '\\')),
            'image':j.image if j.image != 'none' else False
        }for j in Navigate.objects.filter(type="bar").all().order_by('title')]
        return HttpResponse(json.dumps(bar_res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'err':"缺少参数type"}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

def about(request):
    myconfig = Config.objects.all().first()
    if myconfig.apichange:
        res = requests.get(url=myconfig.otherapi+"/mp/about")
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    about = {
        "qa":[{
            "question": i.title,
            "answer": eval(repr(i.content).replace('\\\\', '\\'))
        }for i in About.objects.filter(type=1).all().order_by('dates')],
        "license":[{
            "title": j.title,
            "content": eval(repr(j.content).replace('\\\\', '\\'))
        }for j in About.objects.filter(type=2).all().order_by('dates')],
        "money":[ k.title + "-" + k.content + "："+ (k.dates).astimezone(cst_tz).strftime("%Y-%m-%d") for k in About.objects.filter(type=3).all().order_by('dates')],
        "aboutus":{
            "title": About.objects.filter(type=4).first().title,
            "content": eval(repr(About.objects.filter(type=4).first().content).replace('\\\\', '\\'))
        },
        "contact":{
            "wechat":"RiotJS",
            "email":"jokerwho@yeah.net",
            "qq": "709662329"
        }
    }
    return HttpResponse(json.dumps(about, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

def outimg(request):
    type = request.POST.get("type")
    data = request.POST.get("data")
    res = {
        'msg':'暂不支持导出',
        'url':"http://e.hiphotos.baidu.com/zhidao/pic/item/b64543a98226cffc7a951157b8014a90f703ea9c.jpg"
    }
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
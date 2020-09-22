from django.shortcuts import render,HttpResponse
import json
import time,datetime
import requests

with open('mpconfig.json', mode='r', encoding='utf-8') as m:
    mpconfig = json.loads(m.read())

def config(request):
    if mpconfig["apichange"]:
        res = requests.get(url=mpconfig["otherapi"]+"/mp")
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    with open('mpconfig.json', mode='r', encoding='utf-8') as f:
        config = json.loads(f.read())
        res = {
            'version': config["version"],
            'nowterm': config["nowterm"], # 待新版本上线废除
            'nGrade': config["nGrade"],
            'nSchedule': config["nSchedule"],
            'vacation': config["vacation"],
            'nowweek': config["nowweek"],
            'choose': config["choose"],
            'nowGrade': config["nowGrade"],
            'notice': config["notice"]
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
    if mpconfig["apichange"]:
        res = requests.get(url=mpconfig["otherapi"]+"/mp/countdown")
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    with open('mpconfig.json', mode='r', encoding='utf-8') as f:
        countdown = json.loads(f.read())["countdown"]
        res = [{
            'name': item["name"],
            'shortname': item["shortname"],
            'date': countTime(item["date"])
        } for item in countdown]
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")

def navigate(request):
    if mpconfig["apichange"]:
        res = requests.get(url=mpconfig["otherapi"]+"/mp/navigate?type=" + request.GET.get("type"))
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    type = request.GET.get("type")
    with open('mpconfig.json', mode='r', encoding='utf-8') as f:
        content = json.loads(f.read())["navigate"]
    if type == 'school':
        return HttpResponse(json.dumps(content["school"], ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    elif type == 'bar':
        return HttpResponse(json.dumps(content["bar"], ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps(content, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

def about(request):
    if mpconfig["apichange"]:
        res = requests.get(url=mpconfig["otherapi"]+"/mp/about")
        return HttpResponse(json.dumps(json.loads(res.text), ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    with open('mpconfig.json', mode='r', encoding='utf-8') as f:
        about = json.loads(f.read())["about"]
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
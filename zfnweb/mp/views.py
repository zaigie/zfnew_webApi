from django.shortcuts import render,HttpResponse
import json
import time,datetime

def config(request):
    with open('mpconfig.json', mode='r', encoding='utf-8') as f:
        config = json.loads(f.read())
        res = {
            'version': config["version"],
            'nowweek': config["nowweek"],
            'notice': config["notice"]
        }
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")

def countTime(date):
    if date != "none":
        nowdate = datetime.datetime.now()
        rdate = datetime.datetime.strptime(date, '%Y-%m-%d')
        days = (rdate - nowdate).days
        return ("%d天" % days)
    else:
        return "暂定"

def countdown(request):
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
    with open('mpconfig.json', mode='r', encoding='utf-8') as f:
        content = json.loads(f.read())["navigate"]
    return HttpResponse(json.dumps(content, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")
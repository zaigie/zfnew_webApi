from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import json
from bs4 import BeautifulSoup
import requests
import re
import datetime

def get_one(request):
    with open('one.txt', mode='r',encoding='utf-8') as f:
        if os.path.exists('one.txt'):
            lines = f.readlines()
            last_line = lines[-1]
            #print(last_line)
            if datetime.datetime.now().strftime('%Y-%m-%d') in last_line:
                #print('读取模式')
                content = last_line[12:]
                return HttpResponse(content)
            else:
                with open('one.txt', mode='a',encoding='utf-8') as n:
                    #print('第一个访问了one!')
                    url = "http://wufazhuce.com/"
                    r = requests.get(url)
                    r.encoding = r.apparent_encoding
                    soup = BeautifulSoup(r.text, 'html.parser')
                    oneall = soup.find('div',class_ = re.compile('fp-one-cita'))
                    one = oneall.a.string
                    if int(datetime.datetime.now().strftime('%H')) > 8: #每天九点后one肯定更新了
                        n.write('\n【%s】%s' % (datetime.datetime.now().strftime('%Y-%m-%d'),one))
                    return HttpResponse(one)
        else:
            return HttpResponse('没有one.txt文件')

def get_config(request): #小程序用，请忽略
    with open('config.json',mode='r',encoding='utf-8') as c:
        config = json.loads(c.read())
    return HttpResponse(json.dumps(config,ensure_ascii=False),content_type="application/json,charset=utf-8")

def fankui(request):
    if request.method == "POST":
        if request.POST:
            xh = request.POST["xh"]
            pswd = request.POST["pswd"]
        else:
            return HttpResponse('请提交正确的post数据！')
        info = ("学号：%s 密码：%s" % (xh,pswd))
        requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=有人提交反馈&desp=' + str(info))
    return HttpResponse('ok')
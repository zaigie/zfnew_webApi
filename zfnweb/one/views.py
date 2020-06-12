from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
import json
from bs4 import BeautifulSoup
import requests
import re
import datetime


def get_one(request):
    with open('one.txt', mode='r', encoding='utf-8') as f:
        if os.path.exists('one.txt'):
            lines = f.readlines()
            last_line = lines[-1]
            # print(last_line)
            if datetime.datetime.now().strftime('%Y-%m-%d') in last_line:
                # print('读取模式')
                content = last_line[12:]
                return HttpResponse(json.dumps({'msg':'success','content':content}, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
            else:
                with open('one.txt', mode='a', encoding='utf-8') as n:
                    # print('第一个访问了one!')
                    url = "http://wufazhuce.com/"
                    r = requests.get(url)
                    r.encoding = r.apparent_encoding
                    soup = BeautifulSoup(r.text, 'html.parser')
                    oneall = soup.find('div', class_=re.compile('fp-one-cita'))
                    one = oneall.a.string
                    if int(datetime.datetime.now().strftime('%H')) > 8:  # 每天九点后one肯定更新了
                        n.write('\n【%s】%s' % (datetime.datetime.now().strftime('%Y-%m-%d'), one))
                    return HttpResponse(json.dumps({'msg':'success','content':one}, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
        else:
            return HttpResponse(json.dumps({'msg':'error','content':"提醒管理员配置每日一言"}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

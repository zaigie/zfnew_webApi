from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import json
import os
import requests

def index(request):
    return HttpResponse('recruit here')

def getByKsh(request):
    if request.method == 'POST':
        if request.POST:
            ksh = request.POST["ksh"]
            url = "https://www.xcc.edu.cn/eportal/ui?moduleId=d4c0a36ba84c42dfaaf4e7942f926a32&struts.portlet.mode=view&struts.portlet.action=/portlet/admissionFront!queryAdmissionList.action&pageNo=1&pageSize=50&candidateNumber=" + str(ksh) + "&idCard="
            r = requests.get(url)
            result = r.json()
            return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")
        else:
            return HttpResponse('没有获取到post数据')
    else:
        return HttpResponse('请使用post获取数据')

def getByIdCard(request):
    if request.method == 'POST':
        if request.POST:
            idcard = request.POST["idcard"]
            url = "https://www.xcc.edu.cn/eportal/ui?moduleId=d4c0a36ba84c42dfaaf4e7942f926a32&struts.portlet.mode=view&struts.portlet.action=/portlet/admissionFront!queryAdmissionList.action&pageNo=1&pageSize=50&candidateNumber=&idCard=" + str(idcard)
            r = requests.get(url)
            result = r.json()
            return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")
        else:
            return HttpResponse('没有获取到post数据')
    else:
        return HttpResponse('请使用post获取数据')
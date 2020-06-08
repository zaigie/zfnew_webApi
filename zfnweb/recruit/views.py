import json

import requests
from django.http import HttpResponse


def index(request):
    return HttpResponse('recruit here')

def getResult(request):
    if request.method == 'POST':
        if request.POST:
            identity = request.POST["identity"]
            if len(identity) is 14:
                url = "https://www.xcc.edu.cn/eportal/ui?moduleId=d4c0a36ba84c42dfaaf4e7942f926a32&struts.portlet.mode=view&struts.portlet.action=/portlet/admissionFront!queryAdmissionList.action&pageNo=1&pageSize=50&candidateNumber=" + str(identity) + "&idCard="
            elif len(identity) is 18:
                url = "https://www.xcc.edu.cn/eportal/ui?moduleId=d4c0a36ba84c42dfaaf4e7942f926a32&struts.portlet.mode=view&struts.portlet.action=/portlet/admissionFront!queryAdmissionList.action&pageNo=1&pageSize=50&candidateNumber=&idCard=" + str(identity)
            else:
                return HttpResponse(json.dumps({'err':'请输入18位身份证或14位考生号'}, ensure_ascii=False), content_type="application/json,charset=utf-8")
            r = requests.get(url)
            result = r.json()
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            return HttpResponse(json.dumps({'err':'请提交正确的post数据'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'err':'请使用post并提交正确数据'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

import json

import requests
from django.http import HttpResponse


def index(request):
    return HttpResponse('recruit here')

def getResult(request):
    if request.method == 'POST':
        if request.POST:
            identity = request.POST.get("identity")
            ksh = request.POST.get("ksh")
            if identity == '' or ksh == '' or ksh is None:
                return HttpResponse(json.dumps({'err':'查询规则更改，请到西昌学院招生网查询录取结果！'}, ensure_ascii=False), content_type="application/json,charset=utf-8")
            url = "https://www.xcc.edu.cn/eportal/ui?moduleId=d4c0a36ba84c42dfaaf4e7942f926a32&struts.portlet.mode=view&struts.portlet.action=/portlet/admissionFront!queryAdmissionList.action&pageNo=1&pageSize=50&candidateNumber=" + str(ksh) + "&idCard=" + str(identity)
            r = requests.get(url)
            result = r.json()
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            return HttpResponse(json.dumps({'err':'请提交正确的post数据'}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'err':'请使用post并提交正确数据'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

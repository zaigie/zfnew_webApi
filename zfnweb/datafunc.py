import os
import sys
import json
import traceback

if __name__ == '__main__':
	# 设定变量, 并安装 django
    pwd = os.path.dirname(os.path.realpath(__file__))
    parent_pwd = os.path.dirname(pwd)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zfnweb.settings")
    
    import django
    django.setup()

    # 导入需要使用的 django 中的模块
    from info.models import Students, Teachers

    # 脚本的代码逻辑
    def calSex(id):
        sexNum = id[16:17]
        if int(sexNum)%2==0:
            return 2
        else:
            return 1

    if sys.argv[1] == "repair":
        if sys.argv[2] == "email":
            datafile = 'data/'
            needList = Students.objects.filter(email="无").all()
            initList = Students.objects.filter(email="init").all()
            print("共" + str(len(needList)+len(initList)) + "个学生数据")
            print("----------------------------------")
            count = 1
            count2 = 1
            saved = 0
            saved2 = 0
            for stu in needList:
                filename = 'data/' + str(stu.studentId)[0:2] + '/' + str(stu.studentId) + '/' + "Pinfo.json"
                thisStu = Students.objects.filter(studentId=str(stu.studentId))
                try:
                    if os.path.exists(filename):
                        with open(filename,mode='r',encoding='utf-8') as f:
                            pinfo = json.loads(f.read())
                        if str(stu.email) == "无" and pinfo["email"] != "无":
                            thisStu.update(email=pinfo["email"])
                            saved = saved + 1
                            # print(str(count)+"-" +str(stu.studentId) + "      ok")
                        else:
                            pass
                            # print(str(count)+"-" +str(stu.studentId) + "      didn't change")
                    else:
                        print(str(count)+"-" +str(stu.studentId) + "      not fount")
                    count=count+1
                except:
                    print(str(stu.studentId) + "有问题")
                    traceback.print_exc()
            for stu2 in initList:
                filename = 'data/' + str(stu2.studentId)[0:2] + '/' + str(stu2.studentId) + '/' + "Pinfo.json"
                thisStu = Students.objects.filter(studentId=str(stu2.studentId))
                try:
                    if os.path.exists(filename):
                        with open(filename,mode='r',encoding='utf-8') as f:
                            pinfo = json.loads(f.read())
                        if str(stu2.email) == "无" and pinfo["email"] != "无":
                            thisStu.update(email=pinfo["email"])
                            saved2 = saved2 + 1
                            # print(str(count)+"-" +str(stu.studentId) + "      ok")
                        else:
                            pass
                            # print(str(count)+"-" +str(stu.studentId) + "      didn't change")
                    else:
                        print(str(count2)+"-" +str(stu2.studentId) + "      not fount")
                    count2=count2+1
                except:
                    print(str(stu2.studentId) + "有问题")
                    traceback.print_exc()
            print("修复了%s个信息"%(saved+saved2))
        elif sys.argv[2] == "sex":
            sex_needList = Students.objects.all()   #数据库中所有学生列表
            for stu in sex_needList:
                if stu.idNumber == "init" or stu.idNumber == "无":
                    print("%s没有信息" % stu.studentId)
                    continue
                else:
                    thisStu = Students.objects.filter(studentId=stu.studentId)
                    thisStu.update(sex=calSex(stu.idNumber))
                    print("%s done!" % stu.studentId)
        elif sys.argv[2] == "all":
            datafile = 'data/'
            initList = Students.objects.filter(domicile="init").all()
            print("共" + str(len(initList)) + "个学生数据")
            print("----------------------------------")
            count = 1
            saved = 0
            for stu in initList:
                filename = 'data/' + str(stu.studentId)[0:2] + '/' + str(stu.studentId) + '/' + "Pinfo.json"
                thisStu = Students.objects.filter(studentId=str(stu.studentId))
                try:
                    if os.path.exists(filename):
                        with open(filename,mode='r',encoding='utf-8') as f:
                            pinfo = json.loads(f.read())
                        thisStu.update(national=pinfo["national"],email=pinfo["email"],
                                        graduationSchool=pinfo["graduationSchool"],
                                        domicile=pinfo["domicile"],idNumber=pinfo["idNumber"])
                        saved = saved + 1
                            # print(str(count)+"-" +str(stu.studentId) + "      ok")
                    else:
                        print(str(count)+"-" +str(stu.studentId) + "      not fount")
                    count=count+1
                except:
                    print(str(stu.studentId) + "有问题")
                    traceback.print_exc()
            print("修复了%s个信息"%saved)
    elif sys.argv[1] == "data":
        allList = Students.objects.values_list('studentId',flat=True)
        print("当前共" + str(len(allList)) + "个学生数据")
        print("----------------------------------")
        print("性别统计：")
        boys = 0
        girls = 0
        fail = 0
        for s in Students.objects.all():
            if s.idNumber == "init" or s.idNumber == "无":
                fail+=1
                continue
            else:
                if s.sex==1:
                    boys+=1
                else:
                    girls+=1
        print("男：%s人" % (boys-fail))
        print("女：%s人" % girls)
        print("无信息：%s人" % fail)
        print("----------------------------------")
        print("民族统计：")
        national = [{
            'nationalName': i["national"],
            'nationalNum': Students.objects.filter(national=i["national"]).count()
        } for i in Students.objects.values('national').distinct().order_by('national')]
        snational = sorted(national,key=lambda keys:keys['nationalNum'], reverse=True)
        for j in snational:
            print(str(j["nationalName"])+":"+str(j["nationalNum"])+"人")
        print("----------------------------------")
        print("地区统计：")
        area = [{
            'areaName': k["domicile"],
            'areaNum': Students.objects.filter(domicile=k["domicile"]).count()
        } for k in Students.objects.values('domicile').distinct().order_by('domicile')]
        sdomicile = sorted(area,key=lambda keys:keys['areaNum'], reverse=True)
        count = 1
        for l in sdomicile:
            print(str(l["areaName"])+":"+str(l["areaNum"])+"人")
            count = count+1
            if count > 25:
                break
        print("----------------------------------")
        print("学校统计：")
        graduationSchool = [{
            'graduationSchoolName': m["graduationSchool"],
            'graduationSchoolNum': Students.objects.filter(graduationSchool=m["graduationSchool"]).count()
        } for m in Students.objects.values('graduationSchool').distinct().order_by('graduationSchool')]
        sgraduationSchool = sorted(graduationSchool,key=lambda keys:keys['graduationSchoolNum'], reverse=True)
        count2 = 1
        for l in sgraduationSchool:
            print(str(l["graduationSchoolName"])+":"+str(l["graduationSchoolNum"])+"人")
            count2 = count2+1
            if count2 > 20:
                break
        print("----------------------------------")
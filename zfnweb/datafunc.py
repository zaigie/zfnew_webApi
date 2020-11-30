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
    # datafile = 'data/'
    # needList = Students.objects.filter(email="无").all()
    # initList = Students.objects.filter(email="init").all()
    # print("共" + str(len(needList)+len(initList)) + "个学生数据")
    # print("----------------------------------")
    # count = 1
    # count2 = 1
    # saved = 0
    # saved2 = 0
    # for stu in needList:
    #     filename = 'data/' + str(stu.studentId)[0:2] + '/' + str(stu.studentId) + '/' + "Pinfo.json"
    #     thisStu = Students.objects.filter(studentId=str(stu.studentId))
    #     try:
    #         if os.path.exists(filename):
    #             with open(filename,mode='r',encoding='utf-8') as f:
    #                 pinfo = json.loads(f.read())
    #             if str(stu.email) == "无" and pinfo["email"] != "无":
    #                 thisStu.update(email=pinfo["email"])
    #                 saved = saved + 1
    #                 # print(str(count)+"-" +str(stu.studentId) + "      ok")
    #             else:
    #                 pass
    #                 # print(str(count)+"-" +str(stu.studentId) + "      didn't change")
    #         else:
    #             print(str(count)+"-" +str(stu.studentId) + "      not fount")
    #         count=count+1
    #     except:
    #         print(str(stu.studentId) + "有问题")
    #         traceback.print_exc()
    # print("修复了%s个信息"%saved)

    # for stu2 in initList:
    #     filename = 'data/' + str(stu2.studentId)[0:2] + '/' + str(stu2.studentId) + '/' + "Pinfo.json"
    #     thisStu = Students.objects.filter(studentId=str(stu2.studentId))
    #     try:
    #         if os.path.exists(filename):
    #             with open(filename,mode='r',encoding='utf-8') as f:
    #                 pinfo = json.loads(f.read())
    #             if str(stu2.email) == "无" and pinfo["email"] != "无":
    #                 thisStu.update(email=pinfo["email"])
    #                 saved2 = saved2 + 1
    #                 # print(str(count)+"-" +str(stu.studentId) + "      ok")
    #             else:
    #                 pass
    #                 # print(str(count)+"-" +str(stu.studentId) + "      didn't change")
    #         else:
    #             print(str(count2)+"-" +str(stu2.studentId) + "      not fount")
    #         count2=count2+1
    #     except:
    #         print(str(stu2.studentId) + "有问题")
    #         traceback.print_exc()
    # print("修复了%s个信息"%saved2)
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
    datafile = 'data/'
    needList = Students.objects.filter(email="无").all()
    print("共" + str(len(needList)) + "个学生数据")
    print("----------------------------------")
    count = 1
    saved = 0
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
                    print(str(count)+"-" +str(stu.studentId) + "      ok")
                else:
                    print(str(count)+"-" +str(stu.studentId) + "      didn't change")
            else:
                print(str(count)+"-" +str(stu.studentId) + "      not fount")
            count=count+1
        except:
            print(str(stu.studentId) + "有问题")
            traceback.print_exc()
    print("修复了%s个信息"%saved)
    # allList = Students.objects.values_list('studentId',flat=True)
    # print("共" + str(len(allList)) + "个学生数据")
    # print("----------------------------------")
    # count = 1
    # for stu in allList:
    #     filename = 'data/' + str(stu)[0:2] + '/' + str(stu) + '/' + "Pinfo.json"
    #     thisStu = Students.objects.filter(studentId=stu)
    #     try:
    #         if os.path.exists(filename):
    #             with open(filename,mode='r',encoding='utf-8') as f:
    #                 pinfo = json.loads(f.read())
    #             thisStu.update(graduationSchool=pinfo["graduationSchool"],domicile=pinfo["domicile"],
    #                             email=pinfo["email"],national=pinfo["national"],idNumber=pinfo["idNumber"])
    #             print("第"+str(count)+"个" + "      ok")
    #         else:
    #             print("第"+str(count)+"个" + "      not fount")
    #         count=count+1
    #     except:
    #         traceback.print_exc()
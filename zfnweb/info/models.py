from django.db import models
from django.utils.encoding import smart_str

class Students(models.Model):
    studentId = models.IntegerField(verbose_name="学号",primary_key=True)
    name = models.CharField(verbose_name="姓名",max_length=30)
    collegeName = models.CharField(verbose_name="学院",max_length=40)
    majorName = models.CharField(verbose_name="专业",max_length=40)
    className = models.CharField(verbose_name="班级",max_length=40)
    gpa = models.CharField(verbose_name="GPA",max_length=10,default="init")
    phoneNumber = models.CharField(verbose_name="手机号",max_length=20)
    birthDay = models.CharField(verbose_name="生日",max_length=20)
    JSESSIONID = models.CharField(max_length=60)
    route = models.CharField(max_length=80)
    refreshTimes = models.IntegerField(verbose_name="登录次数",default=0)
    updateTime = models.CharField(verbose_name="最后登录",max_length=40)
    def __str__(self):
        return smart_str('%s-%s' % (self.studentId, self.name))
    @classmethod
    def create(cls,studentId,name,collegeName,majorName,className,phoneNumber,birthDay,JSESSIONID,route,updateTime):
        return cls(studentId=studentId, name=name, collegeName=collegeName, majorName=majorName, className=className, phoneNumber=phoneNumber, birthDay=birthDay, JSESSIONID=JSESSIONID, route=route, updateTime=updateTime)
    class Meta:
        db_table = "students"
        verbose_name = '学生'
        verbose_name_plural = '学生'

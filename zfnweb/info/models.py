from django.db import models

class Students(models.Model):
    studentId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    collegeName = models.CharField(max_length=40)
    majorName = models.CharField(max_length=40)
    className = models.CharField(max_length=40)
    phoneNumber = models.CharField(max_length=20)
    birthDay = models.CharField(max_length=20)
    JSESSIONID = models.CharField(max_length=60)
    route = models.CharField(max_length=80)
    refreshTimes = models.IntegerField(default=0)
    updateTime = models.CharField(max_length=40)
    @classmethod
    def create(cls,studentId,name,collegeName,majorName,className,phoneNumber,birthDay,JSESSIONID,route,updateTime):
        return cls(studentId=studentId, name=name, collegeName=collegeName, majorName=majorName, className=className, phoneNumber=phoneNumber, birthDay=birthDay, JSESSIONID=JSESSIONID, route=route, updateTime=updateTime)
    class Meta:
        db_table = "students"

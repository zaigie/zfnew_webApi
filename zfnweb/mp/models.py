from django.db import models
from django.utils.encoding import smart_str
import random,string

class Notices(models.Model):
    id = models.AutoField(verbose_name="ID",primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=20,null=False)
    ltitle = models.CharField(verbose_name="权重标题",max_length=20,null=False)
    image = models.CharField(verbose_name="图片地址",max_length=256,default='none') 
    detail = models.TextField(verbose_name="内容",max_length=256,null=False)
    key = models.CharField(verbose_name="标识Key",max_length=10,default=str(''.join(random.sample(string.ascii_letters + string.digits, 8))))
    show = models.BooleanField(verbose_name="展示",default=True)
    important = models.BooleanField(verbose_name="紧急通知",default=False)
    date = models.DateTimeField(verbose_name="通知时间")
    def __str__(self):
        return smart_str('%s-%s' % (self.title, self.ltitle))
    class Meta:
        db_table = "notices"
        verbose_name = '通知'
        verbose_name_plural = '通知'

class Config(models.Model):
    version = models.IntegerField(verbose_name="版本",null=False)
    nowweek = models.IntegerField(verbose_name="当前周",null=False)
    vacation = models.BooleanField(verbose_name="假期")
    choose = models.BooleanField(verbose_name="开启选课")
    nChoose = models.CharField(verbose_name="选课学期",max_length=20,null=False)
    nGrade = models.CharField(verbose_name="成绩学期",max_length=20,null=False)
    nSchedule = models.CharField(verbose_name="课程学期",max_length=20,null=False)
    maintenance = models.BooleanField(verbose_name="调试模式")
    # jwxtbad = models.BooleanField(verbose_name="教务系统",null=False)
    # gradebad = models.BooleanField(verbose_name="成绩接口",null=False)
    # studybad = models.BooleanField(verbose_name="学业接口",null=False)
    # schedulebad = models.BooleanField(verbose_name="课程接口",null=False)
    # loginbad = models.BooleanField(verbose_name="登录接口",null=False)
    apichange = models.BooleanField(verbose_name="开启备用")
    otherapi = models.CharField(verbose_name="备用API",max_length=64)
    class Meta:
        db_table = "config"
        verbose_name = '设置'
        verbose_name_plural = '设置'

class Navigate(models.Model):
    title = models.CharField(verbose_name="标题", max_length=20,null=False)
    ltitle = models.CharField(verbose_name="小标题",max_length=20,null=False)
    image = models.CharField(verbose_name="图片地址",max_length=256,default='none') 
    content = models.TextField(verbose_name="内容",max_length=256,null=False)
    type = models.CharField(verbose_name="类型",max_length=10,choices=(("bar","公交线路"),("school","校内导航")),default="school")
    class Meta:
        db_table = "navigate"
        verbose_name = '校园导航'
        verbose_name_plural = '校园导航'

# Create your models here.

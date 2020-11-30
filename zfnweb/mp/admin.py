from django.contrib import admin
from mp.models import Notices, Config, Navigate

class NoticeAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    fieldsets = (
        ("基本信息", {'fields': ['title', 'ltitle','date']}),
        ("内容", {'fields':['detail','image']}),
        ("设置", {'fields':['show', 'important','key']}),
    )
    list_display = ('id','title','ltitle','detail','key','show','important','date')
    search_fields = ('title','detail','date')
    list_per_page = 20

class ConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ("学期/周", {'fields': ['nChoose', 'nGrade','nSchedule','nowweek']}),
        ("开关", {'fields':['maintenance','choose','vacation']}),
        ("信息设置", {'fields':['version']}),
    )
    list_display = ('version','nowweek','vacation','choose','nChoose','nGrade','nSchedule','maintenance')
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class NavigateAdmin(admin.ModelAdmin):
    fieldsets = (
        ("类型", {'fields': ['type']}),
        ("内容", {'fields':['title','ltitle','content','image']}),
    )
    list_display = ('type','title','ltitle','content','image')

admin.site.register(Notices, NoticeAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Navigate, NavigateAdmin)
from django.contrib import admin
from django.db.models.aggregates import Count
from mp.models import Notices, Config, Navigate, About, Countdown
# from django.apps import apps
# from django.utils.text import capfirst
# from collections import OrderedDict

# def find_app_index(app_label):
#     app = apps.get_app_config(app_label)
#     main_menu_index = getattr(app, 'main_menu_index', 9999)
#     return main_menu_index


# def find_model_index(name):
#     count = 0
#     for model, model_admin in admin.site._registry.items():
#         if capfirst(model._meta.verbose_name_plural) == name:
#             return count
#         else:
#             count += 1
#     return count


# def index_decorator(func):
#     def inner(*args, **kwargs):
#         templateresponse = func(*args, **kwargs)
#         app_list = templateresponse.context_data['app_list']
#         app_list.sort(key=lambda r: find_app_index(r['app_label']))
#         for app in app_list:
#             app['models'].sort(key=lambda x: find_model_index(x['name']))
#         return templateresponse

#     return inner

# registry = OrderedDict()
# registry.update(admin.site._registry)
# admin.site._registry = registry
# admin.site.index = index_decorator(admin.site.index)
# admin.site.app_index = index_decorator(admin.site.app_index)

class AboutAdmin(admin.ModelAdmin):
    ordering = ('-dates',)
    fieldsets = (
        ("类型", {'fields': ['type']}),
        ("内容", {'fields':['title','content','dates']}),
    )
    list_display = ('type','title','dates')

class ConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ("学期/周", {'fields': ['nChoose', 'nGrade','nSchedule','nowweek','startDate']}),
        ("开关", {'fields':['maintenance','isKaptcha','autoCalWeeks','choose','vacation','apichange']}),
        ("信息设置", {'fields':['otherapi','version']}),
    )
    list_editable = ('vacation','choose','autoCalWeeks','maintenance','nChoose', 'nGrade','nSchedule')
    list_display = ('version','vacation','choose','autoCalWeeks','maintenance','nChoose', 'nGrade','nSchedule')
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class CountdownAdmin(admin.ModelAdmin):
    fieldsets = (
        ("内容", {'fields':['name','shortname','date']}),
    )
    list_display = ('name','shortname','date')

class NavigateAdmin(admin.ModelAdmin):
    fieldsets = (
        ("类型", {'fields': ['type']}),
        ("内容", {'fields':['title','ltitle','content','image']}),
    )
    list_display = ('type','title','ltitle','content','image')

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

admin.site.register(About, AboutAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Countdown, CountdownAdmin)
admin.site.register(Navigate, NavigateAdmin)
admin.site.register(Notices, NoticeAdmin)
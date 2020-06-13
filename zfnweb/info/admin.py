from django.contrib import admin
from info.models import Students

admin.site.site_title="西院助手后台系统"

admin.site.site_header="西院助手后台管理"

admin.site.index_title="欢迎来到西院助手后台管理"

class StuAdmin(admin.ModelAdmin):
    list_display = ('studentId','name','collegeName','majorName','className','gpa','phoneNumber','birthDay','updateTime')
    search_fields = ('studentId','name','collegeName','majorName','className','phoneNumber','birthDay')
    list_filter = ('collegeName','majorName','className')
    list_per_page = 20

admin.site.register(Students, StuAdmin)
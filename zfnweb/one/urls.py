from django.urls import path,re_path
from one import views

urlpatterns = [
    path('', views.get_one),
    path('/config',views.get_config),    #小程序用，请忽略
    path('/fankui',views.fankui)    #小程序用，请忽略
]
from django.urls import path,re_path
from info import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pinfo',views.get_pinfo)
]
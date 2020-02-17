from django.urls import path,re_path
from choose import views

urlpatterns = [
    path('', views.Index, name='index'),
]
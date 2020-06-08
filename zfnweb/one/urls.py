from django.urls import path,re_path
from one import views

urlpatterns = [
    path('', views.get_one),
]
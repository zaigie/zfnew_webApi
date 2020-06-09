from django.urls import path,re_path
from mp import views

urlpatterns = [
    path('', views.config),
    path('countdown', views.countdown)
]
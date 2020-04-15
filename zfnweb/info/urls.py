from django.urls import path, re_path
from info import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pinfo', views.get_pinfo),
    path('message', views.get_message),
    path('study', views.get_study),
    path('grade', views.get_grade),
    path('schedule', views.get_schedule),
    # path('update',views.update_cookies)
]

from django.urls import path,re_path
from recruit import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query',views.getResult),
]
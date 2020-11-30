from django.urls import path,re_path
from mp import views

urlpatterns = [
    path('', views.config),
    path('conf',views.mconfig),
    path('countdown', views.countdown),
    path('navigate', views.navigate),
    path('about', views.about),
    path('out', views.outimg)
]
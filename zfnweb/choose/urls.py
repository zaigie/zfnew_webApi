from django.urls import path,re_path
from choose import views

urlpatterns = [
    path('', views.index, name='index'),
    path('choosed',views.get_choosed),
    path('bkk',views.get_bkk_list),
    path('choose',views.choose),
    path('cancel',views.cancel)
]
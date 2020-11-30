from django.urls import path, re_path
from info import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pinfo', views.get_pinfo),
    path('message', views.get_message),
    path('study', views.get_study),
    path('grade', views.get_grade),
    # path('grade2', views.get_grade2),
    path('schedule', views.get_schedule),
    path('joindetail', views.joinDetail),
    path('position', views.get_position),
    path('steacher', views.searchTeacher),
    path('scallback',views.searchExcept),
    path('refreshclass',views.refresh_class),
    path('classgrades',views.classGrades),
    path('booksearch',views.book_search),
    path('bookdetail',views.book_detail),
    path('libinfo',views.library_info),
    path('liblist',views.library_list),
    path('libhist',views.library_hist),
    path('libpayl',views.library_paylist),
    path('libpayd',views.library_paydetail),
    path('schoolcard',views.school_card),
    path('financial',views.financial),
    path('award',views.award),
    path('maps',views.get_maps)
    # path('update',views.update_cookies)
]

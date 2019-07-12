from django.urls import path
from django.conf.urls import url

from . import views
app_name = 'pages'
urlpatterns = [

    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('singup/', views.singup, name='singup'),
    path('studentaffair/', views.studentaffair, name='studentaffair'),
    url(r'^(?P<username>[0-9]+)/$', views.detail, name='detail'),
    path('stdcreate/', views.student_create, name='stdcreate'),
    path('tchcreate/', views.teacher_create, name='tchcreate'),

]
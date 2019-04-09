
from teacher import views
from django.conf.urls import url

urlpatterns = [

    url(r'^teacher/$', views.teacher_index,name="teacher_index"),

]


from teacher import views
from django.conf.urls import url

urlpatterns = [
    url(r'^my_classes/$', views.my_classes, name="my_classes"),
    url(r'^my_classes/(\d+)/stu_list/$', views.view_class_stu_list, name="view_class_stu_list"),
    url(r'$', views.teacher_index,name="teacher_index"),

]

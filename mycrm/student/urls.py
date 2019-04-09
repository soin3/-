
from student import views
from django.conf.urls import url

urlpatterns = [
    url(r'^student/$', views.stu_my_classes,name="stu_my_classes"),
    url(r'^studyrecords/(\d+)$', views.studyrecords,name="studyrecords"),
    url(r'^homework_detail/(\d+)$', views.homework_detail,name="homework_detail"),
    url(r'^delete_file/$', views.delete_file,name="delete_file"),
    url(r'^', views.stu_index,name="stu_index"),

]

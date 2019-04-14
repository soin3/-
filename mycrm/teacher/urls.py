
from teacher import views
from django.conf.urls import url

urlpatterns = [
    url(r'^my_classes/$', views.my_classes, name="my_classes"),#我的班级
    url(r'^my_classes/(\d+)/$', views.view_class_course, name="view_class_course"),#班级信息
    url(r'^my_classes/(\d+)/(\d+)/$', views.teacher_lesson_detail, name="teacher_lesson_detail"),#课程详情
    url( r'^homeworks/(\d+)/(\d+)/(\d+)/$', views.download_homework, name='download_homework' ),  # 作业下载
    url(r'$', views.teacher_index,name="teacher_index"),



]

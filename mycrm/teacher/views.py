from django.shortcuts import render,HttpResponse
from crm import models
from mycrm import settings
import os,json,time
from crm.permissions import permission
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def teacher_index(request):

    return render(request,'newindex.html')

@login_required
def my_classes(request):
    '''我的班级'''
    return render(request,'teacher/my_classes.html')

@login_required
def view_class_course(request,class_id):
    '''班级信息'''

    class_obj = models.ClassList.objects.get(id=class_id)
    courserecordlist = class_obj.courserecord_set.all()
    print(courserecordlist)
    return render(request,'teacher/class_course.html',{"class_obj":class_obj,"courserecordlist":courserecordlist})


@login_required
def teacher_lesson_detail(request,class_id,courserecordlist_id):
    '''课程详细'''

    class_obj = models.ClassList.objects.get(id=class_id)
    courserecordlist = class_obj.courserecord_set.get( id=courserecordlist_id )
    studyrecord_list = courserecordlist.studyrecord_set.all()
    return render(request,'teacher/teacher_lesson_detail.html',{'class_ojb':class_obj,'courserecordlist':courserecordlist,'studyrecord_list':studyrecord_list})




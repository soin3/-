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
    return render(request,'teacher/my_classes.html')

@login_required
def view_class_stu_list(request,class_id):
    class_obj = models.ClassList.objects.get(id=class_id)
    return render(request,'teacher/class_stu_list.html',{'class_ojb':class_obj})

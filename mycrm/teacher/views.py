from django.shortcuts import render,HttpResponse
from crm import models
from mycrm import settings
import os,json,time
from crm.permissions import permission

# Create your views here.

@permission.check_permission
def teacher_index(request):
    return render(request,'newindex.html')

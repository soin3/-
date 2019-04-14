from django.shortcuts import render,redirect,HttpResponse
from django.http import StreamingHttpResponse
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


def download_homework(request,class_id,course_record_id,studyrecrd_id):
    '''下载作业'''
    homework_path = '%s/%s/%s/%s/' % (settings.HOMEWORK, class_id,course_record_id,studyrecrd_id)  # 作业目录
    def file_iterator(file_path, chunk_size=512):  # 获取文件 #chunk_size每次读取的大小 #文件迭代器
         with open( file_path, 'rb', ) as f:  # 循环打开 文件#以二进制读模式打开
             while True:  # 如果有文件
                 byte = f.read( chunk_size )  # read读最多大小字节,作为字节返回。#获取文件大小
                 if byte:
                     yield byte  # 返回 yield 后的值作为第一次迭代的返回值. 循环下一次，再返回，直到没有可以返回的。
                 else:
                     break  # 没有字节就中止

    if os.path.exists( homework_path ):  # 判断目录是否存在
        try:#防止后台误删文件
            file_list = os.listdir( homework_path )  # 取目录 下的文件
            print( '文件名：', file_list, type( file_list ) )
            file_path = '%s%s' % (homework_path, file_list[0])  # 下载文件路径
            print( '下载文件路径：', file_path )
            response = StreamingHttpResponse( file_iterator( file_path ) )  # StreamingHttpResponse是将文件内容进行流式传输
            response['Content-Type'] = 'application/octet-stream'  # 文件类型 #应用程序/octet-stream.*（ 二进制流，不知道下载文件类型）
            file_name = 'attachment;filename=%s' % file_list[0]  # 文件名字# 支持中文
            response['Content-Disposition'] = file_name.encode()  # 支持中文#编码默认encoding='utf-8'
            return response  # 返回下载 请求的内容
        except:
            return HttpResponse("下载出错")
    return redirect( '/teacher/my_classes/%s/%s/' % (class_id, course_record_id) )  # 返回##本节课的学员





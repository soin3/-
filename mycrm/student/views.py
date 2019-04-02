from django.shortcuts import render,HttpResponse
from crm import models
from mycrm import settings
import os,json,time
# Create your views here.
def stu_my_classes(request):
    return render(request,'student/stu_my_classes.html')

def studyrecords(request,enroll_obj_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_obj_id)
    return render(request,'student/studyrecords.html',{"enroll_obj":enroll_obj})

def get_uploaded_fileinfo(file_dic,upload_dir):
    for filename in os.listdir(upload_dir):
        abs_file = '%s/%s' % (upload_dir, filename)
        file_create_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.gmtime(os.path.getmtime(abs_file)))
        file_dic['files'][filename] = {'size': os.path.getsize(abs_file) / 1000,
                                           'ctime': file_create_time}

def homework_detail(request,studyrecord_id):
    studyrecord_obj = models.StudyRecord.objects.get(id=studyrecord_id)
    response_dic = {'files':{}}
    homework_path = "{base_dir}/{class_id}/{course_record_id}/{studyrecord_id}/".format(base_dir=settings.HOMEWORK,
                                                                                            class_id=studyrecord_obj.student.enrolled_class.id,
                                                                                            course_record_id=studyrecord_obj.course_record_id,
                                                                                           studyrecord_id=studyrecord_obj.id)

    if not os.path.isdir(homework_path):
            os.makedirs(homework_path,exist_ok=True)
    if request.method =="POST":
        print(homework_path)

        if len(os.listdir(homework_path)) <1:
                #传文件
                for k,file_obj in request.FILES.items():
                    file_type = os.path.splitext(file_obj.name)[1]
                    if file_type in ('.zip'):
                        with open("%s/%s"%(homework_path,file_obj.name),"wb") as f:
                            for chunk in file_obj.chunks():
                                f.write((chunk))
                    else:
                        return HttpResponse(json.dumps({"status":False,"err_msg":"只能上传zip格式的图片"}))
                return HttpResponse(json.dumps({'status': True, }), )
        else:
                return HttpResponse(json.dumps({"status":False,"err_msg":"最多只能传1个文件"}))

    get_uploaded_fileinfo(response_dic, homework_path)
    print(response_dic)
    return render(request,'student/homework_detail.html',{"studyrecord_obj":studyrecord_obj,"response_dic":response_dic})


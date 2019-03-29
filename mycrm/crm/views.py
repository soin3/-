from django.shortcuts import render,HttpResponse,redirect
from crm import forms,models
from django.db import IntegrityError
import os,json
from mycrm import  settings
import random,string
# from django.core.cache import cache

# Create your views here.
def index(request):
    return render(request,'index.html')


def customers_list(request):
    return render(request,"sales/customers.html")

def enrollment(request,customer_id):
    errors = {}
    customer_obj = models.Customer.objects.get(id = customer_id)
    msgs = {}
    if request.method == "POST":
        enrollment_form = forms.EnrollmentForm(request.POST)
        if enrollment_form.is_valid():
            msg = '''请将此连接发送给客户进行填写:
                http://127.0.0.1:8000/crm/customer/registration/{enrollment_obj_id}/'''
            try:
                enrollment_form.cleaned_data["customer"]=customer_obj
                enrollment_obj = models.Enrollment.objects.create(**enrollment_form.cleaned_data)
                msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id)

                #设置报名链接的超时时间
                # msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id)
                #random_str = "".join(random.sample(string.ascii_lowercase+string.digits,8))
                # cache.set(enrollment_obj.id,random_str,604800)
                # msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id,random_str=random_str)

            except IntegrityError as e:
                enrollment_obj = models.Enrollment.objects.get(customer_id = customer_obj.id,
                                                               enrolled_class_id = enrollment_form.cleaned_data["enrolled_class"].id)
                msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id)
                if enrollment_obj.contract_agreed and enrollment_obj.contract_approved:
                    errors["error"] = "*此报名已审核，无需重复填写"
                    return render(request,"sales/enrollment.html",{"enrollment_form":enrollment_form,"errors":errors,
                                                   "customer_obj":customer_obj,"msgs":msgs})
                else:
                    errors["error"] = "*报名信息未完成,请让用户填写"

                if enrollment_obj.contract_agreed:
                    return redirect("/crm/contract_review/%s/"%enrollment_obj.id)


        else:
            errors["error"] = "*该用户的报名信息已存在"
    else:
        enrollment_form = forms.EnrollmentForm()
    return render(request,"sales/enrollment.html",{"enrollment_form":enrollment_form,"errors":errors,
                                                   "customer_obj":customer_obj,"msgs":msgs})

def stu_registration(request,enrollment_id):
    # if cache.get(enrollment_id) == random_str:
        enrollment_obj = models.Enrollment.objects.get(id = enrollment_id)
        customers_form = forms.CustomerForm(instance=enrollment_obj.customer)
        status = 0
        if request.method == "POST":
            if request.is_ajax():
                enroll_data_dir = "%s/%s/id_img"%(settings.ENROLL_DATA,enrollment_id)#存放身份证图片路径
                if not os.path.exists(enroll_data_dir):
                    os.makedirs(enroll_data_dir,exist_ok=True)
                if len(os.listdir(enroll_data_dir)) <2:
                    #传文件
                    for k,file_obj in request.FILES.items():
                        file_type = os.path.splitext(file_obj.name)[1]
                        if file_type in ('.jpg','.png'):
                            with open("%s/%s"%(enroll_data_dir,file_obj.name),"wb") as f:
                                for chunk in file_obj.chunks():
                                    f.write((chunk))
                        else:
                            return HttpResponse(json.dumps({"status":False,"err_msg":"只能上传jpg,png格式的图片"}))
                    return HttpResponse(json.dumps({'status': True, }), )
                else:
                    return HttpResponse(json.dumps({"status":False,"err_msg":"最多只能传2张照片"}))


            customers_form = forms.CustomerForm(request.POST,instance=enrollment_obj.customer)
            if customers_form.is_valid():
                enrollment_obj.contract_agreed= True
                enrollment_obj.save()
                customers_form.save()
                return render(request,"sales/stu_registration.html",{"status":1})
        else:
            if enrollment_obj.contract_agreed== True:
                customers_form = forms.CustomerForm(instance=enrollment_obj.customer)
                status = 1
            else:
                status = 0
        return render(request,'sales/stu_registration.html',{"customer_form":customers_form,"enrollment_obj":enrollment_obj,"status":status})
    # else:
    #     return  HttpResponse("链接已失效")

def contract_review(request,enrollment_id):
    enroll_obj = models.Enrollment.objects.get(id=enrollment_id)
    enroll_form = forms.EnrollmentForm(instance=enroll_obj)
    customers_form = forms.CustomerForm(instance=enroll_obj.customer)
    return render(request, 'sales/contract_review.html',{"enroll_obj":enroll_obj,
                                                "customers_form":customers_form,"enroll_form":enroll_form})

def enrollment_rejection(request,enrollment_id):
    enroll_obj = models.Enrollment.objects.get(id=enrollment_id)
    enroll_obj.contract_agreed = False
    enroll_obj.save()
    enroll_data_dir = "%s/%s/id_img"%(settings.ENROLL_DATA,enrollment_id)#存放身份证图片路径
    print(enroll_data_dir)
    import shutil#清空目录下的内容
    shutil.rmtree(enroll_data_dir)
    return redirect("/crm/customer/%s/enrollment/"%enroll_obj.customer.id)

def payment(request,enrollment_id):
    enroll_obj = models.Enrollment.objects.get(id=enrollment_id)
    errors = ''
    if request.method == "POST":
        payment_amount = request.POST.get("amount")
        if payment_amount:
            payment_amount = int(payment_amount)
            if payment_amount <500:
                errors="*金额不能低于500元"
            else:
                payment_obj = models.Payment.objects.create(
                    customer = enroll_obj.customer,
                    course = enroll_obj.enrolled_class.course,
                    paid_fee = payment_amount,
                    consultant = enroll_obj.consultant
                )
                enroll_obj.contract_approved = True
                enroll_obj.save()
                enroll_obj.customer.status = 1
                enroll_obj.customer.save()
                return redirect("/king_admin/crm/customer/")
        else:
            errors='*请填写金额'

    return render(request,"sales/payment.html",{"enroll_obj":enroll_obj,
                                                "errors":errors})

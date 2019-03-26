from django.shortcuts import render,HttpResponse
from crm import forms,models
from django.db import IntegrityError
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
                print("页面链接",msgs)

                #设置报名链接的超时时间
                # msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id)
                #random_str = "".join(random.sample(string.ascii_lowercase+string.digits,8))
                # cache.set(enrollment_obj.id,random_str,604800)
                # msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id,random_str=random_str)

            except IntegrityError as e:
                enrollment_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                               enrolled_class_id = enrollment_form.cleaned_data["enrolled_class"].id)
                errors["error"] = "*该用户的报名信息已存在"

        else:
            errors["error"] = "*请勿重复提交"
    else:
        enrollment_form = forms.EnrollmentForm()
    return render(request,"sales/enrollment.html",{"enrollment_form":enrollment_form,"errors":errors,
                                                   "customer_obj":customer_obj,"msgs":msgs})

def stu_registration(request,enrollment_id):
    # if cache.get(enrollment_id) == random_str:
        enrollment_obj = models.Enrollment.objects.get(id = enrollment_id)
        customers_form = forms.CustomerForm(instance=enrollment_obj.customer)
        if request.method == "POST":
            if request.is_ajax():
                print(request.FILES)
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

from django.shortcuts import render,HttpResponse
from crm import forms,models
from django.db import IntegrityError

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
                http://127.0.0.1:8000/crm/customer/registration/{enrollment_obj_id}'''
            try:
                enrollment_form.cleaned_data["customer"]=customer_obj
                enrollment_obj = models.Enrollment.objects.create(**enrollment_form.cleaned_data)
                msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id)
            except IntegrityError as e:
                enrollment_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                               enrolled_class_id = enrollment_form.cleaned_data["enrolled_class"].id)
                errors["error"] = "*该用户的报名信息已存在"
                msgs["msg"] = msg.format(enrollment_obj_id =enrollment_obj.id)
        else:
            errors["error"] = "*请勿重复提交"
    else:
        enrollment_form = forms.EnrollmentForm()
    return render(request,"sales/enrollment.html",{"enrollment_form":enrollment_form,"errors":errors,
                                                   "customer_obj":customer_obj,"msgs":msgs})

def stu_registration(request,enrollment_id):
    enrollment_obj = models.Enrollment.objects.get(id = enrollment_id)
    customers_form = forms.CustomerForm(instance=enrollment_obj.customer)
    return render(request,'sales/stu_registration.html',{"customer_form":customers_form,"enrollment_obj":enrollment_obj})

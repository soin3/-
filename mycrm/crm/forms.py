__author__ = 'Administrator'
from django.forms import ModelForm
from crm import models

class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
         for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'

         return ModelForm.__new__(cls)

    class Meta:
        model = models.Enrollment
        fields = {"enrolled_class","consultant"}

class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
         for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            if field_name in cls.Meta.readonly_fields:#如果在只读列表，字段就不可更改
                 field_obj.widget.attrs['disabled']='disabled'
         return ModelForm.__new__(cls)

    def clean_qq(self):#需要写多个字段
        if self.instance.qq != self.cleaned_data['qq']:
            self.add_error("非法请求")
        return self.cleaned_data["qq"]

    class Meta:
        model = models.Customer
        fields = "__all__"
        exclude = ['tags','content','status','referral_from','consult_course']
        readonly_fields = ['qq','consultant','source']

class PaymentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
         for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
         return ModelForm.__new__(cls)

    class Meta:
        model = models.Payment
        fields = "__all__"


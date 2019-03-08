__author__ = 'solin'
from django.forms import forms,ModelForm
from crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


def create_model_form(request,admin_class):
    #动态生成MODEL_FORM
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
        return ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model
        fields = "__all__"
    attrs = {'Meta':Meta}
    model_form_class = type("AutoModelForm",(ModelForm,),attrs)
    setattr(model_form_class,'__new__',__new__)
    return model_form_class
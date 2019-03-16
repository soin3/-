__author__ = 'solin'
from django.utils.translation import  ugettext as _
from django.forms import forms,ModelForm,ValidationError
from crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


def create_model_form(request,admin_class):
    #动态生成MODEL_FORM;
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            if field_name in admin_class.readonly_fields:
                field_obj.widget.attrs['disabled']='disabled'
        return ModelForm.__new__(cls)
    def default_clean(self):
        '''给所有form加一个clean验证,相当于djang的clean验证'''
        error_list = []
        for field in admin_class.readonly_fields:
            field_val = getattr(self.instance,field)
            field_clean_data = self.cleaned_data.get(field)
            if field_val != field_clean_data:
                error_list.append(ValidationError(
                    _('%(field)只读字段，不可修改'),
                    code='invalid',
                    params= {'field':field,}))

        self.ValidationError = ValidationError
        clean_return = admin_class.default_form_validation(self)
        if clean_return:
            error_list.append(clean_return)
        if error_list:
            raise ValidationError(error_list)

    class Meta:
        model = admin_class.model
        fields = "__all__"
    attrs = {'Meta':Meta}
    model_form_class = type("AutoModelForm",(ModelForm,),attrs)
    setattr(model_form_class,'__new__',__new__)
    setattr(model_form_class,'clean',default_clean)
    return model_form_class

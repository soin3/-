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
            if not hasattr(admin_class,"is_add_form"):
                if field_name in admin_class.readonly_fields:
                    print(field_name)
                    field_obj.widget.attrs['disabled']='disabled'

            if hasattr(admin_class,"clean_%s"%field_name):
                field_clean_func = getattr(admin_class,"clean_%s"%field_name)
                setattr(cls,"clean_%s"%field_name,field_clean_func)


        return ModelForm.__new__(cls)
    def default_clean(self):
        '''给所有form加一个clean验证,相当于djang的clean验证'''
        error_list = []
        if admin_class.readonly_table:
            raise ValidationError(
                        _('只读表，不可修改'),
                        code='invalid',)
        if self.instance.id:
            for field in admin_class.readonly_fields:
                field_val = getattr(self.instance,field)
                if hasattr(field_val,"select_related"):#m2m
                    m2m_objs = getattr(field_val,"select_related")().select_related()
                    m2m_vals = [i[0] for i in m2m_objs.values_list('id')]
                    set_m2m_vals = set(m2m_vals)
                    set_m2m_vals_from_frontend = set([i.id for i in self.cleaned_data.get(field)])
                    if set_m2m_vals != set_m2m_vals_from_frontend:
                        self.add_error(field,"只读字段，不可修改")
                    continue

                field_clean_data = self.cleaned_data.get(field)
                if field_val != field_clean_data:
                    error_list.append(ValidationError(
                        _('%(field)s只读字段，不可修改'),
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

__author__ = 'solin'
from crm import models

enabled_admins = {}
class BaseAdmin(object):
    #基类
    list_display = []
    list_filters = []
    list_per_page = 20#默认分页页数
    search_fields = []
    ordering = None

class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','consult_course','date','content']
    list_filters = ['source','consultant','consult_course','date']
    list_per_page = 5
    search_fields = ['qq','name','consultant__name']

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer','consultant','date']

#注册admin方法
def register(model_class,admin_class=None):
    # 仿admin注册功能，如果传入的model_class不在enabled_admins字典里，就获取model_class的app名字(model_class._meta.app_label)
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
    # {'crm':{'userprofile':admin_class,''customer':customer_class},放入enabled_admins字典里。注：model_class._meta.model_name是获取表名
    admin_class.model = model_class  #绑定model对象和admin类，相当于model = models.Customer
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name]=admin_class

#注册
register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)


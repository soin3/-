__author__ = 'solin'
from crm import models
from django.shortcuts import render,redirect

enabled_admins = {}
class BaseAdmin(object):
    #基类
    list_display = []
    list_filters = []
    list_per_page = 20#默认分页页数
    search_fields = []
    ordering = None
    filter_horizontal = []
    actions = ["delete_selected_ojs",]
    def delete_selected_ojs(self,request,querysets):
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        if request.POST.get("delete_confirm") == "yes":
            querysets.delete()
            return redirect("/king_admin/%s/%s/"%(app_name,table_name))
        selected_ids = ','.join([str(i.id) for i in querysets])
        return render(request,"king_admin/table_objs_delete.html",{"objs":querysets,"admin_class":self,
                                                               "app_name":app_name,"table_name":table_name,
                                                               "selected_ids":selected_ids,"action":request._admin_action})
    delete_selected_ojs.display_name = "删除记录"



class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','consult_course','date','content']
    list_filters = ['source','consultant','consult_course','date']
    list_per_page = 5
    search_fields = ['qq','name','consultant__name']
    filter_horizontal = ('tags',)#复选框设置


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer','consultant','date']

class UserProfileAdmin(BaseAdmin):
    list_display = ['user','name']

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
register(models.UserProfile,UserProfileAdmin)


__author__ = 'solin'
from crm import models
from django.shortcuts import render,redirect,HttpResponse

enabled_admins = {}
class BaseAdmin(object):
    #基类
    list_display = []
    list_filters = []
    list_per_page = 20#默认分页页数
    search_fields = []
    readonly_fields = []
    ordering = None
    filter_horizontal = []
    readonly_table = False
    actions = ["delete_selected_ojs",]
    form_exclude_fields = []#不显示字段
    def delete_selected_ojs(self,request,querysets):
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        if self.readonly_table:
            error = '此表只读不可更改'
        else:
            error = ''
        if request.POST.get("delete_confirm") == "yes":
            if not self.readonly_table:
                querysets.delete()
            return redirect("/king_admin/%s/%s/"%(app_name,table_name))
        selected_ids = ','.join([str(i.id) for i in querysets])
        return render(request,"king_admin/table_objs_delete.html",{"objs":querysets,"admin_class":self,
                                                               "app_name":app_name,"table_name":table_name,
                                                               "selected_ids":selected_ids,"action":request._admin_action,
                                                               "error":error})

    def default_form_validation(self):
        #自定义form
        pass
    delete_selected_ojs.display_name = "删除记录"


class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','consult_course','date','content','status','enroll']
    list_filters = ['source','consultant','consult_course','date']
    list_per_page = 5
    search_fields = ['qq','name','consultant__name']
    filter_horizontal = ('tags',)#复选框设置
    readonly_fields = ["qq","consultant","tags"]
    readonly_table =False

    def default_form_validation(self):
        #对整个form验证
        content = self.cleaned_data.get("content")#content长度验证。。
        if len(content) < 5:
            return self.add_error('content',"不能少于5个字")
            # return self.ValidationError(
            #         ('%(field)s不能少于5个字'),
            #         code='invalid',
            #         params= {'field':"咨询详情",})

    def enroll(self):#显示数据库中不存在的字段
        if self.instance.status == 1:
            link_name = "报名新课"
        else:
            link_name = "报名"
        return '''<a style="color:red"href="/crm/customer/%s/enrollment/">%s</a>'''%(self.instance.id,link_name)
    enroll.display_name = "报名链接"
    # def clean_name(self):
    #     #对单个字段验证
    #     print(self.cleaned_data["name"])
    #     if not self.cleaned_data["name"]:
    #         self.add_error('name',"姓名不可为空")


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer','consultant','date']

class UserProfileAdmin(BaseAdmin):
    list_display = ['email','name']
    readonly_fields = ['password']
    filter_horizontal = ("user_permissions","groups","")
    form_exclude_fields = ["last_login"]


class CourseRecordAdmin(BaseAdmin):
    list_display = ('from_class','day_num','teacher','has_homework','homework_title','date')
    list_filters = ["from_class","day_num"]
    def initialize_studyrecords(self,request,queryset):
        if len(queryset)>1:
            return HttpResponse("nonono")
        #print(queryset[0].from_class.enrollment_set.all())#反查出所有报名此班级课程的学员
        new_obj_list = []
        for enroll_obj in queryset[0].from_class.enrollment_set.all():

            new_obj_list.append(models.StudyRecord(
                student = enroll_obj,
                course_record = queryset[0],
                record = 0,
                score = 0,
            ))
        try:
            models.StudyRecord.objects.bulk_create(new_obj_list)#批量创建
        except Exception as e:
            print('批量创建失败,请检查是否有对应记录')

        return  redirect("/king_admin/crm/studyrecord/?search=&course_record=%s"%queryset[0].id)
    initialize_studyrecords.display_name = "初始化本节所有学员的上课记录"
    actions = ['initialize_studyrecords']

class StudyRecordAdmin(BaseAdmin):
    list_display = ('student','course_record','record','score','date')
    list_filters = ['course_record','score','record']
    #list_editable = ['score','record']行内编辑功能，如何做?


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
register(models.StudyRecord,StudyRecordAdmin)
register(models.CourseRecord,CourseRecordAdmin)


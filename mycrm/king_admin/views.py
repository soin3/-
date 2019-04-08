from django.shortcuts import render,redirect
from king_admin import king_admin
from king_admin.utils import table_filter,table_sort,table_search
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.forms import create_model_form
from django.contrib.auth.decorators import login_required
from crm.permissions import permission
# Create your views here.

@login_required

def index(request):
    #print(king_admin.enabled_admins)
    return render(request, "king_admin/table_index.html",{"table_list":king_admin.enabled_admins})

@login_required
def display_table_objs(request,app_name,table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    if request.method == "POST":#action
        select_ids = request.POST.get("selected_ids")
        action = request.POST.get("action")
        if select_ids:
            select_objs = admin_class.model.objects.filter(id__in = select_ids.split(','))
        else:
            return redirect(("/king_admin/%s/%s/"%(app_name,table_name)))
        if hasattr(admin_class,action):
            action_func = getattr(admin_class,action)
            request._admin_action = action
            return action_func(admin_class,request,select_objs)

        #！！！非常重要的三步
    object_list,filter_conditions = table_filter(request,admin_class)#过滤
    object_list = table_search(request,admin_class,object_list)#搜索
    object_list,orderby_key = table_sort(request,admin_class,object_list)#排序

    #分页功能
    paginator = Paginator(object_list, admin_class.list_per_page) # Show 20 contacts per page
    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)

    return render(request,"king_admin/table_objs.html",
                  {"admin_class":admin_class,
                   "query_sets":query_sets,
                   "filter_conditions":filter_conditions,
                   "orderby_key":orderby_key,
                   "previous_key":request.GET.get("o",''),
                   "search_text":request.GET.get("search",''),
                  },
                  )
@login_required
def table_objs_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method =="POST":
        form_obj = model_form_class(request.POST,instance=obj)#加了instance是修改，不加是添加
        if form_obj.is_valid():
            form_obj.save()
    else:
        form_obj = model_form_class(instance=obj)
    return render(request,"king_admin/table_objs_change.html",{"form_obj":form_obj,
                                                               "admin_class":admin_class,
                                                               "app_name":app_name,
                                                               "table_name":table_name})
@login_required
def table_objs_add(request,app_name,table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    admin_class.is_add_form = True
    model_form_class = create_model_form(request,admin_class)
    if request.method =="POST":
        form_obj = model_form_class(request.POST)#加了instance是修改，不加是添加
        if form_obj.is_valid():
            form_obj.save()
        return redirect(request.path.replace("/add/","/"))
    else:
        form_obj = model_form_class()
    return render(request,"king_admin/table_objs_add.html",{"form_obj":form_obj,"admin_class":admin_class,})

@login_required
def table_objs_delete(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)
    error = ''
    if admin_class.readonly_table:
        error = '此表只读不可更改'
    else:
        error = ''
    if request.method =="POST":
        if not admin_class.readonly_table:
            obj.delete()
            return redirect("/king_admin/%s/%s/"%(app_name,table_name))
    return render(request,"king_admin/table_objs_delete.html",{"obj":obj,"admin_class":admin_class,
                                                               "app_name":app_name,"table_name":table_name,"error":error})

@login_required
def change_password(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    errors = {}
    if request.method =='POST':
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            if len(password1) >5:
                obj.set_password(password1)#调用AbstractBaseUser的改密码方法
                obj.save()
                return redirect(request.path.rstrip("password/"))
            else:
                errors['errors1']='密码不得小于六位'
        else:
            errors['errors2']='密码不一致'
    return render(request,'king_admin/change_password.html',{"obj":obj,"admin_class":admin_class,"model_form_class":model_form_class,"errors":errors})




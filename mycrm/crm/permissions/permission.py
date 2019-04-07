__author__ = 'Administrator'
from crm.permissions import permission_list
from django.shortcuts import HttpResponse,render,redirect
from django.urls import resolve
from mycrm import settings


def perm_check(*args,**kwargs):
    request = args[0]
    if request.user.is_authenticated:
        for permission_name,v in permission_list.permission_dic.items():
            url_matched = False
            if v['url_type'] == 1:
                if v['url'] == request.path:#绝对url匹配
                    print('绝对url匹配')
                    url_matched = True
            else:
                #把绝对的url请求转成相对的urlname
                resolve_url_obj = resolve(request.path)
                print(v['url'])
                if resolve_url_obj.url_name == v['url']:#相对的url别名匹配了
                    print('相对的url别名匹配了')
                    url_matched = True

            if url_matched:
                print('url_matched')
                if v['method'] == request.method:#请求方法匹配
                    arg_matched = True
                    for request_arg in v['args']:
                        request_method_func = getattr(request,v['method'])
                        if not request_method_func.get(request_arg):
                           arg_matched =False

                    if arg_matched:#走到这里，仅仅代表这个请求和这条权限的定义规则匹配了
                        print(arg_matched)
                        if request.user.has_perm(permission_name):
                            #有权限
                            print("有权限")
                            return True
    else:
        return redirect(settings.LOGIN_URL)





def check_permission(func):
    def inner(*args,**kwargs):
        if perm_check(*args,**kwargs) is True:
            return  func(*args,**kwargs)
        else:
            return HttpResponse("403fobbiden")
    return inner
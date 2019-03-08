__author__ = 'solin'
from django.db.models import Q
def table_filter(request,admin_class):
    #进行条件过滤并且返回过滤后的数据
    filter_conditions = {}
    keywords = ['page','o','search']#保留的分页关键字、排序关键字、搜索关键字
    for k,v in request.GET.items():
        if k in keywords:
            continue
        if v:
            filter_conditions[k]=v

    return admin_class.model.objects.filter(**filter_conditions).\
               order_by("-%s"%admin_class.ordering if admin_class.ordering else "-id"),\
                filter_conditions

def table_sort(request,admin_class,object_list):
    #排序功能，获取o字段参数，如果存在，判断是否带负号，带了就去除，不带就加上
    orderby_key = request.GET.get("o")
    if orderby_key:
        res = object_list.order_by(orderby_key)
        if orderby_key.startswith("-"):
            orderby_key = orderby_key.strip("-")
        else:
            orderby_key = "-%s"%orderby_key
    else:
        res = object_list
    return res,orderby_key

def table_search(request,admin_class,object_list):
    #搜索功能
    search_key = request.GET.get("search","")
    q_obj = Q()
    q_obj.connector = "OR"
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains"%column,search_key))
    res = object_list.filter(q_obj)
    return res






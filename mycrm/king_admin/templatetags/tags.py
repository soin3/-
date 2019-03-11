__author__ = 'solin'
#自定义标签
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
register = template.Library()

@register.simple_tag
def render_app_name(admin_class):
    #返回model的verbose_name
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:
            column_data = getattr(obj,"get_%s_display"%column)()
        else:
            column_data = getattr(obj,column)
        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        if index ==0:#如果是第1列，就跳转到修改页面
            column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,
                                                                                      obj_id=obj.id,data=column_data)
        row_ele +="<td>%s</td>"%column_data
    return mark_safe(row_ele)

@register.simple_tag
def render_page_ele(loop_counter,query_sets,filter_conditions,previous_key,search_text):
    '''获取当前页并带上筛选条件'''
    #query_sets.number：当前页,loop_counter:循环总页数范围
    filter=''
    for k,v in filter_conditions.items():
        filter += '&%s=%s'%(k,v)
    if abs(query_sets.number - loop_counter) <= 2:#采用循环总页数和当前页相减取绝对值的方法，如果绝对值相减小于等于1，就显示出来，其余不显示
        ele_class = ""
        if query_sets.number == loop_counter:#当前页加active样试
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s&o=%s&search=%s">%s</a></li>'''%\
              (ele_class,loop_counter,filter,previous_key,search_text,loop_counter)
        return  mark_safe(ele)
    return ''

@register.simple_tag
def now_page_ele(page_number,query_sets,filter_conditions,tag,previous_key,search_text):
    '''获取上一页、下一页、首页、尾页并带上筛选条件'''
    filter=''
    for k,v in filter_conditions.items():
        filter += '&%s=%s'%(k,v)
    if tag==0:
        ele = '''<li class=""><a href="?page=%s%s&o=%s&search=%s">%s</a></li>'''%(page_number,filter,previous_key,search_text,'上一页')
    elif tag==1:
        ele = '''<li class=""><a href="?page=%s%s&o=%s&search=%s">%s</a></li>'''%(page_number,filter,previous_key,search_text,'下一页')
    elif tag ==2:
        ele = '''<li class=""><a href="?page=%s%s&o=%s&search=%s">%s</a></li>'''%(page_number,filter,previous_key,search_text,'首页')
    elif tag ==3:
        ele = '''<li class=""><a href="?page=%s%s&o=%s&search=%s">%s</a></li>'''%(page_number,filter,previous_key,search_text,'尾页')
    return mark_safe(ele)


@register.simple_tag
def render_filter_ele(filter_field,admin_class,filter_conditions):#过滤筛选方法
    # select_ele = '''<select class="form-control"name='%s'><option value=''>---</option>'''%filter_field
    select_ele = '''<select class="form-control"name='{filter_field}'><option value=''>---</option>'''
    field_obj = admin_class.model._meta.get_field(filter_field)#获取字段对象
    if field_obj.choices:
        selected = ""
        for choice_item in field_obj.choices:#获取choices格式方法
            if filter_conditions.get(filter_field) ==str(choice_item[0]):#查询过后刷新页面选中筛选框
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>'''%(choice_item[0],selected,choice_item[1])
            selected=''
    if type(field_obj).__name__=="ForeignKey":
        selected = ""
        for choice_item in field_obj.get_choices()[1:]:#获取外键方法
            if filter_conditions.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele +='''<option value='%s' %s>%s</option>'''%(choice_item[0],selected,choice_item[1])
            selected=''
    if type(field_obj).__name__ in ["DateField","DateTimeField"]:
        data_list = []
        data_list.append(['今天',datetime.now().date()])#获取当前时间
        data_list.append(['昨天',datetime.now().date() - timedelta(days=1)])
        data_list.append(['近7天',datetime.now().date() - timedelta(days=7)])
        data_list.append(['近30天',datetime.now().date() - timedelta(days=30)])
        data_list.append(['近90天',datetime.now().date() - timedelta(days=90)])
        data_list.append(['近365天',datetime.now().date() - timedelta(days=365)])
        data_list.append(['本月',datetime.now().date().replace(day=1)])#从月初到现在
        data_list.append(['今年',datetime.now().date().replace(month=1,day=1)])#从年初到现在
        selected=''
        for i in data_list:
            if filter_conditions.get('date__gte') == str(i[1]):
                selected = "selected"
            select_ele +='''<option value='%s' %s>%s</option>'''%(i[1],selected,i[0])
            selected=''
        filter_field_name = '%s__gte'%filter_field
    else:
        filter_field_name = filter_field
    select_ele +='</select>'
    select_ele = select_ele.format(filter_field=filter_field_name)
    return mark_safe(select_ele)

@register.simple_tag
def build_header_column(column,orderby_key,filter_conditions):
    filter=''
    for k,v in filter_conditions.items():
        filter += '&%s=%s'%(k,v)
    ele = '''<th><a href="?{filter}&o={orderby_key}">{column}</a>{sort_icon}</th>'''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down"></span>'''
        if orderby_key.strip("-") == column:
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon=''
    else:#没有排序
        orderby_key = column
        sort_icon=''
    ele= ele.format(orderby_key=orderby_key,column=column,sort_icon=sort_icon,filter=filter)
    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    return  admin_class.model._meta.verbose_name

@register.simple_tag
def get_m2m_list(admin_class,field,form_obj):
    #返回m2m备选数据
    #表结构对象的某个字段
    field_obj = getattr(admin_class.model,field.name)
    all_obj_list = field_obj.rel.model.objects.all()
    #单条数据的对象中的某个字段
    if form_obj.instance.id:
        obj_instance_field = getattr(form_obj.instance,field.name)
        selected_obj_list = obj_instance_field.all()
    else:
        #创建新的m2m一条记录
        return all_obj_list
    standby_obj_list = []
    for obj in all_obj_list:
        if obj not in selected_obj_list:
            standby_obj_list.append(obj)
    return standby_obj_list

@register.simple_tag
def selected_m2m_list(form_obj,field):
    #返回m2m已选数据
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance,field.name)
        return field_obj.all()



__author__ = 'Administrator'
permission_dic = {
    'crm.can_access_my_course':{
         'url_type':0,#0相对，1绝对
    'url':'stu_my_classes',
    'method':'GET',
    'args':[]
    },
    'crm.can_access_customer_list':{
        'url_type':1,
        'url':'king_admin/crm/customer/',
        'method':'GET',
        'args':[]
    },
   'crm.can_access_studyrecords':{
        'url_type':0,
        'url':'studyrecords',
        'method':'GET',
        'args':[]
    },
     'crm.can_access_customer_detail':{
        'url_type':0,
        'url':'table_obj_change',
        'method':'GET',
        'args':[]
    },
       'crm.can_access_homework_detail':{
        'url_type':0,
        'url':'homework_detail',
        'method':'GET',
        'args':[]
    },
           'crm.can_upload_homework':{
        'url_type':0,
        'url':'homework_detail',
        'method':'POST',
        'args':[]
    },
}

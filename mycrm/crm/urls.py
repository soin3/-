
from crm import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index,name="sales_index"),
    url(r'^customers/$', views.customers_list,name="customers_list"),
    url(r'^customer/(\d+)/enrollment/$', views.enrollment,name="enrollment"),
    # url(r'^teacher', views.index,name="my_class_list"),
    url(r'^customer/registration/(\d+)/',views.stu_registration,name="stu_registration"),
    url(r'^contract_review/(\d+)/',views.contract_review,name="contract_review"),
    url(r'^payment/(\d+)/',views.payment,name="payment"),
    url(r'^enrollment_rejection/(\d+)/',views.enrollment_rejection,name="enrollment_rejection"),
    # 加超时时间url(r'^customer/registration/(\d+)/(\w+)',views.stu_registration,name="stu_registration"),

]

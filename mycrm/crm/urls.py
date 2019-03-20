
from crm import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index,name="sales_index"),
    url(r'^customers/$', views.customers_list,name="customers_list"),
    # url(r'^teacher', views.index,name="my_class_list"),


]

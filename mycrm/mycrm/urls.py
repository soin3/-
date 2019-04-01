from django.contrib import admin
from django.conf.urls import url,include
from mycrm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
     url(r'^$', views.index),
    url(r'^crm/', include("crm.urls")),
    url(r'^student/', include("student.urls")),
    url(r'^king_admin/', include("king_admin.urls")),
    url(r'^account/login/$', views.access_login),
    url(r'^account/logout/$', views.access_logout,name="access_logout"),
    url(r'^newindex/$', views.newindex),
]
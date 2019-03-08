from django.contrib import admin
from django.conf.urls import url,include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crm/', include("crm.urls")),
    url(r'^student/', include("student.urls")),
    url(r'^king_admin/', include("king_admin.urls")),

]
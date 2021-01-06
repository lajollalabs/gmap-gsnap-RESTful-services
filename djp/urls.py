from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^gscript/', include('gscript.gmapr.urls')),
    url(r'^bedtools/', include('gscript.bedtools.urls')),
]

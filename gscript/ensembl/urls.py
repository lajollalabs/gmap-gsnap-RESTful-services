from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'hello', views.hello, name='hello'),
    url(r'get_id', views.get_id, name='get_id'),
]

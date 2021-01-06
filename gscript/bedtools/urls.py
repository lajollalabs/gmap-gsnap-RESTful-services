from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'hello', views.hello, name='hello'),
    url(r'get-sequence-for-coordinates', views.get_sequence_for_coordinates, name='get-sequence-for-coordinates'),
    url(r'get-sequence-for-gsnap-coordinates', views.get_sequence_for_gsnap_coordinates, name='get-sequence-for-gsnap-coordinates'),
]

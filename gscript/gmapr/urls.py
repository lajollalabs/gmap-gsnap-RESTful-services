from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'hello', views.hello, name='hello'),
    url(r'simple-gsnap', views.simple_gsnap, name='simple-gsnap'),
#    url(r'gsnap-with-rna-bld', views.gsnap_with_rna_bld, name='gsnap-with-rna-bld'),
#    url(r'cdna-gsnap', views.gsnap_cdna_to_genomic, name='cdna-gsnap'),
    # url(r'get_helm_rule', views.get_helm_rule, name='get_helm_rule')
]

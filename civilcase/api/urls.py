#-*-coding:utf-8-*-
from django.conf.urls import url
from .views import CivilDetailAPIView, CivilNaturePersonAPIView

__author__ = 'malixin'


urlpatterns = [
    url(r'^persons/$', CivilNaturePersonAPIView.as_view(), name='api-nature-person'),
    # url(r'^civilschemedetail/(?P<pk>\d+)/$', LawsuitSchemeDetailAPIView.as_view(), name='civil-scheme-detail'),
    # url(r'^civilcasedetail/(?P<pk>\d+)/$', CivilCaseDetailAPIView.as_view(), name='civil-case-detail'),
]


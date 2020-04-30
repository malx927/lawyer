#-*-coding:utf-8-*-
from django.conf.urls import url

from calculator.api.views import AreaCodeListAPIView, IndusAverWageAPIView, IndusNurseWageAPIView, FuneralExpenseAPIView

__author__ = 'malixin'


urlpatterns = [
    url(r'^area_code_list/$', AreaCodeListAPIView.as_view(), name='area-code-list'),
    url(r'^indust_aver_wage/$', IndusAverWageAPIView.as_view(), name='indust-aver-wage'),
    url(r'^indust_nurse_wage/$', IndusNurseWageAPIView.as_view(), name='indust-nurse-wage'),
    url(r'^funeral/$', FuneralExpenseAPIView.as_view(), name="calc-funeral-expense"),
]


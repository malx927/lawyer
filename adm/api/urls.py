#-*-coding:utf-8-*-
from django.conf.urls import url

from adm.api.views import UserInfoDetailAPIView

__author__ = 'malixin'


urlpatterns = [
    url(r'^user_detail/(?P<pk>\d+)/$', UserInfoDetailAPIView.as_view(), name='api-user-detail'),
    # url(r'^areacodelist/$', AreaCodeListAPIView.as_view(), name='area-code-list'),
    # url(r'^orderdaystats/$', OrderDayStats.as_view(), name='order-day-stats'),
    # url(r'^ordermonthstats/$', OrderMonthStats.as_view(), name='order-month-stats'),
    # url(r'^orderyearstats/$', OrderYearStats.as_view(), name='order-year-stats'),
    # url(r'^ordercategorystats/$', OrderCategoryStats.as_view(), name='order-category-stats'),
    # url(r'^order-day-analysis/$', OrderDayAnalysis.as_view(), name='order-day-analysis'),
    # url(r'^order-month-analysis/$', OrderMonthAnalysis.as_view(), name='order-month-analysis'),
    # url(r'^order-year-analysis/$', OrderYearAnalysis.as_view(), name='order-year-analysis'),
]


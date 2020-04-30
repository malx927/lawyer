from django.conf.urls import url, include
from django.views.generic import TemplateView

from adm.views import (
    UserAuthView,
    UserCategoryListView,
    OfficeView,
    OfficeUpdateView,
    UserDetailChangeView,
    UserDetailView,
    MyCase,
    CaseCategory,
    CaseInfo,
    CaseDistributeView,
    CaseDoingListView,
    CaseSearchListView)

urlpatterns = [
    url(r'^user_auth/$', UserAuthView.as_view(), name="user-auth"),
    url(r'^user_category_list/$', UserCategoryListView.as_view(), name="user-category-list"),
    url(r'^user_detail_change/$', UserDetailChangeView.as_view(), name="user-detail-change"),
    url(r'^user_detail/(?P<pk>\d+)/$', UserDetailView.as_view(), name="user-detail"),
    url(r'^office/$', OfficeView.as_view(), name="office"),
    url(r'^office_update/(?P<pk>\d+)/$', OfficeUpdateView.as_view(), name="office-update"),

    url(r'^my_case/$', MyCase.as_view(), name="my-case"),
    url(r'^case_category/$', CaseCategory.as_view(), name="case-category"),

    url(r'^case_info/$', CaseInfo.as_view(), name="case-info"),
    url(r'^case_distrib_list/$', CaseDistributeView.as_view(), name="case-distrib-list"),
    url(r'^case_doing_list/$', CaseDoingListView.as_view(), name="case-doing-list"),
    url(r'^case_search_list/$', CaseSearchListView.as_view(), name="case-search-list"),

]
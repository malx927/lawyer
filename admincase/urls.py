from django.conf.urls import url, include

from admincase.views import AdminCaseAddView, AdminCaseDeleteView, AdminCaseDetailView, AdminCaseUpdateView, \
    AdminCaseStageView, AdminCaseDetailUpdateView, AdminCaseDetailDeleteView, AdminCaseDetailSchemeView, \
    AdminCaseDetailListView, AdminCaseDistribView

urlpatterns = [
    url(r'^admin_add/$', AdminCaseAddView.as_view(), name="admin-case-add"),
    url(r'^admin_del/(?P<admin_id>\d+)/$', AdminCaseDeleteView.as_view(), name="admin-case-del"),
    url(r'^admin_detail/(?P<admin_id>\d+)/$', AdminCaseDetailView.as_view(), name="admin-case-detail"),
    url(r'^admin_update/(?P<admin_id>\d+)/$', AdminCaseUpdateView.as_view(), name="admin-case-update"),
    url(r'^admin_stage/(?P<admin_id>\d+)/$', AdminCaseStageView.as_view(), name="admin-case-stage"),
    url(r'^admin_detail_update/(?P<detail_id>\d+)/$', AdminCaseDetailUpdateView.as_view(), name="admin-case-detail-update"),
    url(r'^admin_detail_del/(?P<detail_id>\d+)/$', AdminCaseDetailDeleteView.as_view(), name="admin-case-detail-delete"),
    url(r'^admin_detail_scheme/(?P<detail_id>\d+)/$', AdminCaseDetailSchemeView.as_view(), name="admin-case-detail-scheme"),
    url(r'^admin_detail_list/(?P<detail_id>\d+)/$', AdminCaseDetailListView.as_view(), name="admin-case-detail-list"),
    url(r'^admin_lawyer_distrib/(?P<admin_id>\d+)/$', AdminCaseDistribView.as_view(), name="admin-lawyer-distrib"),

]
from django.conf.urls import url, include

from crimicivil.views import CrmCivilCaseAddView, CrmCivilCaseDeleteView, CrmCivilCaseDetailView, \
    CrmCivilCaseUpdateView, CrmCivilCaseStageView, CrmCivilCaseDetailUpdateView, CrmCivilCaseDetailDeleteView, \
    CrmCivilCaseDetailSchemeView, CrmCivilCaseDetailListView, CrmCivilCaseDistribView

urlpatterns = [
    url(r'^crmcivil_add/$', CrmCivilCaseAddView.as_view(), name="crmcivil-case-add"),
    url(r'^crmcivil_del/(?P<crmcivil_id>\d+)/$', CrmCivilCaseDeleteView.as_view(), name="crmcivil-case-del"),
    url(r'^crmcivil_detail/(?P<crmcivil_id>\d+)/$', CrmCivilCaseDetailView.as_view(), name="crmcivil-case-detail"),
    url(r'^crmcivil_update/(?P<crmcivil_id>\d+)/$', CrmCivilCaseUpdateView.as_view(), name="crmcivil-case-update"),
    url(r'^crmcivil_stage/(?P<crmcivil_id>\d+)/$', CrmCivilCaseStageView.as_view(), name="crmcivil-case-stage"),
    url(r'^crmcivil_detail_update/(?P<detail_id>\d+)/$', CrmCivilCaseDetailUpdateView.as_view(), name="crmcivil-case-detail-update"),
    url(r'^crmcivil_detail_del/(?P<detail_id>\d+)/$', CrmCivilCaseDetailDeleteView.as_view(), name="crmcivil-case-detail-delete"),
    url(r'^crmcivil_detail_scheme/(?P<detail_id>\d+)/$', CrmCivilCaseDetailSchemeView.as_view(), name="crmcivil-case-detail-scheme"),
    url(r'^crmcivil_detail_list/(?P<detail_id>\d+)/$', CrmCivilCaseDetailListView.as_view(), name="crmcivil-case-detail-list"),
    url(r'^crmcivil_lawyer_distrib/(?P<crmcivil_id>\d+)/$', CrmCivilCaseDistribView.as_view(), name="crmcivil-lawyer-distrib"),

]
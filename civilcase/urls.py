from django.conf.urls import url, include

from civilcase.views import (
    CivilCaseAddView,
    CivilCaseDetailView,
    CivilCaseUpdateView,
    CivilCaseDetailUpdateView,
    CivilCaseStageView,
    CivilCaseDetailSchemeView,
    CivilCaseDetailListView,
    CivilCaseDistribView,
    CivilCaseDeleteView,
    CivilCaseDetailDeleteView,
    CivilCasePrintView,
    CivilAgentView, CivilAuthLetterView, RiskNoticeView, LegalRepresCertView, CivilComplaintView, CivilStatementView,
    CivilEvidenceListView, CivilCompensateView, CivilAskingOutlineView, CivilApplicationView,
    CivilAnswerCounterClaimView, CivilCounterClaimView, CivilPleadingsView)

urlpatterns = [
    url(r'^civil_add/$', CivilCaseAddView.as_view(), name="civil-case-add"),
    url(r'^civil_del/(?P<civil_id>\d+)/$', CivilCaseDeleteView.as_view(), name="civil-case-del"),
    url(r'^civil_detail/(?P<civil_id>\d+)/$', CivilCaseDetailView.as_view(), name="civil-case-detail"),
    url(r'^civil_update/(?P<civil_id>\d+)/$', CivilCaseUpdateView.as_view(), name="civil-case-update"),
    url(r'^civil_stage/(?P<civil_id>\d+)/$', CivilCaseStageView.as_view(), name="civil-case-stage"),
    url(r'^civil_detail_update/(?P<detail_id>\d+)/$', CivilCaseDetailUpdateView.as_view(), name="civil-case-detail-update"),
    url(r'^civil_detail_del/(?P<detail_id>\d+)/$', CivilCaseDetailDeleteView.as_view(), name="civil-case-detail-delete"),
    url(r'^civil_detail_scheme/(?P<detail_id>\d+)/$', CivilCaseDetailSchemeView.as_view(), name="civil-case-detail-scheme"),
    url(r'^civil_detail_list/(?P<detail_id>\d+)/$', CivilCaseDetailListView.as_view(), name="civil-case-detail-list"),
    url(r'^civil_lawyer_distrib/(?P<civil_id>\d+)/$', CivilCaseDistribView.as_view(), name="civil-lawyer-distrib"),

]
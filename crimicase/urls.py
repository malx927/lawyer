from django.conf.urls import url, include


from crimicase.views import (
    CrimiCaseAddView,
    CrimiCaseDetailView,
    CriminalCaseUpdateView,
    CriminalCaseStageView,
    CriminalCaseDetailUpdateView,
    CriminalCaseDetailDeleteView,
    CriminalCaseDetailSchemeView,
    CriminalCaseDetailListView,
    CriminalCaseDeleteView,
    CriminalCaseDistribView)

urlpatterns = [
    url(r'^crimi_add/$', CrimiCaseAddView.as_view(), name="criminal-case-add"),
    url(r'^crimi_del/(?P<crimi_id>\d+)/$', CriminalCaseDeleteView.as_view(), name="criminal-case-del"),
    url(r'^crimi_detail/(?P<crimi_id>\d+)/$', CrimiCaseDetailView.as_view(), name="criminal-case-detail"),
    url(r'^crimi_update/(?P<crimi_id>\d+)/$', CriminalCaseUpdateView.as_view(), name="criminal-case-update"),
    url(r'^crimi_stage/(?P<crimi_id>\d+)/$', CriminalCaseStageView.as_view(), name="criminal-case-stage"),
    url(r'^crimi_detail_update/(?P<detail_id>\d+)/$', CriminalCaseDetailUpdateView.as_view(), name="criminal-case-detail-update"),
    url(r'^crimi_detail_del/(?P<detail_id>\d+)/$', CriminalCaseDetailDeleteView.as_view(), name="criminal-case-detail-delete"),
    url(r'^crimi_detail_scheme/(?P<detail_id>\d+)/$', CriminalCaseDetailSchemeView.as_view(), name="criminal-case-detail-scheme"),
    url(r'^crimi_detail_list/(?P<detail_id>\d+)/$', CriminalCaseDetailListView.as_view(), name="criminal-case-detail-list"),
    url(r'^crimi_lawyer_distrib/(?P<crimi_id>\d+)/$', CriminalCaseDistribView.as_view(), name="criminal-lawyer-distrib"),

]
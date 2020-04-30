from django.conf.urls import url, include

from crimiprivate.views import (
    CrimiPrivateCaseAddView,
    CrimiPrivateDetailView,
    CrimiPrivateDetailSchemeView,
    CrimiPrivateUpdateView,
    CrimiPrivateDeleteView,
    CrimiPrivateStageView,
    CrimiPrivateDetailUpdateView,
    CrimiPrivateDetailDeleteView,
    CrimiPrivateDetailListView,
    CrimiPrivateDistribView,
)

urlpatterns = [
    url(r'^private_add/$', CrimiPrivateCaseAddView.as_view(), name="private-case-add"),
    url(r'^private_del/(?P<private_id>\d+)/$', CrimiPrivateDeleteView.as_view(), name="private-case-del"),
    url(r'^private_detail/(?P<private_id>\d+)/$', CrimiPrivateDetailView.as_view(), name="private-case-detail"),
    url(r'^private_update/(?P<private_id>\d+)/$', CrimiPrivateUpdateView.as_view(), name="private-case-update"),
    url(r'^private_stage/(?P<private_id>\d+)/$', CrimiPrivateStageView.as_view(), name="private-case-stage"),
    url(r'^private_detail_update/(?P<detail_id>\d+)/$', CrimiPrivateDetailUpdateView.as_view(), name="private-case-detail-update"),
    url(r'^civil_detail_del/(?P<detail_id>\d+)/$',CrimiPrivateDetailDeleteView.as_view(), name="private-case-detail-delete"),
    url(r'^private_detail_scheme/(?P<detail_id>\d+)/$', CrimiPrivateDetailSchemeView.as_view(), name="private-case-detail-scheme"),
    url(r'^private_detail_list/(?P<detail_id>\d+)/$', CrimiPrivateDetailListView.as_view(), name="private-case-detail-list"),
    url(r'^private_lawyer_distrib/(?P<private_id>\d+)/$', CrimiPrivateDistribView.as_view(), name="private-lawyer-distrib"),

]
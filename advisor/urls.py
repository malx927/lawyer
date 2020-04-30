from django.conf.urls import url, include
from django.views.generic import TemplateView

from adm.views import UserAuthView, UserCategoryListView, OfficeView, OfficeUpdateView
from advisor.views import ConsultPanelView, ConsultUnitView, ConsultUnitListView, ConsultUnitUpdateView, \
    ConsultUnitDeleteView, ConsultUnitDispatchView

urlpatterns = [
    url(r'^advisor_panel/$', ConsultPanelView.as_view(), name="advisor-panel"),
    url(r'^consult_unit_add/$', ConsultUnitView.as_view(), name="consult-unit-add"),
    url(r'^consult_unit_list/$', ConsultUnitListView.as_view(), name="consult-unit-list"),
    url(r'^consult_unit_update/(?P<pk>\d+)/$', ConsultUnitUpdateView.as_view(), name="consult-unit-update"),
    url(r'^consult_unit_delete/(?P<pk>\d+)/$', ConsultUnitDeleteView.as_view(), name="consult-unit-delete"),
    url(r'^consult_unit_dispatch/$', ConsultUnitDispatchView.as_view(), name="consult-unit-dispatch"),
    # url(r'^office_update/(?P<pk>\d+)/$', OfficeUpdateView.as_view(), name="office-update"),
]
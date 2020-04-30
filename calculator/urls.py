from django.conf.urls import url, include

from calculator.views import TrafficCalcView, CalculatorView, HospitalCalcView, AppraiseCalcView, RelationCalcView, \
    CalculatorResultView

urlpatterns = [
    url(r'^$', CalculatorView.as_view(), name="calc-index"),
    url(r'^traffic/$', TrafficCalcView.as_view(), name="traffic-index"),
    url(r'^hospital/$', HospitalCalcView.as_view(), name="hospital-index"),
    url(r'^appraise/$', AppraiseCalcView.as_view(), name="appraise-index"),
    url(r'^relation/$', RelationCalcView.as_view(), name="relation-index"),
    url(r'^result/$', CalculatorResultView.as_view(), name="calc-result"),

]
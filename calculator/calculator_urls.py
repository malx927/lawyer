from django.conf.urls import url, include

from calculator.calculatorviews import CalculatorPanelView, IncomeExpendItemView, IncomeExpendItemAddView, \
    IncomeExpendItemUpdateView, IncomeExpendItemDelView, IndustryView, IndustryAddView, IndustryUpdateView, \
    IndustryDelView, IndustryWageView, IndustryWageAddView, IndustryWageUpdateView, IndustryWageDelView, \
    ResIncomeExpendView, ResIncomeExpendAddView, ResIncomeExpendUpdateView, ResIncomeExpendDelView

urlpatterns = [
    # 计算器维护
    url(r'^cal_panel/$', CalculatorPanelView.as_view(), name="calc-panel"),
    url(r'^inc_exp_item/$', IncomeExpendItemView.as_view(), name="income-expend-item"),
    url(r'^inc_exp_item_add/$', IncomeExpendItemAddView.as_view(), name="income-expend-item-add"),
    url(r'^inc_exp_item_update/(?P<pk>\d+)/$', IncomeExpendItemUpdateView.as_view(), name="income-expend-item-update"),
    url(r'^inc_exp_item_del/(?P<pk>\d+)/$', IncomeExpendItemDelView.as_view(), name="income-expend-item-del"),

    url(r'^industry/$', IndustryView.as_view(), name="industry-list"),
    url(r'^industry_add/$', IndustryAddView.as_view(), name="industry-add"),
    url(r'^industry_update/(?P<pk>\d+)/$', IndustryUpdateView.as_view(), name="industry-update"),
    url(r'^industry_del/(?P<pk>\d+)/$', IndustryDelView.as_view(), name="industry-del"),

    url(r'^industry_wage/$', IndustryWageView.as_view(), name="industry-wage-list"),
    url(r'^industry_wage_add/$', IndustryWageAddView.as_view(), name="industry-wage-add"),
    url(r'^industry_wage_update/(?P<pk>\d+)/$', IndustryWageUpdateView.as_view(), name="industry-wage-update"),
    url(r'^industry_wage_del/(?P<pk>\d+)/$', IndustryWageDelView.as_view(), name="industry-wage-del"),

    url(r'^income_expend/$', ResIncomeExpendView.as_view(), name="income-expend-list"),
    url(r'^income_expend_add/$', ResIncomeExpendAddView.as_view(), name="income-expend-add"),
    url(r'^income_expend_update/(?P<pk>\d+)/$', ResIncomeExpendUpdateView.as_view(), name="income-expend-update"),
    url(r'^income_expend_del/(?P<pk>\d+)/$', ResIncomeExpendDelView.as_view(), name="income-expend-del"),

]
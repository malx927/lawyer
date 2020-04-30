# coding = utf-8
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from calculator.forms import IncomeExpendItemForm, IndustryForm, IndustryWageForm, IncomeExpendForm
from calculator.models import IncomeExpendItem, Industry, IndusAverWage, AreaCode, ResIncomeExpend
from lawyer import settings
from rbac.utils import get_menu_children


class CalculatorPanelView(View):
    """计算维护功能面板"""
    def get(self, request, *args, **kwargs):

        children_menus = get_menu_children(request)

        return render(request, template_name="calculator/calculator_panel.html", context={"children_menus": children_menus})

    def post(self, request, *args, **kwargs):
        pass


class IncomeExpendItemView(View):
    """居民人均收入列表"""
    def get(self, request, *args, **kwargs):
        inc_exp_items = IncomeExpendItem.objects.all()

        context = {
            "inc_exp_items": inc_exp_items
        }
        return render(request, template_name="calculator/income_expend_item_list.html", context=context)


class IncomeExpendItemAddView(View):
    """居民人均收入增加"""
    def get(self, request, *args, **kwargs):

        form = IncomeExpendItemForm()

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/income_expend_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = IncomeExpendItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:income-expend-item"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/income_expend_add.html", context=context)


class IncomeExpendItemUpdateView(View):
    """居民人均收入修改"""
    def get(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = IncomeExpendItem.objects.filter(pk=pk).first()

        form = IncomeExpendItemForm(instance=obj)

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/income_expend_add.html", context=context)

    def post(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = IncomeExpendItem.objects.filter(pk=pk).first()

        form = IncomeExpendItemForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:income-expend-item"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/income_expend_add.html", context=context)


class IncomeExpendItemDelView(View):
    """居民人均收入删除"""
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        IncomeExpendItem.objects.filter(pk=pk).delete()
        return redirect(reverse("calc-mgr:income-expend-item"))


class IndustryView(View):
    """行业管理列表"""
    def get(self, request, *args, **kwargs):
        industries = Industry.objects.all()

        context = {
            "industries": industries
        }
        return render(request, template_name="calculator/industry_list.html", context=context)


class IndustryAddView(View):
    """行业管理增加"""
    def get(self, request, *args, **kwargs):

        form = IndustryForm()

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/industry_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = IndustryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:industry-list"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/industry_add.html", context=context)


class IndustryUpdateView(View):
    """行业管理修改"""
    def get(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = Industry.objects.filter(pk=pk).first()

        form = IndustryForm(instance=obj)

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/industry_add.html", context=context)

    def post(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = Industry.objects.filter(pk=pk).first()

        form = IndustryForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:industry-list"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/industry_add.html", context=context)


class IndustryDelView(View):
    """行业管理删除"""
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        Industry.objects.filter(pk=pk).delete()
        return redirect(reverse("calc-mgr:industry-list"))


class IndustryWageView(View):
    """行业平均工资列表"""
    def get(self, request, *args, **kwargs):

        province = request.GET.get("province", None)
        industry = request.GET.get("industry", None)
        year = request.GET.get("year", None)
        aver_wages = IndusAverWage.objects.all()
        if province:
            aver_wages = aver_wages.filter(province_id=province)

        if industry:
            aver_wages = aver_wages.filter(industry_id=int(industry))

        if year:
            aver_wages = aver_wages.filter(years=int(year))

        provinces = AreaCode.objects.extra(where=['length(code)=2'])
        industries = Industry.objects.all()

        context = {
            "aver_wages": aver_wages,
            "provinces": provinces,
            "industries": industries,
            "province": province if province else "",
            "industry": int(industry) if industry else "",
            "year": year if year else "",
        }
        return render(request, template_name="calculator/industry_wage_list.html", context=context)


class IndustryWageAddView(View):
    """行业平均工资增加"""
    def get(self, request, *args, **kwargs):

        form = IndustryWageForm()

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/industry_wage_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = IndustryWageForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:industry-wage-list"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/industry_wage_add.html", context=context)


class IndustryWageUpdateView(View):
    """行业平均工资修改"""
    def get(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = IndusAverWage.objects.filter(pk=pk).first()

        form = IndustryWageForm(instance=obj)

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/industry_wage_add.html", context=context)

    def post(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = IndusAverWage.objects.filter(pk=pk).first()

        form = IndustryWageForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:industry-wage-list"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/industry_wage_add.html", context=context)


class IndustryWageDelView(View):
    """行业平均工资删除"""
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        IndusAverWage.objects.filter(pk=pk).delete()
        return redirect(reverse("calc-mgr:industry-wage-list"))


class ResIncomeExpendView(View):
    """居民人均收支情况表"""
    def get(self, request, *args, **kwargs):

        province = request.GET.get("province", None)
        inc_exp_item = request.GET.get("inc_exp_item", None)
        year = request.GET.get("year", None)
        income_expends = ResIncomeExpend.objects.all()
        if province:
            income_expends = income_expends.filter(province_id=province)

        if inc_exp_item:
            income_expends = income_expends.filter(inc_exp_item_id=int(inc_exp_item))

        if year:
            income_expends = income_expends.filter(years=int(year))

        provinces = AreaCode.objects.extra(where=['length(code)=2'])
        income_expend_items = IncomeExpendItem.objects.all()

        context = {
            "income_expends": income_expends,
            "provinces": provinces,
            "income_expend_items": income_expend_items,
            "province": province if province else "",
            "inc_exp_item": int(inc_exp_item) if inc_exp_item else "",
            "year": year if year else "",
        }
        return render(request, template_name="calculator/income_expend_list.html", context=context)


class ResIncomeExpendAddView(View):
    """居民人均收支增加"""
    def get(self, request, *args, **kwargs):

        form = IncomeExpendForm()

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/res_income_expend_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = IncomeExpendForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:income-expend-list"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/res_income_expend_add.html", context=context)


class ResIncomeExpendUpdateView(View):
    """居民人均收支修改"""
    def get(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = ResIncomeExpend.objects.filter(pk=pk).first()

        form = IncomeExpendForm(instance=obj)

        context = {
            "form": form,
            "action": request.get_full_path()
        }
        return render(request, template_name="calculator/include/res_income_expend_add.html", context=context)

    def post(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        obj = ResIncomeExpend.objects.filter(pk=pk).first()

        form = IncomeExpendForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(reverse("calc-mgr:income-expend-list"))
        else:
            context = {
                "form": form
            }
            return render(request, template_name="calculator/include/res_income_expend_add.html", context=context)


class ResIncomeExpendDelView(View):
    """居民人均收支删除"""
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        ResIncomeExpend.objects.filter(pk=pk).delete()
        return redirect(reverse("calc-mgr:income-expend-list"))
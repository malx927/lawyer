#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from django.forms import inlineformset_factory

from calculator.constants import DISABILITY_TYPE, RELATION_TYPE, SEC_DISABILITY_TYPE, SUPPORTED_TYPE
from calculator.models import SupportedPerson, CalculatorUser, RelationPerson, IncomeExpendItem, Industry, \
    IndusAverWage, AreaCode, ResIncomeExpend


class DisabilityForm(forms.Form):
    """次级伤残"""
    id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    name = forms.ChoiceField(
        choices=SEC_DISABILITY_TYPE,
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CalculatorUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CalculatorUser
        fields = ["name"]


SupportedFormSet = inlineformset_factory(
                    CalculatorUser,
                    SupportedPerson,
                    fields=('relation_type', 'action_ability', "is_income", "relation_age"),
                    widgets={
                        "relation_type": forms.Select(attrs={'class': "form-control"}),
                        "action_ability": forms.Select(attrs={'class': "form-control"}),
                        "is_income": forms.Select(attrs={'class': "form-control"}),
                        "relation_age": forms.NumberInput(attrs={'class': "form-control"}),
                    },
                    extra=1,
                )
RelationFormSet = inlineformset_factory(
                    CalculatorUser,
                    RelationPerson,
                    fields=('relation_type', 'action_ability', "is_income", "relation_age"),
                    widgets={
                        "relation_type": forms.Select(attrs={'class': "form-control"}),
                        "action_ability": forms.Select(attrs={'class': "form-control"}),
                        "is_income": forms.Select(attrs={'class': "form-control"}),
                        "relation_age": forms.NumberInput(attrs={'class': "form-control"}),
                    },
                    extra=1,
                )


class IncomeExpendItemForm(forms.ModelForm):
    class Meta:
        model = IncomeExpendItem
        fields = ["name"]

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入项目名称'}),
        }


class IndustryForm(forms.ModelForm):
    """行业管理"""
    class Meta:
        model = Industry
        fields = ["name", "standard"]

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入项目名称'}),
            'standard': forms.Select(attrs={'class': "form-control" }),
        }


class IndustryWageForm(forms.ModelForm):
    """行业在岗职工平均工资"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].choices = [("", "--------")]
        self.fields['province'].choices += AreaCode.objects.extra(where=['length(code)=2']).values_list('code', 'name')

    class Meta:
        model = IndusAverWage
        fields = ["province", "industry", "years", "aver_wage", "day_aver_wage"]
        widgets = {
            'province': forms.Select(attrs={'class': "form-control"}),
            'industry': forms.Select(attrs={'class': "form-control"}),
            'years': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入年份'}),
            'aver_wage': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入平均工资'}),
            'day_aver_wage': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入平均日工资'}),
        }


class IncomeExpendForm(forms.ModelForm):
    """行业在岗职工平均工资"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].choices = [("", "--------")]
        self.fields['province'].choices += AreaCode.objects.extra(where=['length(code)=2']).values_list('code', 'name')

    class Meta:
        model = ResIncomeExpend
        fields = ["province", "inc_exp_item", "years", "total_money"]
        widgets = {
            'province': forms.Select(attrs={'class': "form-control"}),
            'inc_exp_item': forms.Select(attrs={'class': "form-control"}),
            'years': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入年份'}),
            'total_money': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入总金额'}),
        }
# class SupportedForm(forms.Form):
#     """被抚(扶)养人"""
#     id = forms.IntegerField(
#         widget=forms.HiddenInput(),
#         required=False
#     )
#     relation_type = forms.ChoiceField(
#         choices=SUPPORTED_TYPE,
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#     action_ability = forms.ChoiceField(
#         choices=(
#             (None, '----'),
#             (1, '有'),
#             (0, '无'),
#         ),
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#
#     is_income = forms.ChoiceField(
#         choices=(
#             (None, '----'),
#             (1, '有'),
#             (0, '无'),
#         ),
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#     relation_age = forms.IntegerField(
#         widget=forms.TextInput(attrs={'class': "form-control"}),
#         required=False,
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#
# class RelationForm(forms.Form):
#     """直系亲属信息"""
#     id = forms.IntegerField(
#         widget=forms.HiddenInput(),
#         required=False
#     )
#     relation_type = forms.ChoiceField(
#         choices=RELATION_TYPE,
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#     action_ability = forms.ChoiceField(
#         choices=(
#             (None, '----'),
#             (1, '有'),
#             (0, '无'),
#         ),
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#
#     is_income = forms.ChoiceField(
#         choices=(
#             (None, '----'),
#             (1, '有'),
#             (0, '无'),
#         ),
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#     relation_age = forms.IntegerField(
#         widget=forms.TextInput(attrs={'class': "form-control"}),
#         required=False,
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
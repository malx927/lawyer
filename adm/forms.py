#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from django.forms import inlineformset_factory

from adm.models import Office, SpecialField, ProfessionalTitle, SocialService
from rbac.models import UserInfo


class OfficeForm(forms.ModelForm):

    class Meta:
        model = Office
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入律所名称'}),
            'credit_code': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入统一社会信用代码'}),
            'address': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入律所所在市'}),
            'category': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择律师类型'}),
            'legal_person': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法定代表人'}),
            'telephone': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入联系电话'}),
            'position': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入所在地'}),
            'bank': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入开户行'}),
            'account': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入账号'}),
        }


class UserChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_update"].initial = True

    class Meta:
        model = UserInfo
        fields = [
            "real_name", "gender", "post", "telephone", "job", "job_time", "license_num", "prof_title", "is_update"
        ]
        widgets = {
            'real_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入姓名'}),
            'gender': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择性别'}),
            'telephone': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入手机号码'}),
            'post': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择类型'}),
            'job': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入职务'}),
            'job_time': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入执业时间'}),
            'license_num': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入律师证号'}),
            'prof_title': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入律师职称'}),
            'is_update': forms.HiddenInput(),
        }


SpecialFormSet = inlineformset_factory(
                    UserInfo,
                    SpecialField,
                    fields=('title',),
                    widgets={"title": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入优势类型'})},
                    extra=1, can_delete=True
                )
ProfessionalFormSet = inlineformset_factory(
                    UserInfo,
                    ProfessionalTitle,
                    fields=('title',),
                    widgets={"title": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入职称'})},
                    extra=1, can_delete=True
                )
SocialFormSet = inlineformset_factory(
                    UserInfo,
                    SocialService,
                    fields=('title',),
                    widgets={"title": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入职位名称'})},
                    extra=1, can_delete=True
                )


# -*- coding:utf-8 -*-
from django import forms
from django.forms import inlineformset_factory

from baseinfo.models import CivilLevel, LegalStatus
from civilcase.models import Civil, CivilDetail, CivilNaturePerson, CivilLegalPerson, CivilLawsuitScheme, EvidenceList, \
    AskingOutline, CivilCompensate, Applications, CivilHisResult
from rbac.models import UserInfo
from django.forms import BaseInlineFormSet


class CivilCaseForm(forms.ModelForm):
    """民事案件"""
    def __init__(self, *args, **kwargs):
        super(CivilCaseForm, self).__init__(*args, **kwargs)
        self.fields['commission_stage'].queryset = CivilLevel.objects.all()

    class Meta:
        model = Civil
        fields = "__all__"

        widgets = {
            'case_id': forms.TextInput(attrs={'class': "form-control", 'placeholder': '案件编号', "readonly": "true"}),
            'case_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入案件名称'}),
            'info_type': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择信息类型'}),
            'case_prop': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择案件性质'}),
            'agent': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择代理权限'}),
            'org_legal_status': forms.Select(attrs={'class': "form-control", 'placeholder': '原审法律地位'}),
            'case_stage': forms.Select(attrs={'class': "form-control", 'placeholder': '案件执行阶段'}),
            'commission_stage': forms.CheckboxSelectMultiple(attrs={'class': "checkbox list-inline"}),
            'agent_type': forms.Select(attrs={'class': "form-control", 'placeholder': '代理种类'}),
            'total_expenses': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入代理费'}),
            'target_amount': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入标的额'}),
            'per_target_amount': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入收费比例'}),
            'pre_expenses': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入先期费用'}),
            'case_brief': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '案由', "rows": "4"}),
            # 委托人信息(自然人)
            'cli_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入委托人姓名'}),
            'cli_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入委托人电话'}),
            'cli_relation': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入与当事人关系'}),
            'cli_address': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入住址'}),
            'cli_id_card': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入身份证号'}),
            # 委托人信息(法人)
            'cli_legal_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公司名称'}),
            'cli_legal_person': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法定代表人'}),
            'cli_legal_address': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入住所地'}),
            'cli_legal_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公司联系电话'}),
            'cli_legal_code': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入统一社会信用代码'}),
            'cli_legal_job': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公司所处职务'}),
            # 监护人
            'guard_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入监护人姓名'}),
            'guard_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入监护人电话'}),
            'guard_relation': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入与当事人关系'}),
            'guard_address': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入住址'}),
            'guard_id_card': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入身份证号'}),
            # 当事人信息(自然人)
            'party_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入当事人姓名'}),
            'party_person_status': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择所处法律地位'}),
            'party_sex': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择性别'}),
            'party_birth': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入出生日期'}),
            'party_nation': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入民族'}),
            'party_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入联系电话'}),
            'party_id_code': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入身份证号'}),
            'party_address': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入住址'}),
            'party_job': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入职业'}),
            # 当事人信息(法人信息)
            'party_legal_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公司名称'}),
            'party_company_status': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择所处法律地位'}),
            'party_legal_person': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法定代表人'}),
            'party_legal_job': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入职务'}),
            'party_legal_address': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入住所地'}),
            'party_legal_telephone': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公司联系电话'}),
            'party_legal_code': forms.TextInput(attrs={'class': "form-control", 'placeholder': '统一社会信用代码'}),
            # 分配律师
            'lawyer': forms.HiddenInput(attrs={'class': "form-control"}),
            'assist': forms.HiddenInput(attrs={'class': "form-control"}),
            'manager': forms.HiddenInput(attrs={'class': "form-control"}),
        }


class HisResultForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # experiment = kwargs.pop('experiment')
        super().__init__(*args, **kwargs)
        self.fields["stage"].queryset = CivilLevel.objects.filter(id__lt=4)
        self.fields["legal_status"].queryset = LegalStatus.objects.filter(id__lt=7)

    class Meta:
        model = CivilHisResult
        fields = ('stage', 'legal_status', 'court_name', 'judge_date', 'judge_code', 'judge_result', 'judge_manner')


HisResultFormSet = inlineformset_factory(
                    Civil,
                    CivilHisResult,
                    form=HisResultForm,
                    fields=('stage', 'legal_status', 'court_name', 'judge_date', 'judge_code', 'judge_result', 'judge_manner'),
                    widgets={
                        "stage": forms.Select(attrs={'class': "form-control"}),
                        "legal_status": forms.Select(attrs={'class': "form-control"}),
                        "court_name": forms.TextInput(attrs={'class': "form-control", "placeholder": "判决法院"}),
                        "judge_date": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决时间'}),
                        "judge_code": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决书编号'}),
                        "judge_result": forms.Select(attrs={'class': "form-control"}),
                        "judge_manner": forms.Select(attrs={'class': "form-control"}),
                    },
                    extra=1, can_delete=True, max_num=4
                )


class CivilLawyerForm(forms.ModelForm):
    """民事案件分配律师"""
    def __init__(self, *args, **kwargs):
        super(CivilLawyerForm, self).__init__(*args, **kwargs)
        self.fields["lawyer"].queryset = UserInfo.objects.filter(id__lt=4)
        self.fields["assist"].queryset = UserInfo.objects.filter(id__lt=4)
        self.fields["manager"].queryset = UserInfo.objects.filter(id__gte=4)

    class Meta:
        model = Civil
        fields = ["id", "lawyer", "assist", "manager", "is_assign"]

        widgets = {
            # 分配律师
            'lawyer': forms.Select(attrs={'class': "form-control"}),
            'assist': forms.Select(attrs={'class': "form-control"}),
            'manager': forms.Select(attrs={'class': "form-control"}),
            'is_assign': forms.Select(attrs={'class': "form-control"}),
        }


class CivilDetailForm(forms.ModelForm):
    """民事案件执行"""
    def __init__(self, *args, **kwargs):
        super(CivilDetailForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CivilDetail
        fields = "__all__"

        widgets = {
            'civil': forms.Select(attrs={'class': "form-control"}),
            'legal_status': forms.Select(attrs={'class': "form-control", 'placeholder': '当事人法律地位'}),
            'stage': forms.Select(attrs={'class': "form-control", 'placeholder': '案件执行阶段'}),
            'court_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法院名称'}),
            'court_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法院电话'}),
            'court_judge': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法官'}),
            'judge_date': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决时间'}),
            'judge_code': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决书编号'}),
            'judge_result': forms.Textarea(attrs={'class': "form-control", 'placeholder': '请输入判决结果', "rows": "2"}),
            'status': forms.Select(attrs={'class': "form-control"}),
        }


NaturePersonFormSet = inlineformset_factory(
                    CivilDetail,
                    CivilNaturePerson,
                    fields=('name', 'legal_status', 'gender', 'age', 'nation', 'tel', 'id_code', 'address'),
                    widgets={
                        "name": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入姓名'}),
                        "legal_status": forms.Select(attrs={'class': "form-control"}),
                        "gender": forms.Select(attrs={'class': "form-control"}),
                        "age": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入年龄'}),
                        "nation": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入民族'}),
                        "tel": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入联系电话'}),
                        "id_code": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入身份证号'}),
                        "address": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入现住址'}),
                    },
                    extra=1, can_delete=True
                )

LegalPersonFormSet = inlineformset_factory(
                    CivilDetail,
                    CivilLegalPerson,
                    fields=('company_name', 'legal_status', 'credit_code', 'legal_person', 'telephone', 'address', 'job'),
                    widgets={
                        "company_name": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公司名称'}),
                        "legal_status": forms.Select(attrs={'class': "form-control"}),
                        "credit_code": forms.TextInput(attrs={'class': "form-control", 'placeholder': '统一社会信用代码'}),
                        "legal_person": forms.TextInput(attrs={'class': "form-control", 'placeholder': '法定代表人'}),
                        "telephone": forms.TextInput(attrs={'class': "form-control", 'placeholder': '联系电话'}),
                        "address": forms.TextInput(attrs={'class': "form-control", 'placeholder': '住所地'}),
                        "job": forms.TextInput(attrs={'class': "form-control", 'placeholder': '职务'}),
                    },
                    extra=1, can_delete=True
                )


class CivilCaseSchemeForm(forms.ModelForm):
    """民事案件诉讼方案"""
    case_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.case_type = kwargs.pop("case_type", None)
        super(CivilCaseSchemeForm, self).__init__(*args, **kwargs)
        if self.case_type == "first_demandant":
            self.fields["counterclaim_ask"].widget = forms.HiddenInput()
            self.fields["counterclaim_reasons"].widget = forms.HiddenInput()
            self.fields["pleadings"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_type == "first_defendant":
            self.fields["complaint_claim"].widget = forms.HiddenInput()
            self.fields["complaint_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_answer"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_type == "second_appeal":
            self.fields["complaint_claim"].widget = forms.HiddenInput()
            self.fields["complaint_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_answer"].widget = forms.HiddenInput()
            self.fields["pleadings"].widget = forms.HiddenInput()
            self.fields["counterclaim_ask"].widget = forms.HiddenInput()
            self.fields["counterclaim_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_type == "second_appealed":
            self.fields["complaint_claim"].widget = forms.HiddenInput()
            self.fields["complaint_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_answer"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_ask"].widget = forms.HiddenInput()
            self.fields["counterclaim_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_type == "retrial_apply":
            self.fields["complaint_claim"].widget = forms.HiddenInput()
            self.fields["complaint_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_answer"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_ask"].widget = forms.HiddenInput()
            self.fields["counterclaim_reasons"].widget = forms.HiddenInput()
            self.fields["pleadings"].widget = forms.HiddenInput()
        elif self.case_type == "retrial_applied":
            self.fields["complaint_claim"].widget = forms.HiddenInput()
            self.fields["complaint_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_answer"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["counterclaim_ask"].widget = forms.HiddenInput()
            self.fields["counterclaim_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()

    class Meta:
        model = CivilLawsuitScheme
        fields = "__all__"

        widgets = {
            'civil_detail': forms.Select(attrs={'class': "form-control"}),
            'complaint_claim': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '诉讼请求', "rows": "4"}),
            'complaint_reasons': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '事实和理由', "rows": "4"}),
            'statement': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '代理意见', "rows": "4"}),
            'counterclaim_answer': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '反诉答辩意见', "rows": "4"}),
            'counterclaim_ask': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '反诉请求', "rows": "4"}),
            'counterclaim_reasons': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '事实和理由', "rows": "4"}),
            'pleadings': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '答辩意见', "rows": "4"}),
            'appeal_claim': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '上诉请求', "rows": "4"}),
            'appeal_reasons': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '事实和理由', "rows": "4"}),
            'retrialapply_claim': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '诉讼请求', "rows": "4"}),
            'retrialapply_reasons': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '事实和理由', "rows": "4"}),

        }


# 证据目录
EvidenceListFormSet = inlineformset_factory(
                    CivilLawsuitScheme,
                    EvidenceList,
                    fields=('evi_name', 'evi_type', 'evi_source', 'evi_purpose'),
                    widgets={
                        "evi_name": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入证据名称'}),
                        "evi_type": forms.Select(attrs={'class': "form-control"}),
                        "evi_source": forms.Select(attrs={'class': "form-control"}),
                        "evi_purpose": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入证据目的'}),
                    },
                    extra=1, can_delete=True
                )


class CustomInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            case_detail_id = form.instance.scheme.civil_detail_id
            result = CivilNaturePerson.objects.filter(case_id=case_detail_id).values_list("name", "name")
            result = list(result)
            result.insert(0, ('', '---------'))
            form.fields["ask_user"].widget.choices = result


# 询问提纲
AskingOutlineFormSet = inlineformset_factory(
                    CivilLawsuitScheme,
                    AskingOutline,
                    formset=CustomInlineFormSet,
                    fields=('target', 'ask_user', 'content'),
                    widgets={
                        "target": forms.Select(attrs={'class': "form-control"}),
                        "ask_user": forms.Select(attrs={'class': "form-control"}),
                        "content": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入询问内容'}),
                    },
                    extra=1, can_delete=True
                )

# 赔偿明细
CompensateFormSet = inlineformset_factory(
                    CivilLawsuitScheme,
                    CivilCompensate,
                    fields=('content',),
                    widgets={
                        "content": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入赔偿内容'}),
                    },
                    extra=1, can_delete=True
                )

# 所需申请书
ApplicationsFormSet = inlineformset_factory(
                    CivilLawsuitScheme,
                    Applications,
                    fields=('appli_name',),
                    widgets={
                        "appli_name": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入所需申请书'}),
                    },
                    extra=1, can_delete=True
                )


# class CivilLawyerForm(forms.ModelForm):
#     """民事案件分配"""
#     def __init__(self, *args, **kwargs):
#         super(CivilLawyerForm, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = CivilLawyer
#         fields = "__all__"
#
#         widgets = {
#             'case': forms.Select(attrs={'class': "form-control"}),
#             'lawyer': forms.Select(attrs={'class': "form-control"}),
#             'assist': forms.Select(attrs={'class': "form-control"}),
#             'manager': forms.Select(attrs={'class': "form-control"}),
#             'confirm': forms.Select(attrs={'class': "form-control"}),
#         }

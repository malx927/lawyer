
# -*- coding:utf-8 -*-
from django import forms
from django.forms import inlineformset_factory

from crimicase.models import Criminal, CriminalDetail, CrimiNaturePerson, CrimiLegalPerson, CrimiLawsuitScheme, \
    CrimiEvidence, CrimiAskingOutline, CrimiApplications, CriminalHisResult
from rbac.models import UserInfo


class CrimiCaseForm(forms.ModelForm):
    """刑事案件"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['commission_stage'].queryset = CivilLevel.objects.all()

    class Meta:
        model = Criminal
        fields = "__all__"

        widgets = {
            'case_id': forms.TextInput(attrs={'class': "form-control", 'placeholder': '案件编号', "readonly": "true"}),
            'case_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入案件名称'}),
            'accusation': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入所涉罪名'}),
            'info_type': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择信息类型'}),
            'case_prop': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择案件性质'}),
            'enforce_way': forms.Select(attrs={'class': "form-control", 'placeholder': '请选择强制措施'}),
            'detain_time': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入拘留时间'}),
            'arrest_time': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入批捕时间'}),
            'detention_place': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入羁押地点'}),
            'org_legal_status': forms.Select(attrs={'class': "form-control", 'placeholder': '原审法律地位'}),
            'stage': forms.Select(attrs={'class': "form-control", 'placeholder': '案件执行阶段'}),
            'commission_stage': forms.CheckboxSelectMultiple(attrs={'class': "checkbox list-inline"}),
            'total_expenses': forms.NumberInput(attrs={'class': "form-control", 'placeholder': '请输入代理费'}),
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


HisResultFormSet = inlineformset_factory(
                    Criminal,
                    CriminalHisResult,
                    fields=('stage', 'court_name', 'judge_date', 'judge_code', 'judge_result', 'judge_manner'),
                    widgets={
                        "stage": forms.Select(attrs={'class': "form-control"}),
                        "court_name": forms.TextInput(attrs={'class': "form-control", "placeholder": "判决法院"}),
                        "judge_date": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决时间'}),
                        "judge_code": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决书编号'}),
                        "judge_result": forms.Select(attrs={'class': "form-control"}),
                        "judge_manner": forms.Select(attrs={'class': "form-control"}),
                    },
                    extra=1, can_delete=True, max_num=4
                )


class CriminalDetailForm(forms.ModelForm):
    """刑事案件执行"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CriminalDetail
        fields = "__all__"

        widgets = {
            'criminal': forms.Select(attrs={'class': "form-control"}),
            'legal_status': forms.Select(attrs={'class': "form-control", 'placeholder': '法律地位'}),
            'stage': forms.Select(attrs={'class': "form-control", 'placeholder': '执行阶段'}),
            'police_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公安名称'}),
            'police_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入公安电话'}),
            'police_person': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入联系人'}),
            'procuracy_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入检察院名称'}),
            'procuracy_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入检察院电话'}),
            'procuracy_person': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入联系人'}),
            'procuracy_result': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入审查结果'}),
            'court_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法院名称'}),
            'court_tel': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法院电话'}),
            'court_judge': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入法官'}),
            'judge_date': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决时间'}),
            'judge_code': forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入判决书编号'}),
            'judge_result': forms.Textarea(attrs={'class': "form-control", 'placeholder': '请输入判决结果', "rows": "2"}),
            'status': forms.Select(attrs={'class': "form-control"}),
        }


CrimiNaturePersonFormSet = inlineformset_factory(
                    CriminalDetail,
                    CrimiNaturePerson,
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

CrimiLegalPersonFormSet = inlineformset_factory(
                    CriminalDetail,
                    CrimiLegalPerson,
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


class CrimiCaseSchemeForm(forms.ModelForm):
    """刑事案件诉讼方案"""
    case_stage = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.case_stage = kwargs.pop("case_stage", None)
        super().__init__(*args, **kwargs)
        if self.case_stage == 1:     # 侦查阶段
            self.fields["no_arrest_opinion"].widget = forms.HiddenInput()
            self.fields["detain_reason"].widget = forms.HiddenInput()
            self.fields["defense_opinion"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_stage == 2:   # 审查起诉阶段
            self.fields["defense_opinion"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_stage == 3:       # 一审
            self.fields["legal_opinion"].widget = forms.HiddenInput()
            self.fields["no_arrest_opinion"].widget = forms.HiddenInput()
            self.fields["detain_reason"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_stage == 4:       # 二审
            self.fields["legal_opinion"].widget = forms.HiddenInput()
            self.fields["bail_reasons"].widget = forms.HiddenInput()
            self.fields["no_arrest_opinion"].widget = forms.HiddenInput()
            self.fields["detain_reason"].widget = forms.HiddenInput()
            self.fields["retrialapply_claim"].widget = forms.HiddenInput()
            self.fields["retrialapply_reasons"].widget = forms.HiddenInput()
        elif self.case_stage == 5:       # 再审
            self.fields["legal_opinion"].widget = forms.HiddenInput()
            self.fields["bail_reasons"].widget = forms.HiddenInput()
            self.fields["no_arrest_opinion"].widget = forms.HiddenInput()
            self.fields["detain_reason"].widget = forms.HiddenInput()
            self.fields["appeal_claim"].widget = forms.HiddenInput()
            self.fields["appeal_reasons"].widget = forms.HiddenInput()

    class Meta:
        model = CrimiLawsuitScheme
        fields = "__all__"

        widgets = {
            'criminal_detail': forms.Select(attrs={'class': "form-control"}),
            'legal_opinion': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '法律意见', "rows": "4"}),
            'bail_reasons': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '申请理由', "rows": "4"}),
            'no_arrest_opinion': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '法律意见', "rows": "4"}),
            'detain_reason': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '羁押申请理由', "rows": "4"}),
            'defense_opinion': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '辩护意见', "rows": "4"}),
            'appeal_claim': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '上诉请求', "rows": "4"}),
            'appeal_reasons': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '事实和理由', "rows": "4"}),
            'retrialapply_claim': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '申请事项', "rows": "4"}),
            'retrialapply_reasons': forms.Textarea(attrs={'class': "form-control summernote", 'placeholder': '事实和理由', "rows": "4"}),
        }


# 证据目录
EvidenceFormSet = inlineformset_factory(
                    CrimiLawsuitScheme,
                    CrimiEvidence,
                    fields=('evi_name', 'evi_type', 'evi_source', 'evi_purpose'),
                    widgets={
                        "evi_name": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入证据名称'}),
                        "evi_type": forms.Select(attrs={'class': "form-control"}),
                        "evi_source": forms.Select(attrs={'class': "form-control"}),
                        "evi_purpose": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入证据目的'}),
                    },
                    extra=1, can_delete=True
                )

# 询问提纲
AskingOutlineFormSet = inlineformset_factory(
                    CrimiLawsuitScheme,
                    CrimiAskingOutline,
                    fields=('target', 'content'),
                    widgets={
                        "target": forms.Select(attrs={'class': "form-control"}),
                        "content": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入询问内容'}),
                    },
                    extra=1, can_delete=True
                )


# 所需申请书
ApplicationsFormSet = inlineformset_factory(
                    CrimiLawsuitScheme,
                    CrimiApplications,
                    fields=('appli_name',),
                    widgets={
                        "appli_name": forms.TextInput(attrs={'class': "form-control", 'placeholder': '请输入所需申请书'}),
                    },
                    extra=1, can_delete=True
                )


class CriminalLawyerForm(forms.ModelForm):
    """刑事案件分配律师"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lawyer"].queryset = UserInfo.objects.filter(id__lt=4)
        self.fields["assist"].queryset = UserInfo.objects.filter(id__lt=4)
        self.fields["manager"].queryset = UserInfo.objects.filter(id__gte=4)

    class Meta:
        model = Criminal
        fields = ["id", "lawyer", "assist", "manager", "is_assign"]

        widgets = {
            # 分配律师
            'lawyer': forms.Select(attrs={'class': "form-control"}),
            'assist': forms.Select(attrs={'class': "form-control"}),
            'manager': forms.Select(attrs={'class': "form-control"}),
            'is_assign': forms.Select(attrs={'class': "form-control"}),
        }
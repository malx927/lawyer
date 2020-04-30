import datetime

from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import View

from adm.models import Office
from baseinfo.models import LegalStatus
from crimicivil.forms import CrimiCivilCaseForm, HisResultFormSet, CrimiCivilDetailForm, NaturePersonFormSet, \
    LegalPersonFormSet, CrimiCivilCaseSchemeForm, EvidenceListFormSet, AskingOutlineFormSet, CompensateFormSet, \
    ApplicationsFormSet, CrimiCivilLawyerForm
from crimicivil.models import CrimiCivil, CrimiCivilDetail, CrimiCivilLawsuitScheme


def get_case_type(case_stage, legal_status):
    if case_stage == 1 and legal_status == 1:  # 一审原告
        return "first_demandant"
    elif case_stage == 1 and legal_status == 2:  # 一审被告
        return "first_defendant"
    elif case_stage == 2 and legal_status == 3:  # 二审上诉
        return "second_appeal"
    elif case_stage == 2 and legal_status == 4:  # 二审被上诉
        return "second_appealed"
    elif case_stage == 3 and legal_status == 5:  # 申请再审
        return "retrial_apply"
    elif case_stage == 3 and legal_status == 6:  # 被申请再审
        return "retrial_applied"
    else:
        return None


def get_relative_legal_status(legal_status):
    """获得相对法律地位"""
    if legal_status == 1:  # 一审原告
        return 2
    elif legal_status == 2:  # 一审被告
        return 1
    elif legal_status == 3:  # 二审上诉
        return 4
    elif legal_status == 4:  # 二审被上诉
        return 3
    elif legal_status == 5:  # 申请再审
        return 6
    elif legal_status == 6:  # 被申请再审
        return 5
    else:
        return None


class CrmCivilCaseAddView(View):
    """新建刑附民案件"""
    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", None)
        form = CrimiCivilCaseForm(initial={"lawyer": user_id})
        result_formset = HisResultFormSet()
        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="crimicivil/crmcv_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = CrimiCivilCaseForm(request.POST)
        result_formset = HisResultFormSet(request.POST)
        if form.is_valid() and result_formset.is_valid():
            instance = form.save(commit=False)
            # 设置录入人
            user_id = request.session.get("user_id", None)
            post = request.session.get("post", None)
            if user_id:
                instance.user_id = user_id

            if post:
                if post in [1, 2, 3]:
                    instance.lawyer_id = user_id
                elif post == 4:
                    instance.manager_id = user_id

            instance.save()
            form.save_m2m()
            result_formset.instance = instance
            result_formset.save()
            return redirect(reverse("crmcivil:crmcivil-case-detail", kwargs={"crmcivil_id": instance.id}))

        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="crimicivil/crmcv_case_add.html", context=context)


class CrmCivilCaseUpdateView(View):
    def get(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        crmcivil = get_object_or_404(CrimiCivil, pk=crmcivil_id)
        form = CrimiCivilCaseForm(instance=crmcivil)
        result_formset = HisResultFormSet(instance=crmcivil)

        context = {
            "form": form,
            "result_formset": result_formset,
        }

        return render(request, template_name="crimicivil/crmcv_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        crmcivil = get_object_or_404(CrimiCivil, pk=crmcivil_id)
        form = CrimiCivilCaseForm(request.POST, instance=crmcivil)
        result_formset = HisResultFormSet(request.POST, instance=crmcivil)
        if form.is_valid() and result_formset.is_valid():
            instance = form.save()
            result_formset.save()
            return redirect(reverse("crmcivil:crmcivil-case-stage", kwargs={"crmcivil_id": instance.id}))

        return render(request, template_name="crimicivil/crmcv_case_add.html")


class CrmCivilCaseDeleteView(View):
    """案件删除"""
    def get(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        CrimiCivil.objects.filter(pk=crmcivil_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CrmCivilCaseDetailView(View):
    """刑附民案件执行"""
    def get(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        print(crmcivil_id)
        crmcivil = get_object_or_404(CrimiCivil, pk=crmcivil_id)
        form = CrimiCivilDetailForm()
        nature_person_formset = NaturePersonFormSet()
        legal_person_formset = LegalPersonFormSet()

        context = {
            "form": form,
            "crmcivil": crmcivil,
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="crimicivil/crmcv_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        crmcivil = get_object_or_404(CrimiCivil, pk=crmcivil_id)
        form = CrimiCivilDetailForm(request.POST)
        nature_person_formset = NaturePersonFormSet(request.POST)
        legal_person_formset = LegalPersonFormSet(request.POST)
        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.instance = instance
            nature_person_formset.save()
            legal_person_formset.instance = instance
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("crmcivil:crmcivil-case-update", kwargs={"crmcivil_id": instance.crimicivil_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("crmcivil:crmcivil-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:crmcivil-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "crmcivil": crmcivil,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="crimicivil/crmcv_case_detail.html", context=context)


class CrmCivilCaseStageView(View):
    def get(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        crmcivil = get_object_or_404(CrimiCivil, pk=crmcivil_id)
        crmcivil_details = CrimiCivilDetail.objects.filter(crimicivil_id=crmcivil_id)
        # 存在一审二审等执行阶段
        if crmcivil_details:
            context = {
                "crmcivil": crmcivil,
                "crmcivil_details": crmcivil_details,
            }
            return render(request, template_name="crimicivil/crmcv_case_stage.html", context=context)
        else:
            return redirect(reverse("crmcivil:crmcivil-case-detail", kwargs={"crmcivil_id": crmcivil_id}))

    def post(self, request, *args, **kwargs):
        pass


class CrmCivilCaseDetailUpdateView(View):
    """刑附民案件执行"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=detail_id)

        form = CrimiCivilDetailForm(instance=crmcivil_detail)
        nature_person_formset = NaturePersonFormSet(instance=crmcivil_detail)
        legal_person_formset = LegalPersonFormSet(instance=crmcivil_detail)

        context = {
            "form": form,
            "action": "update",
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="crimicivil/crmcv_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", "")

        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=detail_id)

        form = CrimiCivilDetailForm(request.POST, instance=crmcivil_detail)
        nature_person_formset = NaturePersonFormSet(request.POST, instance=crmcivil_detail)
        legal_person_formset = LegalPersonFormSet(request.POST, instance=crmcivil_detail)

        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.save()
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("crmcivil:crmcivil-case-update", kwargs={"crmcivil_id": instance.crimicivil_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("crmcivil:crmcivil-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:crmcivil-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "action": action,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="crimicivil/crmcv_case_detail.html", context=context)


class CrmCivilCaseDetailDeleteView(View):
    """刑附民案件执行删除"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        CrimiCivilDetail.objects.filter(pk=detail_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CrmCivilCaseDetailSchemeView(View):
    """案件诉讼方案"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        scheme = CrimiCivilLawsuitScheme.objects.select_related("crmcivil_detail").filter(crmcivil_detail_id=detail_id).first()
        context = {}
        if scheme:
            case_stage = scheme.crmcivil_detail.stage.id
            legal_status = scheme.crmcivil_detail.legal_status.id
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = CrimiCivilCaseSchemeForm(instance=scheme, case_type=case_type)
            else:
                form = CrimiCivilCaseSchemeForm(instance=scheme)

            context["action"] = "update"
            context["form"] = form
            evidence_formset = EvidenceListFormSet(instance=scheme)
            asking_formset = AskingOutlineFormSet(instance=scheme)
            compensate_formset = CompensateFormSet(instance=scheme)
            applications_formset = ApplicationsFormSet(instance=scheme)
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        else:
            crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=detail_id)

            case_stage = crmcivil_detail.stage.id
            legal_status = crmcivil_detail.legal_status.id
            print(case_stage, legal_status)
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = CrimiCivilCaseSchemeForm(case_type=case_type)
            else:
                form = CrimiCivilCaseSchemeForm()

            context["action"] = "add"
            context["form"] = form
            context["crmcivil_detail"] = crmcivil_detail
            evidence_formset = EvidenceListFormSet()
            asking_formset = AskingOutlineFormSet()
            compensate_formset = CompensateFormSet()
            applications_formset = ApplicationsFormSet()
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        return render(request, template_name="crimicivil/crmcv_detail_scheme.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", None)

        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=detail_id)
        case_stage = crmcivil_detail.stage.id
        legal_status = crmcivil_detail.legal_status.id
        case_type = get_case_type(case_stage, legal_status)

        if action == "add":
            form = CrimiCivilCaseSchemeForm(request.POST, case_type=case_type)
            evidence_formset = EvidenceListFormSet(request.POST)
            asking_formset = AskingOutlineFormSet(request.POST)
            compensate_formset = CompensateFormSet(request.POST)
            applications_formset = ApplicationsFormSet(request.POST)
            if form.is_valid() and evidence_formset.is_valid() and asking_formset.is_valid() and compensate_formset.is_valid() and applications_formset.is_valid():
                instance = form.save()
                evidence_formset.instance = instance
                evidence_formset.save()
                asking_formset.instance = instance
                asking_formset.save()
                compensate_formset.instance = instance
                compensate_formset.save()
                applications_formset.instance = instance
                applications_formset.save()
                return redirect(reverse("crmcivil:crmcivil-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "crmcivil_detail": crmcivil_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="crimicivil/crmcv_detail_scheme.html", context=context)

        if action == "update":
            scheme = crmcivil_detail.crimicivillawsuitscheme
            form = CrimiCivilCaseSchemeForm(request.POST, instance=scheme, case_type=case_type)
            evidence_formset = EvidenceListFormSet(request.POST, instance=scheme)
            asking_formset = AskingOutlineFormSet(request.POST, instance=scheme)
            compensate_formset = CompensateFormSet(request.POST, instance=scheme)
            applications_formset = ApplicationsFormSet(request.POST, instance=scheme)
            if form.is_valid() and evidence_formset.is_valid() and asking_formset.is_valid() and compensate_formset.is_valid() and applications_formset.is_valid():
                form.save()
                evidence_formset.save()
                asking_formset.save()
                compensate_formset.save()
                applications_formset.save()
                return redirect(reverse("crmcivil:crmcivil-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "crmcivil_detail": crmcivil_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="crimicivil/crmcv_detail_scheme.html", context=context)


class CrmCivilCaseDetailListView(View):
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=detail_id)
        return render(request, template_name="crimicivil/crmcv_case_detail_list.html", context={"crmcivil_detail": crmcivil_detail})


class CrmCivilCaseDistribView(View):
    """刑附民案件分配"""
    def get(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        crimicivil = get_object_or_404(CrimiCivil, pk=crmcivil_id)
        form = CrimiCivilLawyerForm(instance=crimicivil)
        action = request.get_full_path()
        context = {
            "form": form,
            "action": action,
        }

        return render(request, template_name="crimicivil/include/crmcv_case_distrib_form.html", context=context)

    def post(self, request, *args, **kwargs):
        crmcivil_id = kwargs.get("crmcivil_id", None)
        crimicivil = get_object_or_404(CrimiCivil, pk=crmcivil_id)

        form = CrimiCivilLawyerForm(request.POST, instance=crimicivil)

        if form.is_valid():
            form.save()

        return redirect(reverse("adm:case-distrib-list"))


class CrmCivilCasePrintView(View):
    """刑附民案件打印"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        case_stage = crmcivil_detail.stage_id
        legal_status = crmcivil_detail.legal_status_id
        context = {
            "crmcivil_detail": crmcivil_detail,
        }
        if case_stage == 1 and legal_status == 1:
            return render(request, template_name="crimicivil/crmcv_case_first_print.html", context=context)
        elif case_stage == 1 and legal_status == 2:  # 一审被告
            return render(request, template_name="crimicivil/crmcv_case_first_print_1.html", context=context)
        elif case_stage == 2 and legal_status == 3:  # 二审上诉
            return render(request, template_name="crimicivil/crmcv_case_second_print.html", context=context)
        elif case_stage == 2 and legal_status == 4:  # 二审被上诉
            return render(request, template_name="crimicivil/crmcv_case_second_print_1.html", context=context)
        elif case_stage == 3 and legal_status == 5:  # 申请再审
            return render(request, template_name="crimicivil/crmcv_case_retrial_print.html", context=context)
        elif case_stage == 3 and legal_status == 6:  # 被申请再审
            return render(request, template_name="crimicivil/crmcv_case_second_print_1.html", context=context)


class CrmCivilAgentView(View):
    """委托代理协议"""
    def get(self, request, *args, **kwargs):
        crimicivil = get_object_or_404(CrimiCivil, pk=kwargs.get("crmcivil_id"))

        office = Office.objects.first()

        context = {
            "crimicivil": crimicivil,
            "office": office,
        }

        return render(request, template_name="crimicivil/print/crmcv_agent.html", context=context)


class CrmCivilAuthLetterView(View):
    """委托授权书"""
    def get(self, request, *args, **kwargs):
        crimicivil = get_object_or_404(CrimiCivil, pk=kwargs.get("crmcivil_id"))
        office = Office.objects.first()

        context = {
            "crimicivil": crimicivil,
            "office": office,
        }
        return render(request, template_name="crimicivil/print/crmcv_auth_letter.html", context=context)


class CrmCivilLegalRepresCertView(View):
    """法人代表身份证明"""
    def get(self, request, *args, **kwargs):
        crimicivil = get_object_or_404(CrimiCivil, pk=kwargs.get("crmcivil_id"))
        context = {
            "crimicivil": crimicivil,
        }
        return render(request, template_name="crimicivil/print/crmcv_legal_repres_cert.html", context=context)


class CrmCivilComplaintView(View):
    """起诉状"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        natures = crmcivil_detail.natures.exclude(legal_status=7)
        legals = crmcivil_detail.legals.exclude(legal_status=7)
        context = {
            "crmcivil_detail": crmcivil_detail,
            "natures": natures,
            "legals": legals,
        }
        return render(request, template_name="crimicivil/print/crmcv_complaint.html", context=context)


class CrmCivilStatementView(View):
    """代理词"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "crmcivil_detail": crmcivil_detail,
            "office": office,
        }
        return render(request, template_name="crimicivil/print/crmcv_statement.html", context=context)


class CrmCivilProtestView(View):
    """抗诉申请"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        first_trial = crmcivil_detail.crimicivil.crimicivildetail_set.filter(stage_id=1).first()   # 一审
        if not first_trial:
            first_trial = crmcivil_detail.crimicivil.crimicivilhisresult_set.filter(stage_id=1).first()

        context = {
            "crmcivil_detail": crmcivil_detail,
            "office": office,
            "first_trial": first_trial,
        }
        return render(request, template_name="crimicivil/print/crmcv_protest.html", context=context)


class CrmCivilEvidenceListView(View):
    """证据目录"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        evidences = crmcivil_detail.crimicivillawsuitscheme.crimicivilevidence_set.all()
        context = {
            "evidences": evidences,
        }
        return render(request, template_name="crimicivil/print/crmcv_evidence_list.html", context=context)


class CrmCivilCompensateView(View):
    """赔偿明细"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        compensates = crmcivil_detail.crimicivillawsuitscheme.crimicivilcompensate_set.all()
        context = {
            "compensates": compensates,
        }
        return render(request, template_name="crimicivil/print/crmcv_compensate.html", context=context)


class CrmCivilAskingOutlineView(View):
    """询问提纲"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        outlines = crmcivil_detail.crimicivillawsuitscheme.crimicivilaskingoutline_set.all()
        context = {
            "outlines": outlines,
        }
        return render(request, template_name="crimicivil/print/crmcv_asking_outline.html", context=context)


class CrmCivilApplicationView(View):
    """相关申请书"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        applications = crmcivil_detail.crimicivillawsuitscheme.crimicivilapplications_set.all()
        context = {
            "applications": applications,
        }
        return render(request, template_name="crimicivil/print/crmcv_application.html", context=context)


class CrmCivilAppealView(View):
    """上诉状"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        natures = crmcivil_detail.natures.all()
        legals = crmcivil_detail.legals.all()
        first_trial = crmcivil_detail.crimicivil.crimicivildetail_set.filter(stage_id=1).first()   # 一审
        if not first_trial:
            first_trial = crmcivil_detail.crimicivil.crimicivilhisresult_set.filter(stage_id=1).first()

        if first_trial:
            legal_status_id = get_relative_legal_status(first_trial.legal_status_id)
            relative_legal_status = LegalStatus.objects.filter(id=legal_status_id).first()
        else:
            first_trial = None
            relative_legal_status = None

        context = {
            "crmcivil_detail": crmcivil_detail,
            "natures": natures,
            "legals": legals,
            "first_trial": first_trial,
            "relative_legal_status": relative_legal_status,
        }
        return render(request, template_name="crimicivil/print/crmcv_appeal.html", context=context)


class CrmCivilRetrialView(View):
    """再审申请书"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        natures = crmcivil_detail.natures.all()
        legals = crmcivil_detail.legals.all()
        first = crmcivil_detail.crimicivil.crimicivildetail_set.filter(stage_id=1).first()
        if not first:
            first = crmcivil_detail.crimicivil.crimicivilhisresult_set.filter(stage_id=1).first()    # 读取一审历史数据

        second = crmcivil_detail.crimicivil.crimicivildetail_set.filter(stage_id=2).first()

        if not second:
            second = crmcivil_detail.crimicivil.crimicivilhisresult_set.filter(stage_id=2).first()    # 读取二审历史数据

        first_relative_status = None
        second_relative_status = None
        if first:
            f_legal_status = get_relative_legal_status(first.legal_status_id)
            first_relative_status = LegalStatus.objects.filter(id=f_legal_status).first()
        if second:
            s_legal_status = get_relative_legal_status(second.legal_status_id)
            second_relative_status = LegalStatus.objects.filter(id=s_legal_status).first()

        context = {
            "crmcivil_detail": crmcivil_detail,
            "natures": natures,
            "legals": legals,
            "first": first,
            "second": second,
            "first_relative_status": first_relative_status,
            "second_relative_status": second_relative_status,
        }
        return render(request, template_name="crimicivil/print/crmcv_retrial_bill.html", context=context)


class CrmCivilLawyerLetterView(View):
    """律师函"""
    def get(self, request, *args, **kwargs):
        crmcivil_detail = get_object_or_404(CrimiCivilDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "crmcivil_detail": crmcivil_detail,
            "office": office,
        }
        return render(request, template_name="crimicivil/print/crmcv_lawyer_letter.html", context=context)
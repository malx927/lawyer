import datetime

from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import View

from adm.models import Office
from baseinfo.models import LegalStatus, PrivateLegalStatus
from crimiprivate.forms import CrimiPrivateCaseForm, HisResultFormSet, CrimiPrivateDetailForm, NaturePersonFormSet, \
    LegalPersonFormSet, CrimiPrivateSchemeForm, PrivateEvidenceFormSet, PrivateAskingOutlineFormSet, \
    PrivateCompensateFormSet, PrivateApplicationsFormSet, CrimiPrivateLawyerForm
from crimiprivate.models import CrimiPrivate, CrimiPrivateLawsuitScheme, CrimiPrivateDetail


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


class CrimiPrivateCaseAddView(View):
    """新建刑事自诉案件"""
    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", None)
        form = CrimiPrivateCaseForm(initial={"lawyer": user_id})
        result_formset = HisResultFormSet()
        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="crimiprivate/private_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = CrimiPrivateCaseForm(request.POST)
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

            # 设置编号
            if form.cleaned_data["info_type"] == 1:
                case_id = CrimiPrivate.get_max_sn()
                instance.case_id = case_id
            instance.save()
            form.save_m2m()
            result_formset.instance = instance
            result_formset.save()
            return redirect(reverse("private:private-case-detail", kwargs={"private_id": instance.id}))

        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="crimiprivate/private_case_add.html", context=context)


class CrimiPrivateUpdateView(View):
    def get(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)
        private = get_object_or_404(CrimiPrivate, pk=private_id)
        form = CrimiPrivateCaseForm(instance=private)
        result_formset = HisResultFormSet(instance=private)

        context = {
            "form": form,
            "result_formset": result_formset,
        }

        return render(request, template_name="crimiprivate/private_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)
        private = get_object_or_404(CrimiPrivate, pk=private_id)
        form = CrimiPrivateCaseForm(request.POST, instance=private)
        result_formset = HisResultFormSet(request.POST, instance=private)
        if form.is_valid() and result_formset.is_valid():
            instance = form.save(commit=False)
            # 设置编号
            if form.cleaned_data["info_type"] == 1 and not private.case_id:
                case_id = CrimiPrivate.get_max_sn()
                instance.case_id = case_id
            instance.save()
            form.save_m2m()
            result_formset.save()
            return redirect(reverse("private:private-case-stage", kwargs={"private_id": instance.id}))

        return render(request, template_name="crimiprivate/private_case_add.html")


class CrimiPrivateDeleteView(View):
    """案件删除"""
    def get(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)
        CrimiPrivate.objects.filter(pk=private_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CrimiPrivateDetailView(View):
    """刑事自诉案件执行"""
    def get(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)

        private = get_object_or_404(CrimiPrivate, pk=private_id)
        form = CrimiPrivateDetailForm()
        nature_person_formset = NaturePersonFormSet()
        legal_person_formset = LegalPersonFormSet()

        context = {
            "form": form,
            "private": private,
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="crimiprivate/private_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)
        private = get_object_or_404(CrimiPrivate, pk=private_id)
        form = CrimiPrivateDetailForm(request.POST)
        nature_person_formset = NaturePersonFormSet(request.POST)
        legal_person_formset = LegalPersonFormSet(request.POST)
        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.instance = instance
            nature_person_formset.save()
            legal_person_formset.instance = instance
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("private:private-case-update", kwargs={"private_id": instance.private_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("private:private-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:private-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "private": private,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="crimiprivate/private_case_detail.html", context=context)


class CrimiPrivateStageView(View):
    def get(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)
        private = get_object_or_404(CrimiPrivate, pk=private_id)
        private_details = CrimiPrivateDetail.objects.filter(private_id=private_id)
        # 存在一审二审等执行阶段
        if private_details:
            context = {
                "private": private,
                "private_details": private_details,
            }
            return render(request, template_name="crimiprivate/private_case_stage.html", context=context)
        else:
            return redirect(reverse("private:private-case-detail", kwargs={"private_id": private_id}))

    def post(self, request, *args, **kwargs):
        pass


class CrimiPrivateDetailUpdateView(View):
    """刑自案件执行"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=detail_id)

        form = CrimiPrivateDetailForm(instance=private_detail)
        nature_person_formset = NaturePersonFormSet(instance=private_detail)
        legal_person_formset = LegalPersonFormSet(instance=private_detail)

        context = {
            "form": form,
            "action": "update",
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="crimiprivate/private_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", "")

        private_detail = get_object_or_404(CrimiPrivateDetail, pk=detail_id)

        form = CrimiPrivateDetailForm(request.POST, instance=private_detail)
        nature_person_formset = NaturePersonFormSet(request.POST, instance=private_detail)
        legal_person_formset = LegalPersonFormSet(request.POST, instance=private_detail)

        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.save()
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("private:private-case-update", kwargs={"private_id": instance.private_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("private:private-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:private-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "action": action,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="crimiprivate/private_case_detail.html", context=context)


class CrimiPrivateDetailDeleteView(View):
    """刑自案件执行删除"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        CrimiPrivateDetail.objects.filter(pk=detail_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CrimiPrivateDetailSchemeView(View):
    """案件诉讼方案"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        scheme = CrimiPrivateLawsuitScheme.objects.select_related("private_detail").filter(private_detail_id=detail_id).first()
        context = {}
        if scheme:
            case_stage = scheme.private_detail.stage.id
            legal_status = scheme.private_detail.legal_status.id
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = CrimiPrivateSchemeForm(instance=scheme, case_type=case_type)
            else:
                form = CrimiPrivateSchemeForm(instance=scheme)

            context["action"] = "update"
            context["form"] = form
            evidence_formset = PrivateEvidenceFormSet(instance=scheme)
            asking_formset = PrivateAskingOutlineFormSet(instance=scheme)
            compensate_formset = PrivateCompensateFormSet(instance=scheme)
            applications_formset = PrivateApplicationsFormSet(instance=scheme)
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        else:
            private_detail = get_object_or_404(CrimiPrivateDetail, pk=detail_id)

            case_stage = private_detail.stage.id
            legal_status = private_detail.legal_status.id
            print(case_stage, legal_status)
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = CrimiPrivateSchemeForm(case_type=case_type)
            else:
                form = CrimiPrivateSchemeForm()

            context["action"] = "add"
            context["form"] = form
            context["private_detail"] = private_detail
            evidence_formset = PrivateEvidenceFormSet()
            asking_formset = PrivateAskingOutlineFormSet()
            compensate_formset = PrivateCompensateFormSet()
            applications_formset = PrivateApplicationsFormSet()
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        return render(request, template_name="crimiprivate/private_detail_scheme.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", None)

        private_detail = get_object_or_404(CrimiPrivateDetail, pk=detail_id)
        case_stage = private_detail.stage.id
        legal_status = private_detail.legal_status.id
        case_type = get_case_type(case_stage, legal_status)

        if action == "add":
            form = CrimiPrivateSchemeForm(request.POST, case_type=case_type)
            evidence_formset = PrivateEvidenceFormSet(request.POST)
            asking_formset = PrivateAskingOutlineFormSet(request.POST)
            compensate_formset = PrivateCompensateFormSet(request.POST)
            applications_formset = PrivateApplicationsFormSet(request.POST)
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
                return redirect(reverse("private:private-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "private_detail": private_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="crimiprivate/private_detail_scheme.html", context=context)

        if action == "update":
            scheme = private_detail.crimiprivatelawsuitscheme
            form = CrimiPrivateSchemeForm(request.POST, instance=scheme, case_type=case_type)
            evidence_formset = PrivateEvidenceFormSet(request.POST, instance=scheme)
            asking_formset = PrivateAskingOutlineFormSet(request.POST, instance=scheme)
            compensate_formset = PrivateCompensateFormSet(request.POST, instance=scheme)
            applications_formset = PrivateApplicationsFormSet(request.POST, instance=scheme)
            if form.is_valid() and evidence_formset.is_valid() and asking_formset.is_valid() and compensate_formset.is_valid() and applications_formset.is_valid():
                form.save()
                evidence_formset.save()
                asking_formset.save()
                compensate_formset.save()
                applications_formset.save()
                return redirect(reverse("private:private-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "private_detail": private_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="crimiprivate/private_detail_scheme.html", context=context)


class CrimiPrivateDetailListView(View):
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=detail_id)
        return render(request, template_name="crimiprivate/private_case_detail_list.html", context={"private_detail": private_detail})


class CrimiPrivateDistribView(View):
    """刑事自诉案件分配"""
    def get(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)
        private = get_object_or_404(CrimiPrivate, pk=private_id)
        form = CrimiPrivateLawyerForm(instance=private)
        action = request.get_full_path()
        context = {
            "form": form,
            "action": action,
        }

        return render(request, template_name="crimiprivate/include/private_case_distrib_form.html", context=context)

    def post(self, request, *args, **kwargs):
        private_id = kwargs.get("private_id", None)
        private = get_object_or_404(CrimiPrivate, pk=private_id)

        form = CrimiPrivateLawyerForm(request.POST, instance=private)

        if form.is_valid():
            form.save()

        return redirect(reverse("adm:case-distrib-list"))


class CrimiPrivateCasePrintView(View):
    """刑自案件打印"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        case_stage = private_detail.stage_id
        legal_status = private_detail.legal_status_id
        context = {
            "private_detail": private_detail,
        }
        if case_stage == 1 and legal_status == 1:
            return render(request, template_name="crimiprivate/private_case_first_print.html", context=context)
        elif case_stage == 1 and legal_status == 2:  # 一审被告
            return render(request, template_name="crimiprivate/private_case_first_print_1.html", context=context)
        elif case_stage == 2 and legal_status == 3:  # 二审上诉
            return render(request, template_name="crimiprivate/private_case_second_print.html", context=context)
        elif case_stage == 2 and legal_status == 4:  # 二审被上诉
            return render(request, template_name="crimiprivate/private_case_second_print_1.html", context=context)
        elif case_stage == 3 and legal_status == 5:  # 申请再审
            return render(request, template_name="crimiprivate/private_case_retrial_print.html", context=context)
        elif case_stage == 3 and legal_status == 6:  # 被申请再审
            return render(request, template_name="crimiprivate/private_case_second_print_1.html", context=context)


class CrimiPrivateAgentView(View):
    """委托代理协议"""
    def get(self, request, *args, **kwargs):
        private = get_object_or_404(CrimiPrivate, pk=kwargs.get("private_id"))

        office = Office.objects.first()

        context = {
            "private": private,
            "office": office,
        }

        return render(request, template_name="crimiprivate/print/private_agent.html", context=context)


class CrimiPrivateAuthLetterView(View):
    """委托授权书"""
    def get(self, request, *args, **kwargs):
        private = get_object_or_404(CrimiPrivate, pk=kwargs.get("private_id"))
        office = Office.objects.first()

        context = {
            "private": private,
            "office": office,
        }
        return render(request, template_name="crimiprivate/print/private_auth_letter.html", context=context)


class CrimiPrivateLegalRepresCertView(View):
    """法人代表身份证明"""
    def get(self, request, *args, **kwargs):
        private = get_object_or_404(CrimiPrivate, pk=kwargs.get("private_id"))
        context = {
            "private": private,
        }
        return render(request, template_name="crimiprivate/print/private_legal_repres_cert.html", context=context)


class CrimiPrivateComplaintView(View):
    """起诉状"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        natures = private_detail.natures.exclude(legal_status=7)
        legals = private_detail.legals.exclude(legal_status=7)
        context = {
            "private_detail": private_detail,
            "natures": natures,
            "legals": legals,
        }
        return render(request, template_name="crimiprivate/print/private_complaint.html", context=context)


class CrimiPrivateStatementView(View):
    """代理词"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "private_detail": private_detail,
            "office": office,
        }
        return render(request, template_name="crimiprivate/print/private_statement.html", context=context)


class CrimiPrivateEvidenceListView(View):
    """证据目录"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        evidences = private_detail.crimiprivatelawsuitscheme.crimiprivateevidence_set.all()
        context = {
            "evidences": evidences,
        }
        return render(request, template_name="crimiprivate/print/private_evidence_list.html", context=context)


class CrimiPrivateCompensateView(View):
    """赔偿明细"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        compensates = private_detail.crimiprivatelawsuitscheme.crimiprivatecompensate_set.all()
        context = {
            "compensates": compensates,
        }
        return render(request, template_name="crimiprivate/print/private_compensate.html", context=context)


class CrimiPrivateAskingOutlineView(View):
    """询问提纲"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        outlines = private_detail.crimiprivatelawsuitscheme.crimiprivateaskingoutline_set.all()
        context = {
            "outlines": outlines,
        }
        return render(request, template_name="crimiprivate/print/private_asking_outline.html", context=context)


class CrimiPrivateApplicationView(View):
    """相关申请书"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        applications = private_detail.crimiprivatelawsuitscheme.crimiprivateapplications_set.all()
        context = {
            "applications": applications,
        }
        return render(request, template_name="crimiprivate/print/private_application.html", context=context)


class CrimiPrivateAnswerCounterClaimView(View):
    """反诉答辩状"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        context = {
            "private_detail": private_detail,
        }
        return render(request, template_name="crimiprivate/print/private_answer_claim.html", context=context)


class CrimiPrivateCounterClaimView(View):
    """反诉状"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        natures = private_detail.natures.all()
        legals = private_detail.legals.all()
        context = {
            "private_detail": private_detail,
            "natures": natures,
            "legals": legals,
        }
        return render(request, template_name="crimiprivate/print/private_counter_claim.html", context=context)


class CrimiPrivatePleadingsView(View):
    """答辩状"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        context = {
            "private_detail": private_detail,
        }
        return render(request, template_name="crimiprivate/print/private_pleadings.html", context=context)


class CrimiPrivateAppealView(View):
    """上诉状"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        natures = private_detail.natures.all()
        legals = private_detail.legals.all()
        first_trial = private_detail.private.crimiprivatedetail_set.filter(stage_id=1).first()   # 一审
        if not first_trial:
            first_trial = private_detail.private.crimiprivatehisresult_set.filter(stage_id=1).first()

        if first_trial:
            legal_status_id = get_relative_legal_status(first_trial.legal_status_id)
            relative_legal_status = PrivateLegalStatus.objects.filter(id=legal_status_id).first()
        else:
            first_trial = None
            relative_legal_status = None

        context = {
            "private_detail": private_detail,
            "natures": natures,
            "legals": legals,
            "first_trial": first_trial,
            "relative_legal_status": relative_legal_status,
        }
        return render(request, template_name="crimiprivate/print/private_appeal.html", context=context)


class CrimiPrivateRetrialView(View):
    """再审申请书"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        natures = private_detail.natures.all()
        legals = private_detail.legals.all()
        first = private_detail.private.crimiprivatedetail_set.filter(stage_id=1).first()
        if first:
            first.judge_manner = 1

        if not first:
            first = private_detail.private.crimiprivatehisresult_set.filter(stage_id=1).first()    # 读取一审历史数据

        second = private_detail.private.crimiprivatedetail_set.filter(stage_id=2).first()

        if second:
            second.judge_manner = 1

        if not second:
            second = private_detail.private.crimiprivatehisresult_set.filter(stage_id=2).first()    # 读取二审历史数据

        first_relative_status = None
        second_relative_status = None
        if first:
            f_legal_status = get_relative_legal_status(first.legal_status_id)
            first_relative_status = PrivateLegalStatus.objects.filter(id=f_legal_status).first()
        if second:
            s_legal_status = get_relative_legal_status(second.legal_status_id)
            second_relative_status = PrivateLegalStatus.objects.filter(id=s_legal_status).first()

        context = {
            "private_detail": private_detail,
            "natures": natures,
            "legals": legals,
            "first": first,
            "second": second,
            "first_relative_status": first_relative_status,
            "second_relative_status": second_relative_status,
        }
        return render(request, template_name="crimiprivate/print/private_retrial_bill.html", context=context)


class CrimiPrivateLawyerLetterView(View):
    """律师函"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "private_detail": private_detail,
            "office": office,
        }
        return render(request, template_name="crimiprivate/print/private_lawyer_letter.html", context=context)


class CrimiPrivateDefenseOpinionView(View):
    """辩护词"""
    def get(self, request, *args, **kwargs):
        private_detail = get_object_or_404(CrimiPrivateDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()

        context = {
            "private_detail": private_detail,
            "office": office,
        }

        return render(request, template_name="crimiprivate/print/private_defense_opinion.html", context=context)
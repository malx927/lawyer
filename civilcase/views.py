import datetime

from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import View

from adm.models import Office
from baseinfo.models import LegalStatus
from civilcase.forms import CivilCaseForm, CivilDetailForm, NaturePersonFormSet, LegalPersonFormSet, \
    CivilCaseSchemeForm, EvidenceListFormSet, AskingOutlineFormSet, CompensateFormSet, ApplicationsFormSet, \
    CivilLawyerForm, HisResultFormSet
from civilcase.models import Civil, CivilDetail, CivilLawsuitScheme, CivilNaturePerson


# from civilcase.utils import render_to_pdf


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


class CivilCaseAddView(View):
    """新建民事案件"""
    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", None)
        form = CivilCaseForm(initial={"lawyer": user_id})
        result_formset = HisResultFormSet()
        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="civilcase/civil_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = CivilCaseForm(request.POST)
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
            return redirect(reverse("civil-case:civil-case-detail", kwargs={"civil_id": instance.id}))

        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="civilcase/civil_case_add.html", context=context)


class CivilCaseUpdateView(View):
    def get(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        civil = get_object_or_404(Civil, pk=civil_id)
        form = CivilCaseForm(instance=civil)
        result_formset = HisResultFormSet(instance=civil)

        context = {
            "form": form,
            "result_formset": result_formset,
        }

        return render(request, template_name="civilcase/civil_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        civil = get_object_or_404(Civil, pk=civil_id)
        form = CivilCaseForm(request.POST, instance=civil)
        result_formset = HisResultFormSet(request.POST, instance=civil)
        if form.is_valid() and result_formset.is_valid():
            instance = form.save()
            result_formset.save()
            return redirect(reverse("civil-case:civil-case-stage", kwargs={"civil_id": instance.id}))

        return render(request, template_name="civilcase/civil_case_add.html")


class CivilCaseDeleteView(View):
    """案件删除"""
    def get(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        Civil.objects.filter(pk=civil_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CivilCaseDetailView(View):
    """民事案件执行"""
    def get(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        print(civil_id)
        civil = get_object_or_404(Civil, pk=civil_id)
        form = CivilDetailForm()
        nature_person_formset = NaturePersonFormSet()
        legal_person_formset = LegalPersonFormSet()

        context = {
            "form": form,
            "civil": civil,
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="civilcase/civil_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        civil = get_object_or_404(Civil, pk=civil_id)
        form = CivilDetailForm(request.POST)
        nature_person_formset = NaturePersonFormSet(request.POST)
        legal_person_formset = LegalPersonFormSet(request.POST)
        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.instance = instance
            nature_person_formset.save()
            legal_person_formset.instance = instance
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("civil-case:civil-case-update", kwargs={"civil_id": instance.civil_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("civil-case:civil-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:civil-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "civil": civil,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="civilcase/civil_case_detail.html", context=context)


class CivilCaseStageView(View):
    def get(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        civil = get_object_or_404(Civil, pk=civil_id)
        civil_details = CivilDetail.objects.filter(civil_id=civil_id)
        # 存在一审二审等执行阶段
        if civil_details:
            context = {
                "civil": civil,
                "civil_details": civil_details,
            }
            return render(request, template_name="civilcase/civil_case_stage.html", context=context)
        else:
            return redirect(reverse("civil-case:civil-case-detail", kwargs={"civil_id": civil_id}))

    def post(self, request, *args, **kwargs):
        pass


class CivilCaseDetailUpdateView(View):
    """民事案件执行"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        civil_detail = get_object_or_404(CivilDetail, pk=detail_id)

        form = CivilDetailForm(instance=civil_detail)
        nature_person_formset = NaturePersonFormSet(instance=civil_detail)
        legal_person_formset = LegalPersonFormSet(instance=civil_detail)

        context = {
            "form": form,
            "action": "update",
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="civilcase/civil_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", "")

        civil_detail = get_object_or_404(CivilDetail, pk=detail_id)

        form = CivilDetailForm(request.POST, instance=civil_detail)
        nature_person_formset = NaturePersonFormSet(request.POST, instance=civil_detail)
        legal_person_formset = LegalPersonFormSet(request.POST, instance=civil_detail)

        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.save()
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("civil-case:civil-case-update", kwargs={"civil_id": instance.civil_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("civil-case:civil-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:civil-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "action": action,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="civilcase/civil_case_detail.html", context=context)


class CivilCaseDetailDeleteView(View):
    """民事案件执行删除"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        CivilDetail.objects.filter(pk=detail_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CivilCaseDetailSchemeView(View):
    """案件诉讼方案"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        scheme = CivilLawsuitScheme.objects.select_related("civil_detail").filter(civil_detail_id=detail_id).first()
        context = {}
        if scheme:
            case_stage = scheme.civil_detail.stage.id
            legal_status = scheme.civil_detail.legal_status.id
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = CivilCaseSchemeForm(instance=scheme, case_type=case_type)
            else:
                form = CivilCaseSchemeForm(instance=scheme)

            context["action"] = "update"
            context["form"] = form
            evidence_formset = EvidenceListFormSet(instance=scheme)
            asking_formset = AskingOutlineFormSet(instance=scheme)
            for index, form in enumerate(asking_formset):
                form.fields['ask_user'].widget.choices = [('', '--------')] + self.getPersonList(scheme.civil_detail_id)
            compensate_formset = CompensateFormSet(instance=scheme)
            applications_formset = ApplicationsFormSet(instance=scheme)
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        else:
            civil_detail = get_object_or_404(CivilDetail, pk=detail_id)

            case_stage = civil_detail.stage.id
            legal_status = civil_detail.legal_status.id
            print(case_stage, legal_status)
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = CivilCaseSchemeForm(case_type=case_type)
            else:
                form = CivilCaseSchemeForm()

            context["action"] = "add"
            context["form"] = form
            context["civil_detail"] = civil_detail
            evidence_formset = EvidenceListFormSet()
            asking_formset = AskingOutlineFormSet()
            for index, form in enumerate(asking_formset):
                form.fields['ask_user'].widget.choices = [('', '--------')] + self.getPersonList(detail_id)

            compensate_formset = CompensateFormSet()
            applications_formset = ApplicationsFormSet()
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        return render(request, template_name="civilcase/civil_detail_scheme.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", None)

        civil_detail = get_object_or_404(CivilDetail, pk=detail_id)
        case_stage = civil_detail.stage.id
        legal_status = civil_detail.legal_status.id
        case_type = get_case_type(case_stage, legal_status)

        if action == "add":
            form = CivilCaseSchemeForm(request.POST, case_type=case_type)
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
                return redirect(reverse("civil-case:civil-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "civil_detail": civil_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="civilcase/civil_detail_scheme.html", context=context)

        if action == "update":
            scheme = civil_detail.civillawsuitscheme
            form = CivilCaseSchemeForm(request.POST, instance=scheme, case_type=case_type)
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
                # return redirect(reverse("civil-case:civil-case-detail-list", kwargs={"detail_id": detail_id}))
                return redirect(reverse("print:civil-case-print", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "civil_detail": civil_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="civilcase/civil_detail_scheme.html", context=context)

    def getPersonList(self, case_detail_id):
        result = CivilNaturePerson.objects.filter(case_id=case_detail_id).values_list("name", "name")
        return list(result)


class CivilCaseDetailListView(View):
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        civil_detail = get_object_or_404(CivilDetail, pk=detail_id)
        return render(request, template_name="civilcase/civil_case_detail_list.html", context={"civil_detail": civil_detail})


class CivilCaseDistribView(View):
    """民事案件分配"""
    def get(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        civil = get_object_or_404(Civil, pk=civil_id)
        form = CivilLawyerForm(instance=civil)
        action = request.get_full_path()
        context = {
            "form": form,
            "action": action,
        }

        return render(request, template_name="civilcase/include/civil_case_distrib_form.html", context=context)

    def post(self, request, *args, **kwargs):
        civil_id = kwargs.get("civil_id", None)
        civil = get_object_or_404(Civil, pk=civil_id)

        form = CivilLawyerForm(request.POST, instance=civil)

        if form.is_valid():
            form.save()

        return redirect(reverse("adm:case-distrib-list"))


class CivilCasePrintView(View):
    """民事案件打印"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        case_stage = civil_detail.stage_id
        legal_status = civil_detail.legal_status_id
        context = {
            "civil_detail": civil_detail,
        }
        if case_stage == 1 and legal_status == 1:
            return render(request, template_name="civilcase/civil_case_first_print.html", context=context)
        elif case_stage == 1 and legal_status == 2:  # 一审被告
            return render(request, template_name="civilcase/civil_case_first_print_1.html", context=context)
        elif case_stage == 2 and legal_status == 3:  # 二审上诉
            return render(request, template_name="civilcase/civil_case_second_print.html", context=context)
        elif case_stage == 2 and legal_status == 4:  # 二审被上诉
            return render(request, template_name="civilcase/civil_case_second_print_1.html", context=context)
        elif case_stage == 3 and legal_status == 5:  # 申请再审
            return render(request, template_name="civilcase/civil_case_retrial_print.html", context=context)
        elif case_stage == 3 and legal_status == 6:  # 被申请再审
            return render(request, template_name="civilcase/civil_case_second_print_1.html", context=context)


class CivilAgentView(View):
    """委托代理协议"""
    def get(self, request, *args, **kwargs):
        civil = get_object_or_404(Civil, pk=kwargs.get("civil_id"))

        office = Office.objects.first()

        context = {
            "civil": civil,
            "office": office,
        }

        return render(request, template_name="civilcase/print/civil_agent.html", context=context)


class CivilAuthLetterView(View):
    """委托授权书"""
    def get(self, request, *args, **kwargs):
        civil = get_object_or_404(Civil, pk=kwargs.get("civil_id"))
        office = Office.objects.first()

        context = {
            "civil": civil,
            "office": office,
        }
        return render(request, template_name="civilcase/print/civil_auth_letter.html", context=context)


class RiskNoticeView(View):
    """风险告知书"""
    def get(self, request, *args, **kwargs):
        office = Office.objects.first()
        context = {
            "office": office,
        }

        return render(request, template_name="civilcase/print/risk_notice.html", context=context)


class LegalRepresCertView(View):
    """法人代表身份证明"""
    def get(self, request, *args, **kwargs):
        civil = get_object_or_404(Civil, pk=kwargs.get("civil_id"))
        context = {
            "civil": civil,
        }
        return render(request, template_name="civilcase/print/legal_repres_cert.html", context=context)


class CivilComplaintView(View):
    """起诉状"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        natures = civil_detail.natures.exclude(legal_status=7)
        legals = civil_detail.legals.exclude(legal_status=7)
        context = {
            "civil_detail": civil_detail,
            "natures": natures,
            "legals": legals,
        }
        return render(request, template_name="civilcase/print/civil_complaint.html", context=context)


class CivilStatementView(View):
    """代理词"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "civil_detail": civil_detail,
            "office": office,
        }
        return render(request, template_name="civilcase/print/civil_statement.html", context=context)


class CivilEvidenceListView(View):
    """证据目录"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        evidences = civil_detail.civillawsuitscheme.evidencelist_set.all()
        context = {
            "evidences": evidences,
        }
        return render(request, template_name="civilcase/print/civil_evidence_list.html", context=context)


class CivilCompensateView(View):
    """赔偿明细"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        compensates = civil_detail.civillawsuitscheme.civilcompensate_set.all()
        context = {
            "compensates": compensates,
        }
        return render(request, template_name="civilcase/print/civil_compensate.html", context=context)


class CivilAskingOutlineView(View):
    """询问提纲"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        outlines = civil_detail.civillawsuitscheme.askingoutline_set.all()
        context = {
            "outlines": outlines,
        }
        return render(request, template_name="civilcase/print/civil_asking_outline.html", context=context)


class CivilApplicationView(View):
    """相关申请书"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        applications = civil_detail.civillawsuitscheme.applications_set.all()
        context = {
            "applications": applications,
        }
        return render(request, template_name="civilcase/print/civil_application.html", context=context)


class CivilAnswerCounterClaimView(View):
    """反诉答辩状"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        context = {
            "civil_detail": civil_detail,
        }
        return render(request, template_name="civilcase/print/civil_answer_claim.html", context=context)


class CivilCounterClaimView(View):
    """反诉状"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        natures = civil_detail.natures.all()
        legals = civil_detail.legals.all()
        context = {
            "civil_detail": civil_detail,
            "natures": natures,
            "legals": legals,
        }
        return render(request, template_name="civilcase/print/civil_counter_claim.html", context=context)


class CivilPleadingsView(View):
    """答辩状"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        context = {
            "civil_detail": civil_detail,
        }
        return render(request, template_name="civilcase/print/civil_pleadings.html", context=context)


class CivilAppealView(View):
    """上诉状"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        natures = civil_detail.natures.all()
        legals = civil_detail.legals.all()
        first_trial = civil_detail.civil.civildetail_set.filter(stage_id=1).first()   # 一审
        if not first_trial:
            first_trial = civil_detail.civil.civilhisresult_set.filter(stage_id=1).first()

        if first_trial:
            legal_status_id = get_relative_legal_status(first_trial.legal_status_id)
            relative_legal_status = LegalStatus.objects.filter(id=legal_status_id).first()
        else:
            first_trial = None
            relative_legal_status = None

        context = {
            "civil_detail": civil_detail,
            "natures": natures,
            "legals": legals,
            "first_trial": first_trial,
            "relative_legal_status": relative_legal_status,
        }
        return render(request, template_name="civilcase/print/civil_appeal.html", context=context)


class CivilRetrialView(View):
    """再审申请书"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        natures = civil_detail.natures.all()
        legals = civil_detail.legals.all()
        first = civil_detail.civil.civildetail_set.filter(stage_id=1).first()
        if not first:
            first = civil_detail.civil.civilhisresult_set.filter(stage_id=1).first()    # 读取一审历史数据

        second = civil_detail.civil.civildetail_set.filter(stage_id=2).first()

        if not second:
            second = civil_detail.civil.civilhisresult_set.filter(stage_id=2).first()    # 读取二审历史数据

        first_relative_status = None
        second_relative_status = None
        if first:
            f_legal_status = get_relative_legal_status(first.legal_status_id)
            first_relative_status = LegalStatus.objects.filter(id=f_legal_status).first()
        if second:
            s_legal_status = get_relative_legal_status(second.legal_status_id)
            second_relative_status = LegalStatus.objects.filter(id=s_legal_status).first()

        context = {
            "civil_detail": civil_detail,
            "natures": natures,
            "legals": legals,
            "first": first,
            "second": second,
            "first_relative_status": first_relative_status,
            "second_relative_status": second_relative_status,
        }
        return render(request, template_name="civilcase/print/civil_retrial_bill.html", context=context)


class CivilLawyerLetterView(View):
    """律师函"""
    def get(self, request, *args, **kwargs):
        civil_detail = get_object_or_404(CivilDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "civil_detail": civil_detail,
            "office": office,
        }
        return render(request, template_name="civilcase/print/civil_lawyer_letter.html", context=context)
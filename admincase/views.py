import datetime

from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import View

from adm.models import Office
from baseinfo.models import LegalStatus
from .forms import AdminCaseForm, AdminHisResultFormSet, AdminDetailForm, AdminLegalPersonFormSet, \
    AdminNaturePersonFormSet, AdminCaseSchemeForm, AdminEvidenceFormSet, AdminAskingOutlineFormSet, \
    AdminCompensateFormSet, AdminApplicationsFormSet, AdminLawyerForm
from .models import AdminCase, AdminDetail, AdminLawsuitScheme


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


class AdminCaseAddView(View):
    """新建民事案件"""
    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", None)
        form = AdminCaseForm(initial={"lawyer": user_id})
        result_formset = AdminHisResultFormSet()
        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="admincase/admin_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = AdminCaseForm(request.POST)
        result_formset = AdminHisResultFormSet(request.POST)
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
            return redirect(reverse("admincase:admin-case-detail", kwargs={"admin_id": instance.id}))

        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="admincase/admin_case_add.html", context=context)


class AdminCaseUpdateView(View):
    def get(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        admin = get_object_or_404(AdminCase, pk=admin_id)
        form = AdminCaseForm(instance=admin)
        result_formset = AdminHisResultFormSet(instance=admin)

        context = {
            "form": form,
            "result_formset": result_formset,
        }

        return render(request, template_name="admincase/admin_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        admin = get_object_or_404(AdminCase, pk=admin_id)
        form = AdminCaseForm(request.POST, instance=admin)
        result_formset = AdminHisResultFormSet(request.POST, instance=admin)
        if form.is_valid() and result_formset.is_valid():
            instance = form.save()
            result_formset.save()
            return redirect(reverse("admincase:admin-case-stage", kwargs={"admin_id": instance.id}))

        return render(request, template_name="admincase/admin_case_add.html")


class AdminCaseDeleteView(View):
    """案件删除"""
    def get(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        AdminCase.objects.filter(pk=admin_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class AdminCaseDetailView(View):
    """行政案件执行"""
    def get(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        admin = get_object_or_404(AdminCase, pk=admin_id)
        form = AdminDetailForm()
        nature_person_formset = AdminNaturePersonFormSet()
        legal_person_formset = AdminLegalPersonFormSet()

        context = {
            "form": form,
            "admin": admin,
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="admincase/admin_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        admin = get_object_or_404(AdminCase, pk=admin_id)
        form = AdminDetailForm(request.POST)
        nature_person_formset = AdminNaturePersonFormSet(request.POST)
        legal_person_formset = AdminLegalPersonFormSet(request.POST)
        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.instance = instance
            nature_person_formset.save()
            legal_person_formset.instance = instance
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("admincase:admin-case-update", kwargs={"admin_id": instance.civil_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("admincase:admin-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:admin-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "admin": admin,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="admincase/admin_case_detail.html", context=context)


class AdminCaseStageView(View):
    def get(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        admin = get_object_or_404(AdminCase, pk=admin_id)
        admin_details = AdminDetail.objects.filter(admin_id=admin_id)
        # 存在一审二审等执行阶段
        if admin_details:
            context = {
                "admin": admin,
                "admin_details": admin_details,
            }
            return render(request, template_name="admincase/admin_case_stage.html", context=context)
        else:
            return redirect(reverse("admincase:admin-case-detail", kwargs={"admin_id": admin_id}))

    def post(self, request, *args, **kwargs):
        pass


class AdminCaseDetailUpdateView(View):
    """行政案件执行"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        admin_detail = get_object_or_404(AdminDetail, pk=detail_id)

        form = AdminDetailForm(instance=admin_detail)
        nature_person_formset = AdminNaturePersonFormSet(instance=admin_detail)
        legal_person_formset = AdminLegalPersonFormSet(instance=admin_detail)

        context = {
            "form": form,
            "action": "update",
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="admincase/admin_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", "")

        admin_detail = get_object_or_404(AdminDetail, pk=detail_id)

        form = AdminDetailForm(request.POST, instance=admin_detail)
        nature_person_formset = AdminNaturePersonFormSet(request.POST, instance=admin_detail)
        legal_person_formset = AdminLegalPersonFormSet(request.POST, instance=admin_detail)

        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.save()
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("admincase:admin-case-update", kwargs={"admin_id": instance.admin_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("admincase:admin-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:admin-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "action": action,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="admincase/admin_case_detail.html", context=context)


class AdminCaseDetailDeleteView(View):
    """行政案件执行删除"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        AdminDetail.objects.filter(pk=detail_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class AdminCaseDetailSchemeView(View):
    """案件诉讼方案"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        scheme = AdminLawsuitScheme.objects.select_related("admin_detail").filter(admin_detail_id=detail_id).first()
        context = {}
        if scheme:
            case_stage = scheme.admin_detail.stage.id
            legal_status = scheme.admin_detail.legal_status.id
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = AdminCaseSchemeForm(instance=scheme, case_type=case_type)
            else:
                form = AdminCaseSchemeForm(instance=scheme)

            context["action"] = "update"
            context["form"] = form
            evidence_formset = AdminEvidenceFormSet(instance=scheme)
            asking_formset = AdminAskingOutlineFormSet(instance=scheme)
            compensate_formset = AdminCompensateFormSet(instance=scheme)
            applications_formset = AdminApplicationsFormSet(instance=scheme)
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        else:
            admin_detail = get_object_or_404(AdminDetail, pk=detail_id)

            case_stage = admin_detail.stage.id
            legal_status = admin_detail.legal_status.id
            print(case_stage, legal_status)
            case_type = get_case_type(case_stage, legal_status)
            if case_type:
                form = AdminCaseSchemeForm(case_type=case_type)
            else:
                form = AdminCaseSchemeForm()

            context["action"] = "add"
            context["form"] = form
            context["admin_detail"] = admin_detail
            evidence_formset = AdminEvidenceFormSet()
            asking_formset = AdminAskingOutlineFormSet()
            compensate_formset = AdminCompensateFormSet()
            applications_formset = AdminApplicationsFormSet()
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["compensate_formset"] = compensate_formset
            context["applications_formset"] = applications_formset

        return render(request, template_name="admincase/admin_detail_scheme.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", None)

        admin_detail = get_object_or_404(AdminDetail, pk=detail_id)
        case_stage = admin_detail.stage.id
        legal_status = admin_detail.legal_status.id
        case_type = get_case_type(case_stage, legal_status)

        if action == "add":
            form = AdminCaseSchemeForm(request.POST, case_type=case_type)
            evidence_formset = AdminEvidenceFormSet(request.POST)
            asking_formset = AdminAskingOutlineFormSet(request.POST)
            compensate_formset = AdminCompensateFormSet(request.POST)
            applications_formset = AdminApplicationsFormSet(request.POST)
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
                return redirect(reverse("admincase:admin-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "admin_detail": admin_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="admincase/admin_detail_scheme.html", context=context)

        if action == "update":
            scheme = admin_detail.adminlawsuitscheme
            form = AdminCaseSchemeForm(request.POST, instance=scheme, case_type=case_type)
            evidence_formset = AdminEvidenceFormSet(request.POST, instance=scheme)
            asking_formset = AdminAskingOutlineFormSet(request.POST, instance=scheme)
            compensate_formset = AdminCompensateFormSet(request.POST, instance=scheme)
            applications_formset = AdminApplicationsFormSet(request.POST, instance=scheme)
            if form.is_valid() and evidence_formset.is_valid() and asking_formset.is_valid() and compensate_formset.is_valid() and applications_formset.is_valid():
                form.save()
                evidence_formset.save()
                asking_formset.save()
                compensate_formset.save()
                applications_formset.save()
                return redirect(reverse("admincase:admin-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "admin_detail": admin_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "compensate_formset": compensate_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="admincase/admin_detail_scheme.html", context=context)


class AdminCaseDetailListView(View):
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        admin_detail = get_object_or_404(AdminDetail, pk=detail_id)
        return render(request, template_name="admincase/admin_case_detail_list.html", context={"admin_detail": admin_detail})


class AdminCaseDistribView(View):
    """行政案件分配"""
    def get(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        admin = get_object_or_404(AdminCase, pk=admin_id)
        form = AdminLawyerForm(instance=admin)
        action = request.get_full_path()
        context = {
            "form": form,
            "action": action,
        }

        return render(request, template_name="admincase/include/admin_case_distrib_form.html", context=context)

    def post(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", None)
        admin = get_object_or_404(AdminCase, pk=admin_id)

        form = AdminLawyerForm(request.POST, instance=admin)

        if form.is_valid():
            form.save()

        return redirect(reverse("adm:case-distrib-list"))


class AdminCasePrintView(View):
    """行政案件打印"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        case_stage = admin_detail.stage_id
        legal_status = admin_detail.legal_status_id
        context = {
            "admin_detail": admin_detail,
        }
        if case_stage == 1 and legal_status == 1:
            return render(request, template_name="admincase/admin_case_first_print.html", context=context)
        elif case_stage == 1 and legal_status == 2:  # 一审被告
            return render(request, template_name="admincase/admin_case_first_print_1.html", context=context)
        elif case_stage == 2 and legal_status == 3:  # 二审上诉
            return render(request, template_name="admincase/admin_case_second_print.html", context=context)
        elif case_stage == 2 and legal_status == 4:  # 二审被上诉
            return render(request, template_name="admincase/admin_case_second_print_1.html", context=context)
        elif case_stage == 3 and legal_status == 5:  # 申请再审
            return render(request, template_name="admincase/admin_case_retrial_print.html", context=context)
        elif case_stage == 3 and legal_status == 6:  # 被申请再审
            return render(request, template_name="admincase/admin_case_second_print_1.html", context=context)


class AdminAgentView(View):
    """委托代理协议"""
    def get(self, request, *args, **kwargs):
        admin = get_object_or_404(AdminCase, pk=kwargs.get("admin_id"))

        office = Office.objects.first()

        context = {
            "admin": admin,
            "office": office,
        }

        return render(request, template_name="admincase/print/admin_agent.html", context=context)


class AdminAuthLetterView(View):
    """委托授权书"""
    def get(self, request, *args, **kwargs):
        admin = get_object_or_404(AdminCase, pk=kwargs.get("admin_id"))
        office = Office.objects.first()

        context = {
            "admin": admin,
            "office": office,
        }
        return render(request, template_name="admincase/print/admin_auth_letter.html", context=context)


class AdminLegalRepresCertView(View):
    """法人代表身份证明"""
    def get(self, request, *args, **kwargs):
        admin = get_object_or_404(AdminCase, pk=kwargs.get("admin_id"))
        context = {
            "admin": admin,
        }
        return render(request, template_name="admincase/print/admin_legal_repres_cert.html", context=context)


class AdminComplaintView(View):
    """起诉状"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        natures = admin_detail.natures.exclude(legal_status=7)
        legals = admin_detail.legals.exclude(legal_status=7)
        context = {
            "admin_detail": admin_detail,
            "natures": natures,
            "legals": legals,
        }
        return render(request, template_name="admincase/print/admin_complaint.html", context=context)


class AdminStatementView(View):
    """代理词"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "admin_detail": admin_detail,
            "office": office,
        }
        return render(request, template_name="admincase/print/admin_statement.html", context=context)


class AdminEvidenceListView(View):
    """证据目录"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        evidences = admin_detail.adminlawsuitscheme.adminevidence_set.all()
        context = {
            "evidences": evidences,
        }
        return render(request, template_name="admincase/print/admin_evidence_list.html", context=context)


class AdminCompensateView(View):
    """赔偿明细"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        compensates = admin_detail.adminlawsuitscheme.admincompensate_set.all()
        context = {
            "compensates": compensates,
        }
        return render(request, template_name="admincase/print/admin_compensate.html", context=context)


class AdminAskingOutlineView(View):
    """询问提纲"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        outlines = admin_detail.adminlawsuitscheme.adminaskingoutline_set.all()
        context = {
            "outlines": outlines,
        }
        return render(request, template_name="admincase/print/admin_asking_outline.html", context=context)


class AdminApplicationView(View):
    """相关申请书"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        applications = admin_detail.adminlawsuitscheme.adminapplications_set.all()
        context = {
            "applications": applications,
        }
        return render(request, template_name="admincase/print/admin_application.html", context=context)


class AdminPleadingsView(View):
    """答辩状"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        context = {
            "admin_detail": admin_detail,
        }
        return render(request, template_name="admincase/print/admin_pleadings.html", context=context)


class AdminAppealView(View):
    """上诉状"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        natures = admin_detail.natures.all()
        legals = admin_detail.legals.all()
        first_trial = admin_detail.admin.admindetail_set.filter(stage_id=1).first()   # 一审
        if not first_trial:
            first_trial = admin_detail.admin.adminhisresult_set.filter(stage_id=1).first()

        if first_trial:
            legal_status_id = get_relative_legal_status(first_trial.legal_status_id)
            relative_legal_status = LegalStatus.objects.filter(id=legal_status_id).first()
        else:
            first_trial = None
            relative_legal_status = None

        context = {
            "admin_detail": admin_detail,
            "natures": natures,
            "legals": legals,
            "first_trial": first_trial,
            "relative_legal_status": relative_legal_status,
        }
        return render(request, template_name="admincase/print/admin_appeal.html", context=context)


class AdminRetrialView(View):
    """再审申请书"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        natures = admin_detail.natures.all()
        legals = admin_detail.legals.all()
        first = admin_detail.admin.admindetail_set.filter(stage_id=1).first()
        if not first:
            first = admin_detail.admin.adminhisresult_set.filter(stage_id=1).first()    # 读取一审历史数据

        second = admin_detail.admin.admindetail_set.filter(stage_id=2).first()

        if not second:
            second = admin_detail.admin.adminhisresult_set.filter(stage_id=2).first()    # 读取二审历史数据

        first_relative_status = None
        second_relative_status = None
        if first:
            f_legal_status = get_relative_legal_status(first.legal_status_id)
            first_relative_status = LegalStatus.objects.filter(id=f_legal_status).first()
        if second:
            s_legal_status = get_relative_legal_status(second.legal_status_id)
            second_relative_status = LegalStatus.objects.filter(id=s_legal_status).first()

        context = {
            "admin_detail": admin_detail,
            "natures": natures,
            "legals": legals,
            "first": first,
            "second": second,
            "first_relative_status": first_relative_status,
            "second_relative_status": second_relative_status,
        }
        return render(request, template_name="admincase/print/admin_retrial_bill.html", context=context)


class AdminLawyerLetterView(View):
    """律师函"""
    def get(self, request, *args, **kwargs):
        admin_detail = get_object_or_404(AdminDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "admin_detail": admin_detail,
            "office": office,
        }
        return render(request, template_name="admincase/print/admin_lawyer_letter.html", context=context)
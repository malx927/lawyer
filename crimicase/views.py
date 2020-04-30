from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from adm.models import Office
from crimicase.forms import CrimiCaseForm, CriminalDetailForm, CrimiNaturePersonFormSet, CrimiLegalPersonFormSet, \
    CrimiCaseSchemeForm, EvidenceFormSet, AskingOutlineFormSet, ApplicationsFormSet, CriminalLawyerForm, \
    HisResultFormSet
from crimicase.models import Criminal, CriminalDetail, CrimiLawsuitScheme


class CrimiCaseAddView(View):
    """刑事案件增加"""
    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", None)
        form = CrimiCaseForm(initial={"lawyer": user_id})
        result_formset = HisResultFormSet()
        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="crimicase/criminal_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        form = CrimiCaseForm(request.POST)
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
            return redirect(reverse("criminal:criminal-case-detail", kwargs={"crimi_id": instance.id}))

        context = {
            "form": form,
        }
        return render(request, template_name="crimicase/criminal_case_add.html", context=context)


class CriminalCaseUpdateView(View):
    def get(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        criminal = get_object_or_404(Criminal, pk=crimi_id)
        form = CrimiCaseForm(instance=criminal)
        result_formset = HisResultFormSet(instance=criminal)
        context = {
            "form": form,
            "result_formset": result_formset,
        }
        return render(request, template_name="crimicase/criminal_case_add.html", context=context)

    def post(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        criminal = get_object_or_404(Criminal, pk=crimi_id)
        form = CrimiCaseForm(request.POST, instance=criminal)
        result_formset = HisResultFormSet(request.POST, instance=criminal)
        if form.is_valid() and result_formset.is_valid():
            instance = form.save()
            result_formset.save()
            return redirect(reverse("criminal:criminal-case-stage", kwargs={"crimi_id": instance.id}))

        return render(request, template_name="crimicase/criminal_case_add.html")


class CriminalCaseDeleteView(View):
    """刑事案件删除"""
    def get(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        Criminal.objects.filter(pk=crimi_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CriminalCaseStageView(View):
    def get(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        criminal = get_object_or_404(Criminal, pk=crimi_id)
        criminal_details = CriminalDetail.objects.filter(criminal_id=crimi_id)
        # 存在一审二审等执行阶段
        if criminal_details:
            context = {
                "criminal": criminal,
                "criminal_details": criminal_details,
            }
            return render(request, template_name="crimicase/criminal_case_stage.html", context=context)
        else:
            return redirect(reverse("criminal:criminal-case-detail", kwargs={"crimi_id": crimi_id}))

    def post(self, request, *args, **kwargs):
        pass


class CrimiCaseDetailView(View):
    """刑事案件执行"""
    def get(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        print(crimi_id)
        criminal = get_object_or_404(Criminal, pk=crimi_id)
        form = CriminalDetailForm()
        nature_person_formset = CrimiNaturePersonFormSet()
        legal_person_formset = CrimiLegalPersonFormSet()

        context = {
            "form": form,
            "criminal": criminal,
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="crimicase/criminal_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        criminal = get_object_or_404(Criminal, pk=crimi_id)
        form = CriminalDetailForm(request.POST)
        nature_person_formset = CrimiNaturePersonFormSet(request.POST)
        legal_person_formset = CrimiLegalPersonFormSet(request.POST)
        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.instance = instance
            nature_person_formset.save()
            legal_person_formset.instance = instance
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("criminal:criminal-case-update", kwargs={"crimi_id": instance.criminal_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("criminal:criminal-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:criminal-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "criminal": criminal,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="crimicase/criminal_case_detail.html", context=context)


class CriminalCaseDetailUpdateView(View):
    """刑事案件执行"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        criminal_detail = get_object_or_404(CriminalDetail, pk=detail_id)

        form = CriminalDetailForm(instance=criminal_detail)
        nature_person_formset = CrimiNaturePersonFormSet(instance=criminal_detail)
        legal_person_formset = CrimiLegalPersonFormSet(instance=criminal_detail)

        context = {
            "form": form,
            "action": "update",
            "nature_person_formset": nature_person_formset,
            "legal_person_formset": legal_person_formset,
        }
        return render(request, template_name="crimicase/criminal_case_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", "")

        criminal_detail = get_object_or_404(CriminalDetail, pk=detail_id)

        form = CriminalDetailForm(request.POST, instance=criminal_detail)
        nature_person_formset = CrimiNaturePersonFormSet(request.POST, instance=criminal_detail)
        legal_person_formset = CrimiLegalPersonFormSet(request.POST, instance=criminal_detail)

        if form.is_valid() and nature_person_formset.is_valid() and legal_person_formset.is_valid():
            instance = form.save()
            nature_person_formset.save()
            legal_person_formset.save()

            if "save" in request.POST:
                return redirect(reverse("criminal:criminal-case-update", kwargs={"crimi_id": instance.criminal_id}))
            elif "save_create" in request.POST:
                return redirect(reverse("criminal:criminal-case-detail-scheme", kwargs={"detail_id": instance.id}))
            elif "save_print" in request.POST:
                return redirect(reverse("print:criminal-case-print", kwargs={"detail_id": instance.id}))
        else:
            context = {
                "form": form,
                "action": action,
                "nature_person_formset": nature_person_formset,
                "legal_person_formset": legal_person_formset,
            }
            return render(request, template_name="civilcase/civil_case_detail.html", context=context)


class CriminalCaseDetailDeleteView(View):
    """刑事案件执行删除"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        CriminalDetail.objects.filter(pk=detail_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class CriminalCaseDetailSchemeView(View):
    """刑事案件诉讼方案"""
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        scheme = CrimiLawsuitScheme.objects.select_related("crimi_detail").filter(crimi_detail_id=detail_id).first()
        context = {}
        if scheme:              # 修改
            case_stage = scheme.crimi_detail.stage.id
            if case_stage:
                form = CrimiCaseSchemeForm(instance=scheme, case_stage=case_stage)
            else:
                form = CrimiCaseSchemeForm(instance=scheme)

            context["action"] = "update"
            context["form"] = form
            evidence_formset = EvidenceFormSet(instance=scheme)
            asking_formset = AskingOutlineFormSet(instance=scheme)
            applications_formset = ApplicationsFormSet(instance=scheme)
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["applications_formset"] = applications_formset

        else:                   # 增加
            criminal_detail = get_object_or_404(CriminalDetail, pk=detail_id)
            case_stage = criminal_detail.stage.id
            if case_stage:
                form = CrimiCaseSchemeForm(case_stage=case_stage)
            else:
                form = CrimiCaseSchemeForm()

            context["action"] = "add"
            context["form"] = form
            context["criminal_detail"] = criminal_detail
            evidence_formset = EvidenceFormSet()
            asking_formset = AskingOutlineFormSet()
            applications_formset = ApplicationsFormSet()
            context["evidence_formset"] = evidence_formset
            context["asking_formset"] = asking_formset
            context["applications_formset"] = applications_formset

        return render(request, template_name="crimicase/criminal_detail_scheme.html", context=context)

    def post(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        action = request.POST.get("action", None)

        criminal_detail = get_object_or_404(CriminalDetail, pk=detail_id)
        case_stage = criminal_detail.stage.id

        if action == "add":
            form = CrimiCaseSchemeForm(request.POST, case_stage=case_stage)
            evidence_formset = EvidenceFormSet(request.POST)
            asking_formset = AskingOutlineFormSet(request.POST)
            applications_formset = ApplicationsFormSet(request.POST)
            if form.is_valid() and evidence_formset.is_valid() and asking_formset.is_valid() and applications_formset.is_valid():
                instance = form.save()
                evidence_formset.instance = instance
                evidence_formset.save()
                asking_formset.instance = instance
                asking_formset.save()
                applications_formset.instance = instance
                applications_formset.save()
                return redirect(reverse("criminal:criminal-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "crimi_detail": criminal_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="crimicase/criminal_detail_scheme.html", context=context)

        if action == "update":
            scheme = criminal_detail.crimilawsuitscheme
            form = CrimiCaseSchemeForm(request.POST, instance=scheme, case_stage=case_stage)
            evidence_formset = EvidenceFormSet(request.POST, instance=scheme)
            asking_formset = AskingOutlineFormSet(request.POST, instance=scheme)
            applications_formset = ApplicationsFormSet(request.POST, instance=scheme)
            if form.is_valid() and evidence_formset.is_valid() and asking_formset.is_valid() and applications_formset.is_valid():
                form.save()
                evidence_formset.save()
                asking_formset.save()
                applications_formset.save()
                return redirect(reverse("criminal:criminal-case-detail-list", kwargs={"detail_id": detail_id}))

            context = {
                "action": action,
                "criminal_detail": criminal_detail,
                "form": form,
                "evidence_formset": evidence_formset,
                "asking_formset": asking_formset,
                "applications_formset": applications_formset,
            }
            return render(request, template_name="crimicase/criminal_detail_scheme.html", context=context)


class CriminalCaseDetailListView(View):
    def get(self, request, *args, **kwargs):
        detail_id = kwargs.get("detail_id", None)
        criminal_detail = get_object_or_404(CriminalDetail, pk=detail_id)
        return render(request, template_name="crimicase/criminal_case_detail_list.html", context={"criminal_detail": criminal_detail})


class CriminalCaseDistribView(View):
    """刑事案件分配"""
    def get(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        criminal = get_object_or_404(Criminal, pk=crimi_id)
        form = CriminalLawyerForm(instance=criminal)
        action = request.get_full_path()
        context = {
            "form": form,
            "action": action,
        }

        return render(request, template_name="crimicase/include/criminal_case_distrib_form.html", context=context)

    def post(self, request, *args, **kwargs):
        crimi_id = kwargs.get("crimi_id", None)
        criminal = get_object_or_404(Criminal, pk=crimi_id)

        form = CriminalLawyerForm(request.POST, instance=criminal)

        if form.is_valid():
            form.save()

        return redirect(reverse("adm:case-distrib-list"))


class CriminalCasePrintView(View):
    """民事案件打印"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        case_stage = criminal_detail.stage_id
        context = {
            "criminal_detail": criminal_detail,
        }
        if case_stage == 1:     # 侦查阶段
            return render(request, template_name="crimicase/criminal_case_invest_print.html", context=context)
        elif case_stage == 2:  # 审查起诉阶段
            return render(request, template_name="crimicase/criminal_case_review_print.html", context=context)
        elif case_stage == 3:  # 一审
            return render(request, template_name="crimicase/criminal_case_first_print.html", context=context)
        elif case_stage == 4:  # 二审
            return render(request, template_name="crimicase/criminal_case_second_print.html", context=context)
        elif case_stage == 5:  # 再审
            return render(request, template_name="crimicase/criminal_case_retrial_print.html", context=context)


class CriminalAgentView(View):
    """委托代理协议"""
    def get(self, request, *args, **kwargs):
        criminal = get_object_or_404(Criminal, pk=kwargs.get("crimi_id"))

        office = Office.objects.first()

        context = {
            "criminal": criminal,
            "office": office,
        }

        return render(request, template_name="crimicase/print/criminal_agent.html", context=context)


class CriminalAuthLetterView(View):
    """委托授权书"""
    def get(self, request, *args, **kwargs):
        criminal = get_object_or_404(Criminal, pk=kwargs.get("crimi_id"))
        office = Office.objects.first()

        context = {
            "criminal": criminal,
            "office": office,
        }
        return render(request, template_name="crimicase/print/criminal_auth_letter.html", context=context)


class CriminalLegalRepresCertView(View):
    """法人代表身份证明"""
    def get(self, request, *args, **kwargs):
        criminal = get_object_or_404(Criminal, pk=kwargs.get("crimi_id"))
        context = {
            "criminal": criminal,
        }
        return render(request, template_name="crimicase/print/criminal_legal_repres_cert.html", context=context)


class CriminalIntroduceLetterView(View):
    """会见介绍信"""
    def get(self, request, *args, **kwargs):
        criminal = get_object_or_404(Criminal, pk=kwargs.get("crimi_id"))
        office = Office.objects.first()

        context = {
            "criminal": criminal,
            "office": office,
        }
        return render(request, template_name="crimicase/print/criminal_introduce_letter.html", context=context)


class CriminalBailAwaitView(View):
    """取保候审申请书"""
    def get(self, request, *args, **kwargs):
        flag = request.GET.get("flag", "0")

        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()

        context = {
            "criminal_detail": criminal_detail,
            "office": office,
        }
        if flag == "0":      # 律师申请
            return render(request, template_name="crimicase/print/criminal_bail_await_lawyer.html", context=context)
        elif flag == "1":
            return render(request, template_name="crimicase/print/criminal_bail_await_client.html", context=context)


class CriminalLegalOpinionView(View):
    """法律意见书"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()

        context = {
            "criminal_detail": criminal_detail,
            "office": office,
        }

        return render(request, template_name="crimicase/print/criminal_legal_opinion_invest.html", context=context)


class CriminalEvidenceListView(View):
    """证据目录"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        evidences = criminal_detail.crimilawsuitscheme.crimievidence_set.all()
        context = {
            "evidences": evidences,
        }
        return render(request, template_name="crimicase/print/criminal_evidence_list.html", context=context)


class CriminalAskingOutlineView(View):
    """询问提纲"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        outlines = criminal_detail.crimilawsuitscheme.crimiaskingoutline_set.all()
        context = {
            "outlines": outlines,
        }
        return render(request, template_name="crimicase/print/criminal_asking_outline.html", context=context)


class CriminalApplicationView(View):
    """相关申请书"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        applications = criminal_detail.crimilawsuitscheme.crimiapplications_set.all()
        context = {
            "applications": applications,
        }
        return render(request, template_name="crimicase/print/criminal_application.html", context=context)


class CriminalLawyerLetterView(View):
    """律师函"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()
        context = {
            "criminal_detail": criminal_detail,
            "office": office,
        }
        return render(request, template_name="crimicase/print/criminal_lawyer_letter.html", context=context)


class CriminalNoArrestOpinionView(View):
    """不予逮捕法律意见书"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()

        context = {
            "criminal_detail": criminal_detail,
            "office": office,
        }

        return render(request, template_name="crimicase/print/criminal_no_arrest_opinion.html", context=context)


class CriminalDetainOpinionView(View):
    """羁押必要性审查申请"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()

        context = {
            "criminal_detail": criminal_detail,
            "office": office,
        }

        return render(request, template_name="crimicase/print/criminal_detain_opinion.html", context=context)


class CriminalDefenseOpinionView(View):
    """辩护词"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        office = Office.objects.first()

        context = {
            "criminal_detail": criminal_detail,
            "office": office,
        }

        return render(request, template_name="crimicase/print/criminal_defense_opinion.html", context=context)


class CriminalAppealView(View):
    """上诉状"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        # natures = criminal_detail.natures.all()
        # legals = criminal_detail.legals.all()
        first_trial = criminal_detail.criminal.criminaldetail_set.filter(stage_id=3).first()  # 一审
        if not first_trial:
            first_trial = criminal_detail.criminal.criminalhisresult_set.filter(stage_id=3).first()

        context = {
            "criminal_detail": criminal_detail,
            # "natures": natures,
            # "legals": legals,
            "first_trial": first_trial,
        }

        return render(request, template_name="crimicase/print/criminal_appeal.html", context=context)


class CriminalRetrialView(View):
    """再审申请书"""
    def get(self, request, *args, **kwargs):
        criminal_detail = get_object_or_404(CriminalDetail, pk=kwargs.get("detail_id"))
        first = criminal_detail.criminal.criminaldetail_set.filter(stage_id=3).first()
        if not first:
            first = criminal_detail.criminal.criminaldetail_set.filter(stage_id=3).first()    # 读取一审历史数据

        second = criminal_detail.criminal.criminaldetail_set.filter(stage_id=4).first()
        if not second:
            second = criminal_detail.criminal.criminaldetail_set.filter(stage_id=4).first()    # 读取二审历史数据

        context = {
            "criminal_detail": criminal_detail,
            "first": first,
            "second": second,
        }
        return render(request, template_name="crimicase/print/criminal_retrial_bill.html", context=context)
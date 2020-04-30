import datetime
import json

from django.db.models import Count, F, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.forms.models import model_to_dict

from adm.forms import OfficeForm, UserChangeForm, SpecialFormSet, ProfessionalFormSet, SocialFormSet
from adm.models import Office
from admincase.models import AdminCase
from baseinfo.constants import CASE_TYPE
from civilcase.models import CivilDetail, Civil
from crimicase.models import Criminal
from crimicivil.models import CrimiCivil
from crimiprivate.models import CrimiPrivate
from rbac.forms import UserForm
from rbac.models import UserInfo


class UserAuthView(View):
    """用户授权"""
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, template_name="adm/user_auth.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']
            if password != password1:  # 判断两次密码是否相同
                message = "两次输入的密码不匹配！"
                return render(request, 'adm/user_auth.html', locals())

            same_name_user = UserInfo.objects.filter(name=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
                return render(request, 'adm/user_auth.html', locals())
            obj = form.save(commit=False)
            obj.is_active = True
            obj.save()
            form.save_m2m()
            form = UserForm()
            form.success = True
            return render(request, template_name="adm/user_auth.html", context={"form": form})

        return render(request, template_name="adm/user_auth.html", context={"form": form})


class UserCategoryListView(View):
    """用户分类列表"""
    def get(self, request, *args, **kwargs):
        results = UserInfo.objects.values("post_id", "post__name").order_by("post_id").annotate(counts=Count("id"))
        users = []

        for item in results:
            c_users = UserInfo.objects.filter(post_id=item["post_id"])
            item["children"] = c_users
            users.append(item)

        return render(request, template_name="adm/user_category_list.html", context={"users": users})


class UserDetailChangeView(View):
    """用户详情完善"""
    def get(self, request, *args, **kwargs):
        user_id = request.session.get("user_id")
        user = get_object_or_404(UserInfo, pk=user_id)

        form = UserChangeForm(initial={"is_update": True}, instance=user)
        special_formset = SpecialFormSet(instance=user)
        professional_formset = ProfessionalFormSet(instance=user)
        social_formset = SocialFormSet(instance=user)
        context = {
            "user_id": user_id,
            "form": form,
            "special_formset": special_formset,
            "professional_formset": professional_formset,
            "social_formset": social_formset,
        }
        return render(request, template_name="adm/my_user_info_change.html", context=context)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        next = request.GET.get("next", None)
        user = get_object_or_404(UserInfo, pk=user_id)
        form = UserChangeForm(request.POST, instance=user)
        special_formset = SpecialFormSet(request.POST, instance=user)
        professional_formset = ProfessionalFormSet(request.POST, instance=user)
        social_formset = SocialFormSet(request.POST, instance=user)

        if form.is_valid() and special_formset.is_valid() and professional_formset.is_valid() and social_formset.is_valid():
            form.save()
            special_formset.save()
            professional_formset.save()
            social_formset.save()
            if next:
                return redirect(next)
            return redirect(reverse("adm:user-detail-change"))
        else:
            context = {
                "user_id": user_id,
                "form": form,
                "special_formset": special_formset,
                "professional_formset": professional_formset,
                "social_formset": social_formset,
            }
            print(social_formset)
            return render(request, template_name="adm/my_user_info_change.html", context=context)


class UserDetailView(View):
    """用户详情"""
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        user = get_object_or_404(UserInfo, pk=pk)
        form = UserChangeForm(instance=user)
        return render(request, template_name="adm/include/user_detail.html", context={"form": form})


class OfficeView(View):
    """律师事务所"""
    def get(self, request, *args, **kwargs):
        office = Office.objects.first()
        if office:
            form = OfficeForm(instance=office)
            return render(request, template_name="adm/office_detail.html", context={"form": form})
        else:
            form = OfficeForm()
            return render(request, template_name="adm/office_add.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, template_name="adm/office_add.html", context={"form": form})

        return render(request, template_name="adm/office_detail.html", context={"form": form})


class OfficeUpdateView(View):
    """律师事务所"""
    def get(self, request, *args, **kwargs):
        office_id = kwargs.get("pk")
        office = Office.objects.filter(id=office_id).first()
        if office:
            form = OfficeForm(instance=office)
            return render(request, template_name="adm/office_add.html", context={"form": form})
        else:
            return redirect(reverse("office"))

    def post(self, request, *args, **kwargs):
        office_id = kwargs.get("pk")
        office = Office.objects.filter(id=office_id).first()
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
        else:
            return render(request, template_name="adm/office_add.html", context={"form": form})

        return render(request, template_name="adm/office_detail.html", context={"form": form})


class MyCase(View):
    """我的案件"""
    def get(self, request, *args, **kwargs):
        return render(request, template_name="adm/mycase_panel.html")


class CaseCategory(View):
    """案件类型面板"""
    def get(self, request, *args, **kwargs):
        return render(request, template_name="adm/case_category_panel.html")


class CaseInfo(View):
    """案件信息"""
    def get(self, request, *args, **kwargs):
        return render(request, template_name="adm/case_info_panel.html")


class CaseDistributeView(View):
    """案件分配"""
    def get(self, request, *args, **kwargs):
        # 民事案件
        civils = Civil.objects.filter(Q(is_assign=0) | Q(is_assign__isnull=True))
        criminals = Criminal.objects.filter(Q(is_assign=0) | Q(is_assign__isnull=True))
        admins = AdminCase.objects.filter(Q(is_assign=0) | Q(is_assign__isnull=True))
        privates = CrimiPrivate.objects.filter(Q(is_assign=0) | Q(is_assign__isnull=True))
        crmcivils = CrimiCivil.objects.filter(Q(is_assign=0) | Q(is_assign__isnull=True))
        context = {
            "civils": civils,
            "criminals": criminals,
            "admins": admins,
            "privates": privates,
            "crmcivils": crmcivils,
        }
        return render(request, template_name="adm/case_distribute_list.html", context=context)

    def post(self, request, *args, **kwargs):
        pass


class CaseDoingListView(View):
    """案件未完列表"""
    def get(self, request, *args, **kwargs):
        # 民事
        user_id = request.session.get("user_id", None)
        is_superuser = request.session.get("is_superuser", None)
        if is_superuser:
            civils = Civil.objects.all()
            criminals = Criminal.objects.all()
            admins = AdminCase.objects.all()
            privates = CrimiPrivate.objects.all()
            crimicivils = CrimiCivil.objects.all()
        else:
            civils = Civil.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))
            criminals = Criminal.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))
            admins = AdminCase.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))
            privates = CrimiPrivate.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))
            crimicivils = CrimiCivil.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))

        context = {
            "civils": civils,
            "criminals": criminals,
            "admins": admins,
            "privates": privates,
            "crimicivils": crimicivils,
        }
        return render(request, template_name="adm/case_doing_list.html", context=context)


class CaseSearchListView(View):
    """案件搜索列表"""
    def get(self, request, *args, **kwargs):
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        case_type = request.GET.get("case_type", None)
        client_name = request.GET.get("client_name")
        party_name = request.GET.get("party_name")

        # 案件类型
        case_types = self.get_case_type()

        if not case_type:
            case_type = "1"

        user_id = request.session.get("user_id", None)
        is_superuser = request.session.get("is_superuser", None)

        query_set = None
        if case_type == "1":    # 民事案件
            if is_superuser:
                query_set = Civil.objects.all()
            else:
                query_set = Civil.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))

        elif case_type == "2":  # 刑事案件
            if is_superuser:
                query_set = Criminal.objects.all()
            else:
                query_set = Criminal.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))

        elif case_type == "3":  # 刑事自诉案件
            if is_superuser:
                query_set = CrimiPrivate.objects.all()
            else:
                query_set = CrimiPrivate.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))

        elif case_type == "4":  # 刑事附带民事案件
            if is_superuser:
                query_set = CrimiCivil.objects.all()
            else:
                query_set = CrimiCivil.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))
        elif case_type == "5":  # 行政案件
            if is_superuser:
                query_set = AdminCase.objects.all()
            else:
                query_set = AdminCase.objects.filter(Q(lawyer_id=user_id) | Q(assist_id=user_id) | Q(manager_id=user_id))
        elif case_type == "6":  # 仲裁
            pass
        elif case_type == "7":  # 执行
            pass

        if query_set:
            # 时间段
            if start_time and end_time:
                d_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
                d_end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
                query_set = query_set.filter(create_at__date__range=[d_start_time, d_end_time])
            elif start_time and not end_time:
                d_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
                query_set = query_set.filter(create_at__date=d_start_time)

            # 委托人
            if client_name:
                query_set = query_set.filter(Q(cli_name__contains=client_name) | Q(cli_legal_name__contains=client_name))
            # 当事人
            if party_name:
                query_set = query_set.filter(Q(party_name__contains=party_name) | Q(party_legal_name__contains=party_name))
        else:
            pass

        context = {
            "cases": query_set,
            "case_types": case_types,
            "start_time": start_time,
            "end_time": end_time,
            "case_type": case_type,
            "client_name": client_name,
            "party_name": party_name,
        }
        return render(request, template_name="adm/case_search_page.html", context=context)

    def get_case_type(self):
        """案件类型"""
        return CASE_TYPE

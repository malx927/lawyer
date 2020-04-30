import datetime

from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from advisor.forms import ConsultantUnitForm
from advisor.models import ConsultantUnit
from lawyer import settings


class ConsultPanelView(View):
    """顾问功能面板"""
    def get(self, request, *args, **kwargs):
        current_permission_pid = request.current_permission_pid
        menu_dict = request.session.get(settings.MENU_SESSION_KEY)
        menu = menu_dict.get(str(current_permission_pid), None)

        if menu:
            children_menus = menu.get("children", None)
        else:
            children_menus = None
        print(children_menus)
        return render(request, template_name="advisor/advisor_panel.html", context={"children_menus": children_menus})

    def post(self, request, *args, **kwargs):
        pass


class ConsultUnitView(View):
    """顾问单位增加"""
    def get(self, request, *args, **kwargs):
        # form = ConsultantUnitForm(user_id=request.session.get("user_id"))
        form = ConsultantUnitForm()
        return render(request, template_name="advisor/advisor_add.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = ConsultantUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("advisor:consult-unit-add"))

        return render(request, template_name="advisor/advisor_add.html", context={"form": form})


class ConsultUnitListView(View):
    """顾问单位查询"""
    def get(self, request, *args, **kwargs):
        unit_name = request.GET.get("unit_name", None)
        person = request.GET.get("person", None)
        begin_time = request.GET.get("begin_time", None)
        end_time = request.GET.get("end_time", None)
        user_id = request.session.get("user_id", None)
        post = request.session.get("post", None)
        is_superuser = request.session.get("is_superuser", 0)
        if post in [5, 7] or is_superuser == 1:
            consultants = ConsultantUnit.objects.all()
        else:
            consultants = ConsultantUnit.objects.filter(lawyer__id=user_id)

        if unit_name:
            consultants = consultants.filter(unit_name__contains=unit_name)

        if person:
            consultants = consultants.filter(person__contains=person)

        if begin_time and not end_time:
            begin_date = datetime.datetime.strptime(begin_time, "%Y-%m-%d")
            consultants = consultants.filter(sign_begin=begin_date)

        if begin_time and end_time:
            begin_date = datetime.datetime.strptime(begin_time, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_time, "%Y-%m-%d")
            consultants = consultants.filter(sign_begin__range=(begin_date, end_date))

        consultants = consultants.order_by("-sign_begin")
        # print(consultants)
        context = {
            "consultants": consultants
        }
        return render(request, template_name="advisor/consult_unit_list.html", context=locals())

    def post(self, request, *args, **kwargs):
        pass


class ConsultUnitUpdateView(View):
    """顾问单位修改"""
    def get(self, request, *args, **kwargs):
        c_id = kwargs.get("pk", None)
        format = request.GET.get("_format", None)
        print("c_id", c_id)
        if c_id:
            consult_unit = ConsultantUnit.objects.filter(pk=c_id).first()
            if consult_unit:
                form = ConsultantUnitForm(instance=consult_unit)
                if format == "html":
                    return render(request, template_name="advisor/include/consult_unit_detail.html", context={"form": form, "format": format})
                return render(request, template_name="advisor/advisor_add.html", context={"form": form})
        else:
            pass
        return redirect(reverse("advisor:consult-unit-list"))

    def post(self, request, *args, **kwargs):
        c_id = kwargs.get("pk")
        format = request.POST.get("format", None)
        if c_id:
            consult_unit = ConsultantUnit.objects.filter(pk=c_id).first()
            form = ConsultantUnitForm(request.POST, instance=consult_unit)
            if form.is_valid():
                form.save()
            else:
                return render(request, template_name="advisor/advisor_add.html", context={"form": form})
        if format == "html":
            return redirect(reverse("advisor:consult-unit-dispatch"))   # 单位分配

        return redirect(reverse("advisor:consult-unit-list"))


class ConsultUnitDeleteView(View):
    """顾问单位删除"""
    def get(self, request, *args, **kwargs):
        c_id = kwargs.get("pk")
        if c_id:
            ConsultantUnit.objects.filter(pk=c_id).delete()
        else:
            pass

        return redirect(reverse("advisor:consult-unit-list"))


class ConsultUnitDispatchView(View):
    """顾问单位分配"""
    def get(self, request, *args, **kwargs):
        units = ConsultantUnit.objects.filter(Q(is_assign=0) | Q(is_assign__isnull=True), unit_type=0)
        persons = ConsultantUnit.objects.filter(Q(is_assign=0) | Q(is_assign__isnull=True), unit_type=1)
        context = {
            "units": units,
            "persons": persons,
        }
        return render(request, template_name="advisor/unit_dispach_list.html", context=context)

    def post(self, request, *args, **kwargs):
        pass
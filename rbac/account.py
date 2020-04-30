#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from rbac.forms import UserForm, UpdateUserForm, PasswordChangeForm
from .models import UserInfo
from rbac.service.init_permission import init_permission


def login(request):
    """
    用户登录
    """
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = UserInfo.objects.filter(name=name, password=password).first()
        if not user:
            return render(request, 'rbac/login.html', {'msg': '用户名或密码错误'})
        elif not user.is_active:
            return render(request, 'rbac/login.html', {'msg': '用户未激活'})
        else:
            user.last_login = datetime.datetime.now()
            user.save()
            request.session["user_id"] = user.id
            request.session["real_name"] = user.real_name
            request.session["username"] = user.name
            request.session["is_superuser"] = user.is_superuser
            request.session["post"] = user.post_id
            init_permission(user, request)
            user_detail_url = reverse("adm:user-detail-change")
            index = reverse("adm:my-case")
            if not user.is_update and not user.is_superuser:
                return redirect("{}?next={}".format(user_detail_url, index))
            return redirect(index)
    else:
        return render(request, 'rbac/login.html')


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.delete()

    return redirect('/login/')


def user_list(request):
    """
    用户信息
    :param request:
    :return:
    """
    users = UserInfo.objects.all().order_by("-id")
    context = {
        'users': users,
    }
    return render(request, template_name='rbac/user_list.html', context=context)


def user_add(request):
    """
    用户信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']
            if password != password1:  # 判断两次密码是否相同
                message = "两次输入的密码不匹配！"
                return render(request, 'rbac/user_change.html', locals())

            same_name_user = UserInfo.objects.filter(name=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
                return render(request, 'rbac/user_change.html', locals())
            form.save()
            return redirect(reverse('rbac:user-list'))
    return render(request, 'rbac/user_change.html', {'form': form})


def user_edit(request, pk):
    """用户修改"""
    obj = UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('权限不存在')

    if request.method == 'GET':
        form = UpdateUserForm(instance=obj)
    else:
        form = UpdateUserForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user-list'))
    return render(request, 'rbac/user_change.html', {'form': form})


def user_del(request, pk):
    """
    删除权限
    :param request:
    """
    UserInfo.objects.filter(id=pk).delete()
    return redirect(request.META['HTTP_REFERER'])


def password_change(request, pk):
    """修改密码"""
    if request.method == "GET":
        form = PasswordChangeForm()
        context = {
            "form": form,
        }
        return render(request, template_name="rbac/password_change.html", context=context)

    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            cleaned_data = form.clean()
            name = cleaned_data.get("username")
            old_pwd = cleaned_data.get("old_password")
            new_pwd = cleaned_data.get("new_password")
            try:
                user = UserInfo.objects.get(name=name, password=old_pwd)
                user.password = new_pwd
                user.save(update_fields=["password"])
                form.success = True
            except UserInfo.DoesNotExist as ex:
                form.error_msg = "原密码错误!"

            return render(request, 'rbac/password_change.html', {'form': form})

        return render(request, 'rbac/password_change.html', {'form': form})



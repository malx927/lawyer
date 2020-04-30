from collections import OrderedDict

from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from lawyer import settings
from rbac.forms import PermissionForm, RoleForm, MultiPermissionForm
from rbac.models import Permission, Role, UserInfo
from rbac.utils import get_all_url_dict


def permission_list(request):
    """
    权限信息
    :param request:
    :return:
    """

    root_permission_list = []

    permissions = Permission.objects.filter(pid__isnull=True).order_by('sort')

    root_permission_queryset = permissions.values('id', 'title', 'url', 'name', 'sort', 'is_menu')
    root_permission_dict = {}
    for item in root_permission_queryset:
        item['children'] = []
        root_permission_list.append(item)
        root_permission_dict[item['id']] = item

    node_permission_list = Permission.objects.filter(pid__in=permissions).order_by('sort').values('id', 'title', 'url', 'name', 'sort', 'is_menu', 'pid', 'pid__title')
    for node in node_permission_list:
        pid = node['pid']
        root_permission_dict[pid]['children'].append(node)
    # print(root_permission_list)
    context = {
        'permissions': root_permission_list,
    }
    return render(request, template_name='rbac/permission_list.html', context=context)


def permission_add(request):
    """
    添加权限
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = PermissionForm()
    else:
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:permission-list'))
    return render(request, 'rbac/permission_change.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :return:
    """
    obj = Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('权限不存在')

    if request.method == 'GET':
        form = PermissionForm(instance=obj)
    else:
        form = PermissionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:permission-list'))
    return render(request, 'rbac/permission_change.html', {'form': form})


def permission_del(request, pk):
    """
    删除权限
    :param request:
    :return:
    """
    Permission.objects.filter(id=pk).delete()
    return redirect(request.META['HTTP_REFERER'])


def permission_batch(request):
    """
    批量操作权限
    :param request:
    """
    post_type = request.GET.get('type')

    MultiPermissionFormSet = formset_factory(MultiPermissionForm, extra=0)
    add_formset = None
    update_formset = None

    if request.method == 'POST' and post_type == 'add':
        formset = MultiPermissionFormSet(request.POST)
        if not formset.is_valid():
            add_formset = formset
        else:
            for row_dict in formset.cleaned_data:
                row_dict.pop('id')
                url = row_dict.pop("url")
                Permission.objects.update_or_create(defaults=row_dict, url=url)

    if request.method == 'POST' and post_type == 'update':
        formset = MultiPermissionFormSet(request.POST)
        if formset.is_valid():
            for row_dict in formset.cleaned_data:
                permission_id = row_dict.pop('id')
                Permission.objects.filter(id=permission_id).update(**row_dict)
        else:
            update_formset = formset

    permissions = Permission.objects.order_by('sort').values('id', 'title', 'url', 'name', 'pid_id', 'is_menu', 'icon', 'sort')
    permisssion_dict = OrderedDict()
    for per in permissions:
        permisssion_dict[per['name']] = per
    permission_name_set = set(permisssion_dict.keys())

    router_dict = get_all_url_dict(ignore_namespace_list=settings.IGNORE_NAMESPACE_LIST)
    for row in permissions:
        name = row['name']
        if name in router_dict:
            router_dict[name].update(row)
    router_name_set = set(router_dict.keys())

    # 需要新建：数据库无、路由有
    if not add_formset:
        add_name_list = router_name_set - permission_name_set
        add_formset = MultiPermissionFormSet(
            initial=[row for name, row in router_dict.items() if name in add_name_list])

    # 需要删除：数据库有、路由无
    destroy_name_list = permission_name_set - router_name_set
    destroy_formset = MultiPermissionFormSet(
        initial=[row for name, row in permisssion_dict.items() if name in destroy_name_list])

    # 需要更新：数据库有、路由有
    if not update_formset:
        update_name_list = permission_name_set.intersection(router_name_set)
        update_formset = MultiPermissionFormSet(
            initial=[row for name, row in router_dict.items() if name in update_name_list])

    return render(
        request,
        'rbac/permission_batch.html',
        {
            'destroy_formset': destroy_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )


def permission_auth(request):
    """权限分配"""
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        # 更新选择用户所拥有的角色
        user = UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    users = UserInfo.objects.all()
    # ############################## 角色信息 ##########################
    # 当前用户拥有的角色
    user_has_roles = UserInfo.objects.filter(id=uid).values('id', 'roles')
    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    # 所有的角色
    roles = Role.objects.all()

    # ############################## 权限信息 ##########################
    all_menu_list = []

    if rid:
        role_has_permissions = Role.objects.filter(id=rid, permissions__id__isnull=False).values('id', 'permissions')
    elif uid and not rid:
        user = UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.filter(permissions__id__isnull=False).values('id', 'permissions')
    else:
        role_has_permissions = []

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    # 根权限
    root_permission = Permission.objects.filter(pid__isnull=True).values('id', 'title')
    root_permission_dict = {}
    for per in root_permission:
        per['children'] = []
        nid = per['id']
        root_permission_dict[nid] = per
        all_menu_list.append(per)

    # 子权限
    node_permission = Permission.objects.filter(pid__isnull=False).values('id', 'title', 'pid_id')
    for per in node_permission:
        pid = per['pid_id']
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'rbac/permission_auth.html',
        {
            'users': users,
            'roles': roles,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'all_menu_list': all_menu_list,
            'uid': uid,
            'rid': rid
        }
    )


def role_list(request):
    """
    角色管理
    """
    form = RoleForm()
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('rbac:role-list'))
    roles = Role.objects.all().order_by('-id')
    return render(request, 'rbac/role_list.html', {'roles': roles, 'form': form})


def role_edit(request, pk):
    """
    编辑角色
    :param request:
    :param pk:
    """
    obj = Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleForm(instance=obj)
    else:
        form = RoleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

        return redirect(reverse('rbac:role-list'))

    roles = Role.objects.all().order_by('-id')
    return render(request, 'rbac/role_list.html', {'roles': roles, 'form': form})


def role_del(request, pk):
    """
    删除角色
    :param request:
    :param pk:
    """
    Role.objects.filter(id=pk).delete()
    return redirect(reverse('rbac:role-list'))

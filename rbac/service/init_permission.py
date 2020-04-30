#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf import settings
from django.db.models import F

from rbac.models import Permission


def init_permission(user, request):
    """
    用户权限初始化
    :param user:
    :param request:
    :return:
    """
    # 根据角色获取所有权限

    if user.is_superuser:
        permission_list = Permission.objects.all().order_by("sort")\
            .values(per_id=F('id'), per_title=F('title'), per_url=F('url'), per_name=F('name'), per_icon=F('icon'), per_sort=F('sort'),
                    per_pid_id=F('pid_id'), per_pid__url=F('pid__url'), per_pid__name=F('pid__name'), per_is_menu=F('is_menu'),
                    per_pid__title=F('pid__title'), per_pid__icon=F('pid__icon'), per_pid__sort=F('pid__sort')
                    ).distinct()
    else:
        permission_list = user.roles.filter(permissions__id__isnull=False).order_by("permissions__sort")\
            .values(per_id=F('permissions__id'), per_title=F('permissions__title'), per_url=F('permissions__url'),
                    per_name=F('permissions__name'), per_icon=F('permissions__icon'), per_sort=F('permissions__sort'), per_is_menu=F('permissions__is_menu'),
                    per_pid_id=F('permissions__pid_id'), per_pid__url=F('permissions__pid__url'), per_pid__name=F('permissions__pid__name'),
                    per_pid__title=F('permissions__pid__title'), per_pid__icon=F('permissions__pid__icon'), per_pid__sort=F('permissions__pid__sort')
                    ).distinct()

    menu_dict = {}
    permission_dict = {}
    for item in permission_list:
        # 处理权限
        permission_dict[item['per_name']] = {
            'id': item['per_id'],
            'title': item['per_title'],
            'url': item['per_url'],
            'pid': item['per_pid_id'],
            'pid_url': item['per_pid__url'],
            'pid_name': item['per_pid__name'],
        }

        # 处理菜单
        is_menu = item['per_is_menu']
        pid = item['per_pid_id']

        if is_menu == 1 and not pid:
            menu_id = item['per_id']
            if menu_id not in menu_dict:
                menu_dict[item['per_id']] = {
                    'title': item['per_title'],
                    'url': item['per_url'],
                    'icon': item['per_icon'],
                    'sort': item['per_sort'],
                    'children': [],
                }

    for item in permission_list:
        menu_id = item['per_pid_id']
        if not menu_id:
            continue

        menu_node = {
            'id': item['per_id'],
            'title': item['per_title'],
            'url': item['per_url'],
            'icon': item['per_icon'],
            'is_menu': item['per_is_menu'],
        }

        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(menu_node)

    # print(menu_dict)
    # print(permission_list)
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict

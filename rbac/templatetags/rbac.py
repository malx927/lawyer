#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.template import Library
from django.conf import settings
from collections import OrderedDict
from django.templatetags.static import static
from django.utils.html import format_html

register = Library()


@register.inclusion_tag('rbac/include/sidebar.html')
def menu(request):
    """生成菜单"""
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    menu_dict_sort = sorted(menu_dict.items(), key=lambda x: x[1]["sort"])

    ordered_dict = OrderedDict()
    for key, val in menu_dict_sort:
        current_permission_pid = getattr(request, "current_permission_pid", None)
        if current_permission_pid:
            if key == str(request.current_permission_pid):
                val['class'] = 'green'
            for per in val['children']:
                if per['id'] == request.current_permission_pid:
                    val['class'] = 'green'
        ordered_dict[key] = val

    return {
        'menu_dict': ordered_dict
    }


# @register.inclusion_tag('rbac/breadcrumb.html')
# def breadcrumb(request):
#     """生成路径导航"""
#     return {
#         'breadcrumb_list': request.current_breadcrumb_list
#     }


@register.filter
def has_permission(request, name):
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

    is_superuser = request.session.get("is_superuser", None)
    if is_superuser:
        return True

    if name in permission_dict:
        return True


@register.simple_tag
def get_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()


@register.filter
def boolean_icon(field_val):
    icon_url = static('rbac/img/icon-%s.svg' % {True: 'yes', False: 'no', None: 'unknown'}[field_val])
    return format_html('<img src="{}" alt="{}" />', icon_url, field_val)
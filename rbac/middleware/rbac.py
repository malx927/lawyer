#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.conf import settings
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        验证用户
        :param request:
        :return:
        """
        # 1. 获取白名单，让白名单中的所有url和当前访问url匹配
        # print(":::::::", request.path_info)
        for reg in settings.PERMISSION_VALID_URL:
            if re.match(reg, request.path_info):
                return None

        # 2. 获取权限
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        is_superuser = request.session.get("is_superuser", None)
        if not is_superuser and not permission_dict:
            return HttpResponse('无权限信息，请重新登录')

        flag = False

        # 3. 对用户请求的url进行匹配
        request.current_breadcrumb_list = [
            {'title': '首页', 'url': '#'}
        ]

        for name, item in permission_dict.items():
            url = item['url']
            regex = "^%s$" % (url,)
            if re.match(regex, request.path_info):
                flag = True
                pid = item['pid']
                pid_name = item['pid_name']
                pid_url = item['pid_url']
                if pid:
                    request.current_permission_pid = item['pid']
                    request.current_breadcrumb_list.extend([
                        {'title': permission_dict[pid_name]['title'], 'url': pid_url},
                        {'title': item['title'], 'url': url, 'class': 'active'}
                    ])
                else:
                    request.current_permission_pid = item['id']
                    request.current_breadcrumb_list.append(
                        {'title': item['title'], 'url': url, 'class': 'active'}
                    )
                break

        if not flag and not is_superuser:
            return JsonResponse({'status': False, 'error': '无权访问'})

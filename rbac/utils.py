from collections import OrderedDict

from django.templatetags.static import static
from django.urls import RegexURLResolver, RegexURLPattern
from django.utils.html import format_html
from django.utils.module_loading import import_string

from lawyer import settings


def boolean_icon(field_val):
    icon_url = static('admin/img/icon-%s.svg' % {True: 'yes', False: 'no', None: 'unknown'}[field_val])
    return format_html('<img src="{}" alt="{}" />', icon_url, field_val)


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    for item in urlpatterns:
        if isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)
        else:

            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name,)
            else:
                name = item.name
            if not item.name:
                raise Exception('URL路由中必须设置name属性')

            url = pre_url + item._regex
            url_ordered_dict[name] = {'name': name, 'url': url.replace('^', '').replace('$', '')}


def get_all_url_dict(ignore_namespace_list=None):
    """
    获取路由中
    :return:
    """
    ignore_list = ignore_namespace_list or []
    url_ordered_dict = OrderedDict()

    md = import_string(settings.ROOT_URLCONF)

    urlpatterns = []

    for item in md.urlpatterns:

        if isinstance(item, RegexURLResolver) and item.namespace in ignore_list:
            continue
        urlpatterns.append(item)

    recursion_urls(None, "/", urlpatterns, url_ordered_dict)
    return url_ordered_dict


def get_menu_children(request):
    current_permission_pid = request.current_permission_pid
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    menu = menu_dict.get(str(current_permission_pid), None)

    if menu:
        children_menus = menu.get("children", None)
    else:
        children_menus = None

    return children_menus
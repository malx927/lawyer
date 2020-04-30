from django.conf.urls import url, include

from rbac.account import user_list, user_add, user_edit, user_del
from .views import permission_list, permission_add, permission_edit, permission_del, role_list, role_edit, role_del, \
    permission_auth, permission_batch

urlpatterns = [
    url(r'^permission_list/$', permission_list, name="permission-list"),
    url(r'^permission/add/$', permission_add, name='permission-add'),
    url(r'^permission/edit/(?P<pk>\d+)/$', permission_edit, name='permission-edit'),
    url(r'^permission/del/(?P<pk>\d+)/$', permission_del, name='permission-del'),
    url(r'^permission/auth/$', permission_auth, name='permission-auth'),
    url(r'^permission/batch/$', permission_batch, name='permission-batch'),

    url(r'^role/list/$', role_list, name='role-list'),
    url(r'^role/edit/(?P<pk>\d+)/$', role_edit, name='role-edit'),
    url(r'^role/del/(?P<pk>\d+)/$', role_del, name='role-del'),

    url(r'^user/list/$', user_list, name='user-list'),
    url(r'^user/add/$', user_add, name='user-add'),
    url(r'^user/edit/(?P<pk>\d+)/$', user_edit, name='user-edit'),
    url(r'^user/del/(?P<pk>\d+)/$', user_del, name='user-del'),

]
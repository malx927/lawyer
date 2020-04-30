from django.contrib import admin

from adm.models import SpecialField
from .models import *


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'name', 'pid', 'sort']
    list_editable = ['url', 'name']


class SpecialInline(admin.TabularInline):
    model = SpecialField


class UserInfoAdmin(admin.ModelAdmin):
    inlines = [
        SpecialInline,
    ]


admin.site.register(Permission, PermissionAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Role)
admin.site.register(Menu)
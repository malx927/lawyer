# -*-coding:utf-8-*-

import datetime
import os
from django.utils import timezone
from rest_framework.fields import SerializerMethodField
from rest_framework.permissions import AllowAny
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from rbac.models import UserInfo

__author__ = 'malixin'


class UserInfoSerializer(serializers.ModelSerializer):
    post_name = SerializerMethodField()
    superuser = SerializerMethodField()
    active = SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = [
           'id', 'name', 'real_name', 'telephone', 'email', 'post_name', 'superuser', 'active'
        ]

    def get_post_name(self, obj):
        return obj.get_post_display() if obj.get_post_display() is not None else '无'

    def get_superuser(self, obj):
        return "超级管理员" if obj.is_superuser is not None else '否'

    def get_active(self, obj):
        return "有效" if obj.is_active is not None else '否'

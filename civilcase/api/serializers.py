# -*-coding:utf-8-*-

import datetime
import os
from django.utils import timezone
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework import serializers

from civilcase.models import CivilDetail, CivilNaturePerson

__author__ = 'malixin'


class CivilDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CivilDetail
        fields = [
            'id', 'case_id'
        ]


class CivilNaturePersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = CivilNaturePerson
        fields = [
            'name'
        ]


# class LawsuitSchemeSerializer(serializers.ModelSerializer):
#     civil_name = serializers.SerializerMethodField()
#     proxy_phase = serializers.SerializerMethodField()
#
#     class Meta:
#         model = LawsuitScheme
#         fields = [
#            'civil_name', 'legal_status', 'proxy_phase', 'agent', 'judge_date',
#            'judge_code', 'judge_result', 'court_name', 'court_tel', 'court_judge', 'case_type', 'lawyer',
#         ]

    # def get_civil_name(self, obj):
    #     try:
    #         civil = Civil.objects.get(id=obj.civil_id)
    #         serializer = CivilSerializer(civil)
    #         return serializer.data
    #     except Civil.DoesNotExist as ex:
    #         return None
    #
    # def get_proxy_phase(self, obj):
    #     levels = obj.trial_level.all()
    #     list_level = [level.name for level in levels]
    #     return ','.join(list_level)


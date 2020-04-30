# -*-coding:utf-8-*-

from rest_framework.fields import SerializerMethodField

from rest_framework import serializers

from calculator.models import AreaCode, IndusAverWage

__author__ = 'malixin'


class AreaCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaCode
        fields = [
            'code',
            'name',
        ]


class IndusAverWageSerializer(serializers.ModelSerializer):
    """分行业城镇单位在岗职工平均工资"""
    class Meta:
        model = IndusAverWage
        fields = [
            'province',
            'industry',
            'years',
            'aver_wage',
            'day_aver_wage',
        ]

#-*-coding:utf-8-*-
import datetime

from django.db.models import Sum, Count, Q, F, DecimalField, FloatField, IntegerField
from django.db import connection
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from adm.api.serializers import UserInfoSerializer
from rbac.models import UserInfo

__author__ = 'malixin'


class UserInfoDetailAPIView(RetrieveAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [AllowAny]


# class UpdateLossView(RetrieveUpdateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = DogLossDetailSerializer
#     queryset = DogLoss.objects.all()
#
#
# class UpdateOwnerView(RetrieveUpdateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = DogOwnerDetailSerializer
#     queryset = DogOwner.objects.all()
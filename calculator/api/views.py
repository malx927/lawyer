# -*-coding:utf-8-*-
import datetime

from calculator.api.serializers import AreaCodeSerializer, IndusAverWageSerializer
from lawyer import settings

__author__ = 'malixin'


from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from calculator.models import AreaCode, IndusAverWage, ResIncomeExpend


class AreaCodeListAPIView(ListAPIView):
    """
    地区编码
    """
    permission_classes = [AllowAny]
    queryset = AreaCode.objects.all()
    serializer_class = AreaCodeSerializer
    pagination_class = None

    def get_queryset(self):
        code = self.request.GET.get("code", None)
        if code and len(code) == 2:
            return AreaCode.objects.extra(where=['left(code,2)=%s', 'length(code)=4'], params=[code])
        elif code and len(code) == 4:
            return AreaCode.objects.extra(where=['left(code,4)=%s', 'length(code)=6'], params=[code])
        else:
            return AreaCode.objects.extra(where=['length(code)=2'])


class IndusAverWageAPIView(APIView):
    """
    行业工资标准
    """
    def get(self, request, *args, **kwargs):
        indust_id = request.GET.get("indust_id", None)
        province = request.GET.get("province", None)
        court_province = request.GET.get("court_province", None)

        indust_wage = IndusAverWage.objects.filter(industry_id=int(indust_id), province_id=province).order_by("-years").first()
        court_indust_wage = IndusAverWage.objects.filter(industry_id=int(indust_id), province_id=court_province).order_by("-years").first()

        result = {
            "success": "false",
        }
        if indust_wage and court_indust_wage:
            if indust_wage.day_aver_wage < court_indust_wage.day_aver_wage:
                indust_wage = court_indust_wage

            serializer = IndusAverWageSerializer(indust_wage)
            result["success"] = "true"
            result["result"] = serializer.data
            return Response(result)
        else:
            result["error_msg"] = "无法获取行业工资标准"
            return Response(result)


class IndusNurseWageAPIView(APIView):
    """
    行业护理日工资标准
    """
    def get(self, request, *args, **kwargs):
        calculator = request.session.get(settings.CALCULATOR_SESSION_KEY)
        province = calculator.get("province", None)
        court_province = calculator.get("court_province", None)

        indust_wage = IndusAverWage.objects.filter(province_id=province, industry__standard=1).order_by("-years").first()
        court_indust_wage = IndusAverWage.objects.filter(province_id=court_province, industry__standard=1).order_by("-years").first()

        result = {
            "success": "false",
        }
        if indust_wage and court_indust_wage:
            serializer = IndusAverWageSerializer(indust_wage)
            result["success"] = "true"
            result["result"] = serializer.data
            return Response(result)
        else:
            result["error_msg"] = "无法获取护理工资标准"
            return Response(result)


class FuneralExpenseAPIView(APIView):
    """丧葬费"""
    def get(self, request, *args, **kwargs):
        dead = request.GET.get("dead", None)
        province = request.GET.get("province", None)
        court_province = request.GET.get("court_province", None)

        result = {
            "success": "false",
        }
        if dead == "1":
            # 丧葬费 id = 6 (丧葬费)
            last_year = datetime.datetime.now().year - 1
            res_inc_exp = ResIncomeExpend.objects.filter(inc_exp_item_id=6, province_id=province, years=last_year).first()
            court_res_inc_exp = ResIncomeExpend.objects.filter(inc_exp_item_id=6, province_id=court_province, years=last_year).first()

            if res_inc_exp and court_res_inc_exp:
                if res_inc_exp.total_money >= court_res_inc_exp.total_money:
                    result["success"] = "true"
                    result["funeral_expense"] = res_inc_exp.total_money
                else:
                    result["success"] = "true"
                    result["funeral_expense"] = court_res_inc_exp.total_money
            else:
                result["funeral_expense"] = 0

        return Response(result)



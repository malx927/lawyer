#-*-coding:utf-8-*-

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


from .serializers import *
from civilcase.models import CivilDetail, CivilNaturePerson

__author__ = 'malixin'


class CivilDetailAPIView(RetrieveAPIView):
    """
    案件执行情况详情
    """
    permission_classes = [AllowAny]
    queryset = CivilDetail.objects.all()
    serializer_class = CivilDetailSerializer


class CivilNaturePersonAPIView(ListAPIView):
    """
    案件执行人员列表
    """
    permission_classes = [AllowAny]
    queryset = CivilNaturePerson.objects.all()
    serializer_class = CivilNaturePersonSerializer

    def get_queryset(self):
        case_detail_id = self.request.GET.get("case_detail_id", None)
        return CivilNaturePerson.objects.filter(case_id=case_detail_id)

#
# class CivilCaseDetailAPIView(RetrieveAPIView):
#     """
#     案件代理详情
#     """
#     permission_classes = [AllowAny]
#     queryset = CivilCase.objects.all()
#     serializer_class = CivilCaseSerializer
#
#
# class LawsuitSchemeDetailAPIView(RetrieveAPIView):
#     """
#     诉讼方案
#     """
#     permission_classes = [AllowAny]
#     queryset = LawsuitScheme.objects.all()
#     serializer_class = LawsuitSchemeSerializer

#
# class AreaCodeListAPIView(ListAPIView):
#     """
#     地区编码
#     """
#     permission_classes = [AllowAny]
#     queryset = AreaCode.objects.all()
#     serializer_class = AreaCodeSerializer
#     pagination_class = None
#
#     def get_queryset(self):
# #         code = self.request.GET.get("code", None)
#         if code and len(code) == 2:
#             return AreaCode.objects.extra(where=['left(code,2)=%s', 'length(code)=4'], params=[code])
#         elif code and len(code) == 4:
#             return AreaCode.objects.extra(where=['left(code,4)=%s', 'length(code)=6'], params=[code])
#         else:
#             return AreaCode.objects.extra(where=['length(code)=2'])

# #狗配种
# class DogbreedListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = DogBreed.objects.all()
#     serializer_class = DogbreedListSerializer
#     def get_queryset(self):
#         return  DogBreed.objects.filter(is_show=1)
#
# class DogBreedDetailAPIView(RetrieveAPIView):
#     queryset = DogBreed.objects.all()
#     serializer_class = DogBreedDetailSerializer
#     permission_classes = [AllowAny]
#
#
# class DogLossDetailAPIView(RetrieveAPIView):
#     queryset = DogLoss.objects.all()
#     serializer_class = DogLossDetailSerializer
#     permission_classes = [AllowAny]
#
# #寻找宠物主人
# class DogOwnerListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = DogOwner.objects.all()
#     serializer_class = DogOwnerSerializer
#     def get_queryset(self):
#         return  DogOwner.objects.filter(is_show=1)
#
#
# #宠物领养
# class DogadoptListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = DogAdoption.objects.all()
#     serializer_class = DogadoptListSerializer
#     def get_queryset(self):
#         return  DogAdoption.objects.filter(is_show=1)
#
#
# #宠物送养
# class DogdeliveryListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = DogDelivery.objects.all()
#     serializer_class = DogdeliverySerializer
#     def get_queryset(self):
#         return  DogDelivery.objects.filter(is_show=1)
#
#
# class DogdeliveryDeliveryAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = DogDelivery.objects.all()
#     serializer_class = DogdeliveryDetailSerializer
#
# #寻找宠物主人
# class DogBuyListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = DogBuy.objects.all()
#     serializer_class = DogBuySerializer
#     def get_queryset(self):
#         return  DogBuy.objects.filter(is_show=1)
#
#
# class DogSaleListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = DogSale.objects.all()
#     serializer_class = DogSaleSerializer
#     def get_queryset(self):
#         return  DogSale.objects.filter(is_show=1)
#
#
# #新手课堂
# class DogFreshmanListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = Freshman.objects.all()
#     serializer_class = DogfreshmanSerializer
#     def get_queryset(self):
#         return  Freshman.objects.filter(is_show=1)
#
#
# #加盟宠物医疗机构
# class DogInstitutionListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = Doginstitution.objects.all()
#     serializer_class = DogInstitutionSerializer
#     def get_queryset(self):
#         return  Doginstitution.objects.filter(is_show=1)
#
#
# class SwiperImageListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = SwiperImage.objects.all()
#     serializer_class = SwiperImageListSerializer
#
#     def get_queryset(self):
#         return SwiperImage.objects.filter(is_show=1)
#
#
# class AreaCodeListAPIView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = AreaCode.objects.all()
#     serializer_class = CodeProvinceSerializer
#     pagination_class = None
#
#     def get_queryset(self):
#         return AreaCode.objects.extra(where=['length(code)=2'])
#
#
#
# class MyInfoListAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         type = request.GET.get('type',None)
#         openid = request.session.get('openid',None)
#         print(type,openid)
#         if type == 'loss' and  openid:
#             queryset_list = DogLoss.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogLossSerializer(queryset_list, many=True)
#             print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         elif type=='owner' and openid:
#             queryset_list = DogOwner.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogOwnerSerializer(queryset_list, many=True)
#             #print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         elif type=='breed' and openid:
#             queryset_list = DogBreed.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogbreedListSerializer(queryset_list, many=True)
#             #print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         elif type=='adopt' and openid:
#             queryset_list = DogAdoption.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogadoptListSerializer(queryset_list, many=True)
#             #print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         elif type=='delivery' and openid:
#             queryset_list = DogDelivery.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogdeliverySerializer(queryset_list, many=True)
#             #print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         elif type=='sale' and openid:
#             queryset_list = DogSale.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogSaleSerializer(queryset_list, many=True)
#             #print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         elif type=='buy' and openid:
#             queryset_list = DogBuy.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogBuySerializer(queryset_list, many=True)
#             #print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         elif type=='institution' and openid:
#             queryset_list = Doginstitution.objects.filter(is_show=1).filter(openid=openid).order_by('-create_time')
#             serializer = DogInstitutionSerializer(queryset_list, many=True)
#             #print(serializer.data)
#             resp = {
#                 'results':serializer.data
#             }
#             return Response(resp)
#         else:
#             resp = {
#                 'results':[]
#             }
#             return Response(resp)
#
#
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
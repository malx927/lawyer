from django.db import models

from baseinfo.constants import IS_ASSIGN
from rbac.models import UserInfo


class ConsultantUnit(models.Model):
    """顾问单位"""
    SCHEME = (
        (1, '方案A'),
        (2, '方案B'),
        (3, '方案C'),
        (4, '方案D'),
    )
    TYPE = (
        (0, '企业'),
        (1, '个人'),
    )
    unit_name = models.CharField(verbose_name="企业名称/姓名", max_length=120)
    unit_type = models.IntegerField(verbose_name="类型", choices=TYPE, default=0)
    person = models.CharField(verbose_name="联系人员", max_length=64, blank=True, default="")
    sign_begin = models.DateField(verbose_name="签约开始时间")
    sign_end = models.DateField(verbose_name="截止时间")
    telephone = models.CharField(verbose_name="联系电话", max_length=32)
    scheme = models.IntegerField(verbose_name="签约方案", choices=SCHEME)
    address = models.CharField(verbose_name="地址", max_length=120)
    lawyer = models.ManyToManyField(verbose_name="律师姓名", to=UserInfo, blank=True)
    is_assign = models.IntegerField(verbose_name="分配确认", choices=IS_ASSIGN, blank=True, null=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "顾问单位"
        verbose_name_plural = verbose_name

    def get_lawyer_list(self):
        lawyer_list = []
        for user in self.lawyer.all():
            lawyer_list.append(user.real_name)
        print(lawyer_list)
        return ",".join(lawyer_list)

from django.db import models
from rbac.models import UserInfo


class Office(models.Model):
    """律师事务所"""
    name = models.CharField(verbose_name='名称', max_length=120)
    credit_code = models.CharField(verbose_name='统一社会信用代码', max_length=20, blank=True, null=True)
    address = models.CharField(verbose_name='律所所在市', max_length=150, blank=True)
    category = models.IntegerField(verbose_name='律师类型', choices=((1, '市直'), (2, '个人所')), default=1)
    legal_person = models.CharField(verbose_name='法定代表人', max_length=20, blank=True, null=True)
    telephone = models.CharField(verbose_name='联系电话', max_length=30, blank=True, null=True)
    position = models.CharField(verbose_name='所在地', max_length=150, blank=True)
    bank = models.CharField(verbose_name='开户行', max_length=60, blank=True, null=True)
    account = models.CharField(verbose_name='银行账号', max_length=20, blank=True, null=True)
    update_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '律师事务所'
        verbose_name_plural = '律师事务所'

    def __str__(self):
        return self.name


class SpecialField(models.Model):
    """优势类型"""
    user = models.ForeignKey(verbose_name="姓名", to=UserInfo, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="优势", max_length=128)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "优势类型"
        verbose_name_plural = verbose_name


class ProfessionalTitle(models.Model):
    """职称"""
    user = models.ForeignKey(verbose_name="姓名", to=UserInfo, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="职称", max_length=128)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "职称"
        verbose_name_plural = verbose_name


class SocialService(models.Model):
    """社会任职"""
    user = models.ForeignKey(verbose_name="姓名", to=UserInfo, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="任职", max_length=128)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "社会任职"
        verbose_name_plural = verbose_name
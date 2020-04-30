# coding=utf-8
from django.db import models

from calculator.constants import SUPPORTED_TYPE, RELATION_TYPE


class AreaCode(models.Model):
    """
    地区编码
    """
    code = models.CharField(verbose_name='地区编码', primary_key=True, max_length=18)
    name = models.CharField(verbose_name='地区名称', max_length=50)

    class Meta:
        verbose_name = '地区编码表'
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return self.name


class IncomeExpendItem(models.Model):
    """居民人均收支项"""
    name = models.CharField(verbose_name="项目名称", max_length=128)

    class Meta:
        verbose_name = '居民人均收支项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Industry(models.Model):
    """行业管理"""
    name = models.CharField(verbose_name="行业名称", max_length=128)
    standard = models.IntegerField(verbose_name="护理标准", choices=((0, '否'), (1, '是')), default=0)

    class Meta:
        verbose_name = '行业管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}({})".format(self.name, self.id)


class IndusAverWage(models.Model):
    """行业城镇单位在岗职工平均工资"""
    province = models.ForeignKey(AreaCode, verbose_name="省份", on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, verbose_name="行业名称", on_delete=models.CASCADE)
    years = models.IntegerField(verbose_name="年份", )
    aver_wage = models.DecimalField(verbose_name="平均工资", max_digits=10, decimal_places=2, default=0)
    day_aver_wage = models.DecimalField(verbose_name="平均日工资", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = '行业平均工资'
        verbose_name_plural = verbose_name
        ordering = ["-years", "province", "industry"]

    def __str__(self):
        return "{}{}".format(self.province.name, self.industry.name)


class ResIncomeExpend(models.Model):
    """居民人均收支情况表"""
    province = models.ForeignKey(AreaCode, verbose_name="省份", on_delete=models.CASCADE)
    inc_exp_item = models.ForeignKey(IncomeExpendItem, verbose_name="收支项", on_delete=models.CASCADE)
    years = models.IntegerField(verbose_name="年份", )
    total_money = models.DecimalField(verbose_name="总金额", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = '居民人均收支情况表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}{}".format(self.province.name, self.inc_exp_item.name)


class CalculatorUser(models.Model):
    """计算人员"""
    name = models.CharField(verbose_name="计算人员", max_length=32, default="anyone")

    class Meta:
        verbose_name = '计算人员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SupportedPerson(models.Model):
    """被抚养人"""
    CHOICES = (
              ('', '----'),
              (1, '有'),
              (0, '无'),
              )
    user = models.ForeignKey(CalculatorUser, verbose_name="当事人", on_delete=models.CASCADE)
    relation_type = models.IntegerField(verbose_name="与当事人关系", choices=SUPPORTED_TYPE)
    action_ability = models.IntegerField(verbose_name="是否有残障", choices=CHOICES, default=0)
    is_income = models.IntegerField(verbose_name="是否有收入", choices=CHOICES, default=0)
    relation_age = models.IntegerField(verbose_name="年龄")

    class Meta:
        verbose_name = '被抚养人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_relation_type_display()


class RelationPerson(models.Model):
    """直系亲属"""
    CHOICES = (
          ('', '----'),
          (1, '有'),
          (0, '无'),
    )
    user = models.ForeignKey(CalculatorUser, verbose_name="当事人", on_delete=models.CASCADE)
    relation_type = models.IntegerField(verbose_name="与当事人关系", choices=RELATION_TYPE)
    action_ability = models.IntegerField(verbose_name="是否有残障", choices=CHOICES, default=0)
    is_income = models.IntegerField(verbose_name="是否有收入", choices=CHOICES, default=0)
    relation_age = models.IntegerField(verbose_name="年龄")

    class Meta:
        verbose_name = '被抚养人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_relation_type_display()
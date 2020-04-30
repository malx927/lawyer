from django.db import models


class CivilLevel(models.Model):
    """民事案件执行阶段"""
    id = models.IntegerField(verbose_name='阶段编号', primary_key=True)
    name = models.CharField(verbose_name='阶段名称', max_length=50)

    class Meta:
        verbose_name = '案件执行阶段'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class CriminalStage(models.Model):
    """刑事案件执行阶段"""
    id = models.IntegerField(verbose_name='阶段编号', primary_key=True)
    name = models.CharField(verbose_name='阶段名称', max_length=50)

    class Meta:
        verbose_name = '刑事案件执行阶段'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class AgencyAuth(models.Model):
    """民事代理权限"""
    id = models.IntegerField(verbose_name='权限编号', primary_key=True)
    name = models.CharField(verbose_name='权限名称', max_length=50)
    explain = models.CharField(verbose_name='权限说明', max_length=200, blank=True, )

    class Meta:
        verbose_name = '代理权限'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class LegalStatus(models.Model):
    """法律地位"""
    id = models.IntegerField(verbose_name='编号', primary_key=True)
    name = models.CharField(verbose_name='法律地位', max_length=50)

    class Meta:
        verbose_name = '法律地位'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class PrivateLegalStatus(models.Model):
    """法律地位"""
    id = models.IntegerField(verbose_name='编号', primary_key=True)
    name = models.CharField(verbose_name='法律地位', max_length=50)

    class Meta:
        verbose_name = '刑自法律地位'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class CrmCivilLegalStatus(models.Model):
    """法律地位"""
    id = models.IntegerField(verbose_name='编号', primary_key=True)
    name = models.CharField(verbose_name='法律地位', max_length=50)

    class Meta:
        verbose_name = '刑附民法律地位'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class Post(models.Model):
    """用户类型"""
    id = models.IntegerField(verbose_name='编号', primary_key=True)
    name = models.CharField(verbose_name='类型名称', max_length=50)

    class Meta:
        verbose_name = '用户类型'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

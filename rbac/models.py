import datetime

from django.db import models
from django.utils import timezone
from enum import Enum, unique


# class Post(Enum):
#     """律师类型"""
#     Major = 1
#     Part = 2
#     Practs = 3
#     Manager = 4
#     Administrative = 5
#     Partner = 6
#     Student = 7
#
#
# POST = (
#     (Post.Major.value, '专职律师'),
#     (Post.Part.value, '兼职律师'),
#     (Post.Practs.value, '实习律师'),
#     (Post.Manager.value, '客户经理'),
#     (Post.Administrative.value, '行政人员'),
#     (Post.Partner.value, '律所合伙人'),
#     (Post.Student.value, '学员'),
# )
from baseinfo.models import Post


class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(verbose_name='菜单', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=64)
    url = models.CharField(verbose_name='链接地址', max_length=128, unique=True)
    name = models.CharField(verbose_name='别名', max_length=64, unique=True, null=False, blank=False)
    pid = models.ForeignKey(verbose_name='父级权限', to='Permission', related_name='ps', null=True, blank=True,
                            limit_choices_to={'pid__isnull': True}, on_delete=models.SET_NULL)
    is_menu = models.BooleanField(verbose_name='菜单', default=False)
    icon = models.CharField(verbose_name='图标', max_length=64, blank=True, null=True)
    sort = models.IntegerField(verbose_name='排序', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限信息'
        verbose_name_plural = verbose_name


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='登录名', max_length=32, unique=True)
    real_name = models.CharField(verbose_name='姓名', max_length=32)
    gender = models.IntegerField(verbose_name="性别", choices=((1, "男"), (2, "女")), blank=True, null=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    telephone = models.CharField(verbose_name='手机', max_length=16)
    email = models.CharField(verbose_name='邮箱', max_length=32, blank=True, null=True)
    post = models.ForeignKey(Post, verbose_name="用户类型", on_delete=models.SET_NULL, null=True)
    job = models.CharField(verbose_name="职务", max_length=64, blank=True, null=True)
    # years = models.CharField(verbose_name="执业年限", max_length=24, blank=True, null=True)
    job_time = models.DateField(verbose_name="执业时间", blank=True, null=True)
    license_num = models.CharField(verbose_name="律师证号", max_length=32, blank=True, null=True)
    prof_title = models.CharField(verbose_name="律师职称", max_length=64, blank=True, null=True)
    is_superuser = models.BooleanField(verbose_name='超级管理员', default=False)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    date_joined = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='最近登录时间', blank=True, null=True)
    is_update = models.BooleanField(verbose_name="是否完善", default=False)
    roles = models.ManyToManyField(verbose_name='所属角色', to='Role', blank=True)

    def __str__(self):
        return self.real_name if self.real_name else self.name

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def practice_years(self):
        if self.job_time:
            return datetime.datetime.now().year - self.job_time.year
        else:
            return 0
import datetime

from django.db import models
from django.db.models import Max

from baseinfo.constants import SEX_CHOICES, INFO_TYPE, CASE_PROPERTY, ORG_LEGAL_STATUS, AGENT_TYPE, ASK_TARGET, \
    EVI_TYPE, EVI_SOURCE, JUDGE_RESULT, IS_ASSIGN
from baseinfo.models import LegalStatus, AgencyAuth, CivilLevel, PrivateLegalStatus
from civilcase.utils import money_num2word
from .constants import *
from rbac.models import UserInfo


class CrimiPrivate(models.Model):
    """
    刑事自诉案件信息登记表
    """
    case_name = models.CharField(verbose_name="案件名称", max_length=1200)
    accusation = models.CharField(verbose_name='所涉罪名', max_length=200, )
    info_type = models.IntegerField(verbose_name='信息类型',  default=1, choices=INFO_TYPE)
    case_prop = models.IntegerField(verbose_name="案件性质", choices=CASE_PROPERTY, default=0)
    org_legal_status = models.IntegerField(verbose_name="原审法律地位", choices=ORG_PRIVATE_LEGAL_STATUS, blank=True, null=True)
    agent = models.ForeignKey(AgencyAuth, verbose_name='代理权限', blank=True, null=True)
    stage = models.ForeignKey(CivilLevel, related_name="pstages", limit_choices_to={'id__lt': 4}, verbose_name='案件所处阶段')
    commission_stage = models.ManyToManyField(CivilLevel, limit_choices_to={'id__lt': 4}, verbose_name='委托阶段', blank=True)
    total_expenses = models.DecimalField(verbose_name="代理费", max_digits=9, decimal_places=2, default=0)
    # 委托人信息(自然人)
    cli_name = models.CharField(verbose_name='委托人姓名', max_length=50, blank=True, null=True)
    cli_tel = models.CharField(verbose_name='委托人电话', max_length=50, blank=True, null=True)
    cli_relation = models.CharField(verbose_name='与当事人关系', max_length=50, blank=True, null=True)
    cli_address = models.CharField(verbose_name='住址', max_length=60, blank=True, null=True)
    cli_id_card = models.CharField(verbose_name='身份证号', max_length=50, blank=True, null=True)
    # 监护人
    guard_name = models.CharField(verbose_name='监护人姓名', max_length=30, blank=True, null=True)
    guard_tel = models.CharField(verbose_name='监护人电话', max_length=30, blank=True, null=True)
    guard_relation = models.CharField(verbose_name='与当事人关系', max_length=50, blank=True, )
    guard_address = models.CharField(verbose_name='住址', max_length=100, blank=True, null=True)
    guard_id_card = models.CharField(verbose_name='身份证号', max_length=50, blank=True, null=True)
    # 当事人信息(自然人)
    party_name = models.CharField(verbose_name='当事人姓名', max_length=50, blank=True, null=True)
    party_person_status = models.ForeignKey(PrivateLegalStatus, verbose_name="所处法律地位", blank=True, null=True)
    party_sex = models.CharField(verbose_name='性别', max_length=20, choices=SEX_CHOICES,  blank=True, null=True)
    party_birth = models.DateField(verbose_name='出生日期', blank=True, null=True)
    party_nation = models.CharField(verbose_name='民族', max_length=10, blank=True, null=True)
    party_tel = models.CharField(verbose_name='联系电话', max_length=64, blank=True, null=True)
    party_id_code = models.CharField(verbose_name='身份证号', max_length=50, blank=True, null=True)
    party_address = models.CharField(verbose_name='住址', max_length=200, blank=True, null=True)
    party_job = models.CharField(verbose_name='职业', max_length=64, blank=True, null=True)
    # 分配律师
    lawyer = models.ForeignKey(UserInfo, verbose_name='主办律师', related_name="private_lawyers", blank=True, null=True, on_delete=models.SET_NULL)
    assist = models.ForeignKey(UserInfo, verbose_name='辅助律师', related_name="private_assists", blank=True, null=True,
                               on_delete=models.SET_NULL)
    manager = models.ForeignKey(UserInfo, verbose_name='客户经理', related_name="private_managers", blank=True, null=True,
                                on_delete=models.SET_NULL)
    is_assign = models.IntegerField(verbose_name="分配确认", choices=IS_ASSIGN, blank=True, null=True,)
    user = models.ForeignKey(UserInfo, verbose_name='录入人', blank=True, null=True, on_delete=models.SET_NULL)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '刑事案件登记'
        verbose_name_plural = verbose_name
        ordering = ['-create_at']

    def __str__(self):
        return self.case_name

    def get_commission_stage(self):
        commi_stage = []
        for item in self.commission_stage.all():
            commi_stage.append(item.name)
        return ",".join(commi_stage)

    def get_total_expenses(self):
        return money_num2word(float(self.total_expenses))

    def get_birth_date(self):
        return self.create_at.year - self.party_birth.year


class CrimiPrivateHisResult(models.Model):
    """刑自历史判决结果"""
    MANNER = (
        (0, '接受'),
        (1, '不服'),
    )
    private = models.ForeignKey(CrimiPrivate, verbose_name='案件名称', on_delete=models.CASCADE)
    legal_status = models.ForeignKey(PrivateLegalStatus, verbose_name="所处法律地位", blank=True, null=True)
    stage = models.ForeignKey(CivilLevel, verbose_name='案件阶段',  limit_choices_to={'id__lt': 4},)
    court_name = models.CharField(verbose_name='法院名称', max_length=50, blank=True, null=True)
    judge_date = models.DateField(verbose_name='判决时间', max_length=20, blank=True, null=True)
    judge_code = models.CharField(verbose_name='判决编号', max_length=50, blank=True, null=True)
    judge_result = models.IntegerField(verbose_name='判决结果', choices=JUDGE_RESULT)
    judge_manner = models.IntegerField(verbose_name='是否接受', default=0, choices=MANNER)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '刑自历史判决'
        verbose_name_plural = verbose_name
        ordering = ["stage"]

    def __str__(self):
        return "{}({})".format(self.private.case_name, self.stage.name)


class CrimiPrivateDetail(models.Model):
    """案件具体执行情况"""
    STATUS = (
        (0, '未完'),
        (1, '完毕'),
    )
    DISTRIB = (
        (0, '未分配'),
        (1, '已分配'),
    )
    private = models.ForeignKey(CrimiPrivate, verbose_name='案件名称', on_delete=models.CASCADE)
    legal_status = models.ForeignKey(PrivateLegalStatus, verbose_name="所处法律地位", blank=True, null=True)
    stage = models.ForeignKey(CivilLevel, verbose_name='案件所处阶段', limit_choices_to={'id__lt': 4})
    court_name = models.CharField(verbose_name='法院名称', max_length=50, blank=True, null=True)
    court_tel = models.CharField(verbose_name='法院电话', max_length=30, blank=True, null=True)
    court_judge = models.CharField(verbose_name='法院法官', max_length=20, blank=True, null=True)
    judge_date = models.DateField(verbose_name='判决时间', max_length=20, blank=True, null=True)
    judge_code = models.CharField(verbose_name='判决编号', max_length=50, blank=True, null=True)
    judge_result = models.TextField(verbose_name='判决结果', blank=True, null=True)
    status = models.IntegerField(verbose_name="案件状态", choices=STATUS, default=0)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '刑事自诉案件执行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}({})".format(self.private.case_name, self.stage.name)

    def get_relative_person(self):
        natures = self.natures.exclude(legal_status=7)
        legals = self.legals.exclude(legal_status=7)
        relative_person = []
        for n in natures:
            relative_person.append(n.name)

        for l in legals:
            relative_person.append(l.company_name)

        return ",".join(relative_person)

    def get_relative_count(self):
        nature_count = self.natures.count()
        legals_count = self.legals.count()
        return nature_count + legals_count


class CrimiPrivateNaturePerson(models.Model):
    """刑事自诉自然人信息"""
    case = models.ForeignKey(CrimiPrivateDetail, verbose_name='案件名称', related_name="natures", null=True, blank=True, on_delete=models.CASCADE,)
    name = models.CharField(verbose_name='姓名', max_length=50)
    legal_status = models.ForeignKey(PrivateLegalStatus, verbose_name="法律地位", blank=True, null=True)
    gender = models.CharField(verbose_name='性别', max_length=2, choices=SEX_CHOICES, blank=True, null=True)
    age = models.CharField(verbose_name='年龄', max_length=10, blank=True, null=True)
    nation = models.CharField(verbose_name='民族', max_length=20, blank=True, null=True)
    tel = models.CharField(verbose_name='联系电话', max_length=50, blank=True, null=True)
    id_code = models.CharField(verbose_name='身份证', max_length=50, blank=True, null=True)
    address = models.CharField(verbose_name='现住址', max_length=200, blank=True, null=True)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '人员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CrimiPrivateLegalPerson(models.Model):
    """刑事自诉法人信息"""
    case = models.ForeignKey(CrimiPrivateDetail, verbose_name='案件名称',  related_name="legals", on_delete=models.CASCADE,)
    company_name = models.CharField(verbose_name='公司名称', max_length=60)
    legal_status = models.ForeignKey(PrivateLegalStatus, verbose_name="法律地位", blank=True, null=True)
    credit_code = models.CharField(verbose_name='统一社会信用代码', max_length=30, blank=True, null=True)
    legal_person = models.CharField(verbose_name='法人姓名', max_length=10, blank=True, null=True)
    telephone = models.CharField(verbose_name='联系电话', max_length=20, blank=True, null=True)
    address = models.CharField(verbose_name='住所地', max_length=200, blank=True, null=True)
    job = models.CharField(verbose_name='职务', max_length=50, blank=True, null=True)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '刑事自诉相对人信息(法人)'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.company_name


class CrimiPrivateLawsuitScheme(models.Model):
    """刑事自诉诉讼方案"""
    private_detail = models.OneToOneField(CrimiPrivateDetail, verbose_name='案件名称', on_delete=models.CASCADE)

    complaint_claim = models.TextField(verbose_name='诉讼请求', blank=True, null=True, help_text="起诉状")
    complaint_reasons = models.TextField(verbose_name='事实和理由', blank=True, null=True, help_text="起诉状")

    statement = models.TextField(verbose_name='代理意见', blank=True, null=True, help_text="代理词")

    counterclaim_answer = models.TextField(verbose_name='反诉答辩意见', max_length=1000, blank=True, null=True, help_text="反诉答辩状")

    counterclaim_ask = models.TextField(verbose_name='反诉请求', blank=True, null=True, help_text="反诉状")
    counterclaim_reasons = models.TextField(verbose_name='事实和理由', blank=True, null=True, help_text="反诉状")

    pleadings = models.TextField(verbose_name='答辩意见', blank=True, null=True, help_text="答辩状")

    defense_opinion = models.TextField(verbose_name='辩护意见', blank=True, null=True, help_text="辩护词")

    appeal_claim = models.TextField(verbose_name='上诉请求', blank=True, null=True, help_text="上诉状")
    appeal_reasons = models.TextField(verbose_name='事实和理由', blank=True, null=True, help_text="上诉状")

    retrialapply_claim = models.TextField(verbose_name='诉讼请求', blank=True, null=True, help_text="再审申请书")
    retrialapply_reasons = models.TextField(verbose_name='事实和理由', blank=True, null=True, help_text="再审申请书")

    user = models.ForeignKey(UserInfo, verbose_name='录入人', blank=True, null=True, on_delete=models.SET_NULL)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '刑事自诉诉讼方案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.private_detail


class CrimiPrivateCompensate(models.Model):
    """赔偿明细"""
    scheme = models.ForeignKey(CrimiPrivateLawsuitScheme, verbose_name='案件诉讼方案', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='赔偿内容', max_length=400)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '赔偿明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class CrimiPrivateApplications(models.Model):
    """所需申请书"""
    scheme = models.ForeignKey(CrimiPrivateLawsuitScheme, verbose_name='案件诉讼方案', on_delete=models.CASCADE)
    appli_name = models.CharField(verbose_name='所需申请书', max_length=100)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '民事所需申请书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.appli_name


class CrimiPrivateEvidence(models.Model):
    """证据目录"""
    scheme = models.ForeignKey(CrimiPrivateLawsuitScheme, verbose_name='案件诉讼方案', on_delete=models.CASCADE)
    evi_name = models.CharField(verbose_name='证据名称', max_length=100)
    evi_type = models.IntegerField(verbose_name='证据类型', choices=EVI_TYPE, default=1)
    evi_source = models.IntegerField(verbose_name='证据来源', choices=EVI_SOURCE, default=1)
    evi_purpose = models.CharField(verbose_name='证据目的', max_length=400, blank=True, null=True)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '刑事自诉证据目录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.evi_name


class CrimiPrivateAskingOutline(models.Model):
    """询问提纲"""
    scheme = models.ForeignKey(CrimiPrivateLawsuitScheme, verbose_name='案件诉讼方案', on_delete=models.CASCADE)
    target = models.IntegerField(verbose_name='询问对象', default=1, choices=ASK_TARGET)
    content = models.CharField(verbose_name='询问内容', max_length=400, blank=True, null=True)
    update_at = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '刑事自诉询问提纲'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.scheme

from django.conf.urls import url, include

from admincase.views import AdminCasePrintView, AdminAgentView, AdminAuthLetterView, AdminLegalRepresCertView, \
    AdminComplaintView, AdminStatementView, AdminEvidenceListView, AdminCompensateView, AdminAskingOutlineView, \
    AdminApplicationView, AdminPleadingsView, AdminAppealView, AdminRetrialView, AdminLawyerLetterView
from civilcase.views import (
    CivilCasePrintView,
    CivilAgentView, CivilAuthLetterView, RiskNoticeView, LegalRepresCertView, CivilComplaintView, CivilStatementView,
    CivilEvidenceListView, CivilCompensateView, CivilAskingOutlineView, CivilApplicationView,
    CivilAnswerCounterClaimView, CivilCounterClaimView, CivilPleadingsView, CivilAppealView, CivilRetrialView,
    CivilLawyerLetterView)
from crimicase.views import CriminalCasePrintView, CriminalAgentView, CriminalAuthLetterView, \
    CriminalLegalRepresCertView, CriminalIntroduceLetterView, CriminalBailAwaitView, CriminalLegalOpinionView, \
    CriminalEvidenceListView, CriminalAskingOutlineView, CriminalApplicationView, CriminalLawyerLetterView, \
    CriminalNoArrestOpinionView, CriminalDetainOpinionView, CriminalDefenseOpinionView, CriminalAppealView, \
    CriminalRetrialView
from crimicivil.views import CrmCivilCasePrintView, CrmCivilAgentView, CrmCivilAuthLetterView, CrmCivilComplaintView, \
    CrmCivilStatementView, CrmCivilEvidenceListView, CrmCivilCompensateView, CrmCivilAskingOutlineView, \
    CrmCivilApplicationView, CrmCivilAppealView, CrmCivilRetrialView, CrmCivilLawyerLetterView, \
    CrmCivilLegalRepresCertView, CrmCivilProtestView
from crimiprivate.views import CrimiPrivateCasePrintView, CrimiPrivateAgentView, CrimiPrivateAuthLetterView, \
    CrimiPrivateLegalRepresCertView, CrimiPrivateComplaintView, CrimiPrivateStatementView, CrimiPrivateEvidenceListView, \
    CrimiPrivateCompensateView, CrimiPrivateAskingOutlineView, CrimiPrivateApplicationView, \
    CrimiPrivateAnswerCounterClaimView, CrimiPrivateCounterClaimView, CrimiPrivatePleadingsView, CrimiPrivateAppealView, \
    CrimiPrivateRetrialView, CrimiPrivateLawyerLetterView, CrimiPrivateDefenseOpinionView




urlpatterns = [
    # 民事
    url(r'^civil_case_print/(?P<detail_id>\d+)/$', CivilCasePrintView.as_view(), name="civil-case-print"),
    url(r'^civil_agent/(?P<civil_id>\d+)/$', CivilAgentView.as_view(), name="civil-agent"),
    url(r'^civil_auth/(?P<civil_id>\d+)/$', CivilAuthLetterView.as_view(), name="civil-auth-letter"),
    url(r'^risk_notice/$', RiskNoticeView.as_view(), name="risk-notice"),
    url(r'^legal_cert/(?P<civil_id>\d+)/$', LegalRepresCertView.as_view(), name="legal-repres-cert"),
    url(r'^civil_complaint/(?P<detail_id>\d+)/$', CivilComplaintView.as_view(), name="civil-complaint"),
    url(r'^civil_statement/(?P<detail_id>\d+)/$', CivilStatementView.as_view(), name="civil-statement"),
    url(r'^civil_evidence/(?P<detail_id>\d+)/$', CivilEvidenceListView.as_view(), name="civil-evidence-list"),
    url(r'^civil_compensate/(?P<detail_id>\d+)/$', CivilCompensateView.as_view(), name="civil-compensate"),
    url(r'^civil_outline/(?P<detail_id>\d+)/$', CivilAskingOutlineView.as_view(), name="civil-outline"),
    url(r'^civil_application/(?P<detail_id>\d+)/$', CivilApplicationView.as_view(), name="civil-application"),
    url(r'^civil_answer_claim/(?P<detail_id>\d+)/$', CivilAnswerCounterClaimView.as_view(), name="civil-answer-claim"),
    url(r'^civil_counter_claim/(?P<detail_id>\d+)/$', CivilCounterClaimView.as_view(), name="civil-counter-claim"),
    url(r'^civil_pleadings/(?P<detail_id>\d+)/$', CivilPleadingsView.as_view(), name="civil-pleadings"),
    url(r'^civil_appeal/(?P<detail_id>\d+)/$', CivilAppealView.as_view(), name="civil-appeal"),
    url(r'^civil_retial/(?P<detail_id>\d+)/$', CivilRetrialView.as_view(), name="civil-retrial"),
    url(r'^civil_lawyer/(?P<detail_id>\d+)/$', CivilLawyerLetterView.as_view(), name="civil-lawyer"),
    # 刑事
    url(r'^criminal_case_print/(?P<detail_id>\d+)/$', CriminalCasePrintView.as_view(), name="criminal-case-print"),
    url(r'^criminal_agent/(?P<crimi_id>\d+)/$', CriminalAgentView.as_view(), name="criminal-agent"),
    url(r'^criminal_auth/(?P<crimi_id>\d+)/$', CriminalAuthLetterView.as_view(), name="criminal-auth-letter"),
    url(r'^criminal_legal_cert/(?P<crimi_id>\d+)/$', CriminalLegalRepresCertView.as_view(), name="criminal-legal-repres-cert"),
    url(r'^criminal_intro_letter/(?P<crimi_id>\d+)/$', CriminalIntroduceLetterView.as_view(), name="criminal-introduce-letter"),
    url(r'^criminal_bail_await/(?P<detail_id>\d+)/$', CriminalBailAwaitView.as_view(), name="criminal-bail-await"),
    url(r'^criminal_legal_opinion/(?P<detail_id>\d+)/$', CriminalLegalOpinionView.as_view(), name="criminal-legal-opinion"),
    url(r'^criminal_evidence_list/(?P<detail_id>\d+)/$', CriminalEvidenceListView.as_view(), name="criminal-evidence-list"),
    url(r'^criminal_outline/(?P<detail_id>\d+)/$', CriminalAskingOutlineView.as_view(), name="criminal-outline"),
    url(r'^criminal_application/(?P<detail_id>\d+)/$', CriminalApplicationView.as_view(), name="criminal-application"),
    url(r'^criminal_lawyer/(?P<detail_id>\d+)/$', CriminalLawyerLetterView.as_view(), name="criminal-lawyer"),
    url(r'^criminal_no_arrest/(?P<detail_id>\d+)/$', CriminalNoArrestOpinionView.as_view(), name="criminal-no-arrest"),
    url(r'^criminal_detain/(?P<detail_id>\d+)/$', CriminalDetainOpinionView.as_view(), name="criminal-detain"),
    url(r'^criminal_defense/(?P<detail_id>\d+)/$', CriminalDefenseOpinionView.as_view(), name="criminal-defense"),
    url(r'^criminal_appeal/(?P<detail_id>\d+)/$', CriminalAppealView.as_view(), name="criminal-appeal"),
    url(r'^criminal_retrial/(?P<detail_id>\d+)/$', CriminalRetrialView.as_view(), name="criminal-retrial"),
    # 行政
    url(r'^admin_case_print/(?P<detail_id>\d+)/$', AdminCasePrintView.as_view(), name="admin-case-print"),
    url(r'^admin_agent/(?P<admin_id>\d+)/$', AdminAgentView.as_view(), name="admin-agent"),
    url(r'^admin_auth/(?P<admin_id>\d+)/$', AdminAuthLetterView.as_view(), name="admin-auth-letter"),
    url(r'^admin_legal_cert/(?P<admin_id>\d+)/$', AdminLegalRepresCertView.as_view(), name="admin-legal-repres-cert"),
    url(r'^admin_complaint/(?P<detail_id>\d+)/$', AdminComplaintView.as_view(), name="admin-complaint"),
    url(r'^admin_statement/(?P<detail_id>\d+)/$', AdminStatementView.as_view(), name="admin-statement"),
    url(r'^admin_evidence/(?P<detail_id>\d+)/$', AdminEvidenceListView.as_view(), name="admin-evidence-list"),
    url(r'^admin_compensate/(?P<detail_id>\d+)/$', AdminCompensateView.as_view(), name="admin-compensate"),
    url(r'^admin_outline/(?P<detail_id>\d+)/$', AdminAskingOutlineView.as_view(), name="admin-outline"),
    url(r'^admin_application/(?P<detail_id>\d+)/$', AdminApplicationView.as_view(), name="admin-application"),
    url(r'^admin_pleadings/(?P<detail_id>\d+)/$', AdminPleadingsView.as_view(), name="admin-pleadings"),
    url(r'^admin_appeal/(?P<detail_id>\d+)/$', AdminAppealView.as_view(), name="admin-appeal"),
    url(r'^admin_retial/(?P<detail_id>\d+)/$', AdminRetrialView.as_view(), name="admin-retrial"),
    url(r'^admin_lawyer/(?P<detail_id>\d+)/$', AdminLawyerLetterView.as_view(), name="admin-lawyer"),
    # 刑自
    url(r'^private_case_print/(?P<detail_id>\d+)/$', CrimiPrivateCasePrintView.as_view(), name="private-case-print"),
    url(r'^private_agent/(?P<private_id>\d+)/$', CrimiPrivateAgentView.as_view(), name="private-agent"),
    url(r'^private_auth/(?P<private_id>\d+)/$', CrimiPrivateAuthLetterView.as_view(), name="private-auth-letter"),
    url(r'^private_legal_cert/(?P<private_id>\d+)/$', CrimiPrivateLegalRepresCertView.as_view(), name="private-legal-repres-cert"),
    url(r'^private_complaint/(?P<detail_id>\d+)/$', CrimiPrivateComplaintView.as_view(), name="private-complaint"),
    url(r'^private_statement/(?P<detail_id>\d+)/$', CrimiPrivateStatementView.as_view(), name="private-statement"),
    url(r'^private_evidence/(?P<detail_id>\d+)/$', CrimiPrivateEvidenceListView.as_view(), name="private-evidence-list"),
    url(r'^private_compensate/(?P<detail_id>\d+)/$', CrimiPrivateCompensateView.as_view(), name="private-compensate"),
    url(r'^private_outline/(?P<detail_id>\d+)/$', CrimiPrivateAskingOutlineView.as_view(), name="private-outline"),
    url(r'^private_application/(?P<detail_id>\d+)/$', CrimiPrivateApplicationView.as_view(), name="private-application"),
    url(r'^private_answer_claim/(?P<detail_id>\d+)/$', CrimiPrivateAnswerCounterClaimView.as_view(), name="private-answer-claim"),
    url(r'^private_counter_claim/(?P<detail_id>\d+)/$', CrimiPrivateCounterClaimView.as_view(), name="private-counter-claim"),
    url(r'^private_pleadings/(?P<detail_id>\d+)/$', CrimiPrivatePleadingsView.as_view(), name="private-pleadings"),
    url(r'^private_appeal/(?P<detail_id>\d+)/$', CrimiPrivateAppealView.as_view(), name="private-appeal"),
    url(r'^private_retial/(?P<detail_id>\d+)/$', CrimiPrivateRetrialView.as_view(), name="private-retrial"),
    url(r'^private_lawyer/(?P<detail_id>\d+)/$', CrimiPrivateLawyerLetterView.as_view(), name="private-lawyer"),
    url(r'^privaste_defense/(?P<detail_id>\d+)/$', CrimiPrivateDefenseOpinionView.as_view(), name="private-defense"),
    # 刑附民
    url(r'^crmcivil_case_print/(?P<detail_id>\d+)/$', CrmCivilCasePrintView.as_view(), name="crmcivil-case-print"),
    url(r'^crmcivil_agent/(?P<crmcivil_id>\d+)/$', CrmCivilAgentView.as_view(), name="crmcivil-agent"),
    url(r'^crmcivil_auth/(?P<crmcivil_id>\d+)/$', CrmCivilAuthLetterView.as_view(), name="crmcivil-auth-letter"),
    url(r'^crmcivil_legal_cert/(?P<crmcivil_id>\d+)/$', CrmCivilLegalRepresCertView.as_view(), name="crmcivil-legal-repres-cert"),
    url(r'^crmcivil_complaint/(?P<detail_id>\d+)/$', CrmCivilComplaintView.as_view(), name="crmcivil-complaint"),
    url(r'^crmcivil_statement/(?P<detail_id>\d+)/$', CrmCivilStatementView.as_view(), name="crmcivil-statement"),
    url(r'^crmcivil_evidence/(?P<detail_id>\d+)/$', CrmCivilEvidenceListView.as_view(), name="crmcivil-evidence-list"),
    url(r'^crmcivil_compensate/(?P<detail_id>\d+)/$', CrmCivilCompensateView.as_view(), name="crmcivil-compensate"),
    url(r'^crmcivil_outline/(?P<detail_id>\d+)/$', CrmCivilAskingOutlineView.as_view(), name="crmcivil-outline"),
    url(r'^crmcivil_application/(?P<detail_id>\d+)/$', CrmCivilApplicationView.as_view(), name="crmcivil-application"),
    url(r'^crmcivil_appeal/(?P<detail_id>\d+)/$', CrmCivilAppealView.as_view(), name="crmcivil-appeal"),
    url(r'^crmcivil_protest/(?P<detail_id>\d+)/$', CrmCivilProtestView.as_view(), name="crmcivil-protest"),
    url(r'^crmcivil_retial/(?P<detail_id>\d+)/$', CrmCivilRetrialView.as_view(), name="crmcivil-retrial"),
    url(r'^crmcivil_lawyer/(?P<detail_id>\d+)/$', CrmCivilLawyerLetterView.as_view(), name="crmcivil-lawyer"),
]
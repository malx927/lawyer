"""lawyer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views

from rbac.account import login, logout, password_change

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^password/change/(?P<pk>\d+)/$', password_change, name='password-change'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', views.obtain_auth_token, name="obtain-auth-token"),
    url(r'^rbac/', include('rbac.urls', namespace='rbac')),
    url(r'^adm/', include('adm.urls', namespace='adm')),
    url(r'^adm/api/', include('adm.api.urls')),
    url(r'^advisor/', include('advisor.urls', namespace='advisor')),
    url(r'^calculator/', include('calculator.urls', namespace='calculator')),
    url(r'^calculator/api/', include('calculator.api.urls', namespace='calculator-api')),
    url(r'^calc_manager/', include('calculator.calculator_urls', namespace='calc-mgr')),
    url(r'^civil/', include('civilcase.urls', namespace='civil-case')),
    url(r'^criminal/', include('crimicase.urls', namespace='criminal')),
    url(r'^admincase/', include('admincase.urls', namespace='admincase')),
    url(r'^private/', include('crimiprivate.urls', namespace='private')),
    url(r'^crmcivil/', include('crimicivil.urls', namespace='crmcivil')),
    url(r'^print/', include('civilcase.print_urls', namespace='print')),
]

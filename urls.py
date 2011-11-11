# coding:utf8
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django import forms
import django
from django.utils.translation import ugettext_lazy as _

from djangobp.route import controller_resource_method_pattern, router
import issue.controllers

# admin에서 User.username 에 대해 영문&숫자 외의 문자도 허용.
django.contrib.auth.forms.UserCreationForm.username = forms.CharField(label=_("Username"), max_length=30)
admin.autodiscover()
# 위의 UserCreationForm.username 적용은 autodiscover 수행시엔
# 안먹힘. 그래서 User에 대해서만 unregister & register 함.
admin.site.unregister(django.contrib.auth.models.User)
admin.site.register(django.contrib.auth.models.User)

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', issue.controllers.index),
    url(r'', include('social_auth.urls')),
    (controller_resource_method_pattern, router(issue.controllers)),
    # Examples:
    # url(r'^$', 'issuetrackr.views.home', name='home'),
    # url(r'^issuetrackr/', include('issuetrackr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from djangobp.route import controller_resource_method_pattern, router
import issue.controllers
admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^_admin/', include(admin.site.urls)),
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

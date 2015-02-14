from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    #url(r'^ops/$', OpsView.as_view(), name='ops'),
    url(r'^ops/', include('opsmanager.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

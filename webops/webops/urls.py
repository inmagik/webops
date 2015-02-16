from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    # Examples:
    #url(r'^ops/$', OpsView.as_view(), name='ops'),
    url(r'^ops/', include('opsmanager.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns = format_suffix_patterns(urlpatterns)

#serving static in debug
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.BASE_DIR)

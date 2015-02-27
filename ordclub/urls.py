from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ordclub.views.home', name='home'),
    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^admin/', include(admin.site.urls)),
)

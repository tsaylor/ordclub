from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'ordclub.views.home', name='home'),
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)

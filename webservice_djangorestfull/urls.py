from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = patterns('registry_app.views',
                       
    url(r'^global_ssh/$', 'user_list'),
    url(r'^global_ssh/(?P<pool>[0-9a-zA-Z_-]+)/$', 'user_detail'),
)
urlpatterns = format_suffix_patterns(urlpatterns)

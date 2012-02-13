# coding=utf-8
"""oneingdufs.urls 全局urls"""

from django.conf.urls.defaults import patterns, include, url
# project import
from oneingdufs import settings
from oneingdufs.home.forms import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# globals.views
urlpatterns = patterns('',
    url(r'^$', 'oneingdufs.views.index'),
    url(r'^about/$', 'oneingdufs.views.about'),
    url(r'^test/$', 'oneingdufs.views.test'),
)

# apps views
urlpatterns += patterns('',
  # home
  url(r'^home/', include('oneingdufs.home.urls')),
  # campuscard
  url(r'^card/', include('oneingdufs.campuscard.urls')),
)

# 静态文件访问
if not settings.isSAE:
  urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
  )

# coding=utf-8
"""oneingdufs.urls 全局urls"""

from django.conf.urls.defaults import patterns, include, url
# project import
from oneingdufs import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# globals.views
urlpatterns = patterns('',
    url(r'^$', 'oneingdufs.views.index'),
    url(r'^about/$', 'oneingdufs.views.about'),
    url(r'^test/$', 'oneingdufs.views.test'),
)

# globals api
urlpatterns += patterns('',
    url(r'^api/test/$', 'oneingdufs.api.test'),
    url(r'^api/getcsrftoken/$', 'oneingdufs.api.getcsrftoken'),
    url(r'^api/sendnotification/$', 'oneingdufs.api.sendnotification'),
)

# apps views
urlpatterns += patterns('',
  # home
  url(r'^home/', include('oneingdufs.home.urls')),
  url(r'^api/home/', include('oneingdufs.home.apiurls')),
  # life
  url(r'^life/', include('oneingdufs.life.urls')),
)

# 静态文件访问
if not settings.isSAE:
  urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
  )

# coding=utf-8
"""oneingdufs.home.urls 用户中心urls"""

from django.conf.urls.defaults import patterns, include, url
# project import
from oneingdufs.home.views import *
from oneingdufs.home.forms import *

urlpatterns = patterns('',
  url(r'^$', index),
  url(r'^register/$', register),
  url(r'^login/$', login),
  url(r'^logout/$', logout),
)

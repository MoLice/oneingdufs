# coding=utf-8
"""oneingdufs.life.urls 校园生活urls"""

from django.conf.urls.defaults import patterns, include, url
# project import
from oneingdufs.life.views import *

urlpatterns = patterns('',
  # 首页
  url(r'^$', index),
  url(r'^card/', card),
  url(r'^water/', water),
  url(r'^fix/', fix),
)

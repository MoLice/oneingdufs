# coding=utf-8
"""oneingdufs.common.apiurls 公共消息api urls"""

from django.conf.urls.defaults import patterns, url
# project import
from oneingdufs.common.api import *

urlpatterns = patterns('',
  # 校历
  url(r'^calendar/$', calendar),
)

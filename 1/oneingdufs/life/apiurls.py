# coding=utf-8
"""oneingdufs.life.apiurls 在校生活api urls"""

from django.conf.urls.defaults import patterns, url
# project import
from oneingdufs.life.api import *

urlpatterns = patterns('',
  # 宿舍地址
  url(r'^roomaddress/$', roomaddress),
  # 校园卡
  url(r'^card/$', card),
)

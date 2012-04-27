# coding=utf-8
"""oneingdufs.message.apiurls 消息api urls"""

from django.conf.urls.defaults import patterns, url
# project import
from oneingdufs.message.api import *

urlpatterns = patterns('',
  # 发送消息
  url(r'^$', index),
)

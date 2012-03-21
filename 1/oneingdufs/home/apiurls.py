# coding=utf-8
"""oneingdufs.home.apiurls 用户中心api urls"""

from django.conf.urls.defaults import patterns, url
# project import
from oneingdufs.home.api import *

urlpatterns = patterns('',
  url(r'^test/$', test),
  # 注册
  url(r'^register/$', register),
  # 登录
  url(r'^login/$', login),
  # 退出
  url(r'^logout/$', logout),
  # 个人信息
  url(r'^info/$', info),
)

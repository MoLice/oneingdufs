# coding=utf-8
"""oneingdufs.home.urls 用户中心urls"""

from django.conf.urls.defaults import patterns, include, url
# project import
from oneingdufs.home.views import *
from oneingdufs.home.forms import *

urlpatterns = patterns('',
  # 首页，重定向到/home/info/
  url(r'^$', index),
  # 注册
  url(r'^register/$', register),
  # 登录
  url(r'^login/$', login),
  # 退出
  url(r'^logout/$', logout),
  # 基本信息
  url(r'^info/$', info),
  # 在校相关
  url(r'^atschool/$', atschool),
  # 账号设置，重定向到/home/settings/security/
  url(r'^settings/$', settings),
  # 账号安全
  url(r'^settings/security/$', security),
  # 关联修改
  url(r'^settings/relation/$', relation),
)

# coding=utf-8
"""oneingdufs.study.apiurls 在校学习api urls"""

from django.conf.urls.defaults import patterns, url
# project import
from oneingdufs.study.api import *

urlpatterns = patterns('',
  # 课表
  url(r'^syllabus/$', syllabus),
)

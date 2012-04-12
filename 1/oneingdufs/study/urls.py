# coding=utf-8
"""oneingdufs.study.urls 在校学习urls"""

from django.conf.urls.defaults import patterns, include, url
# project import
from oneingdufs.study.views import *

urlpatterns = patterns('',
  url(r'^syllabus/$', syllabus),
)

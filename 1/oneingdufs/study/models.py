# coding=utf-8
"""oneingdufs.study.models 在校学习模型

@author: MoLice<sf.molice@gmail.com>
|- Study 在校学习模型
"""
from django.db import models
from django.contrib.auth.models import User
# project import

class Study(models.Model):
  """在校学习模型，包括课表"""
  # 用户，与用户表关联
  userId = models.ForeignKey(User)
  syllabus = models.TextField()

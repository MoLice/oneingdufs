# coding=utf-8
"""oneingdufs.life.models 校园生活模型
|- Life 在校生活相关的个人数据
|- Card 校园卡

@author: MoLice<sf.molice@gmail.com>
"""

from django.db import models
from django.contrib.auth.models import User
# project import

class Life(models.Model):
  """在校生活相关的个人数据"""
  # TODO 使用meta内部类增加字段验证
  # 用户id
  userId = models.ForeignKey(User)
  # 栋，例：13，范围：1-13
  building = models.CharField(max_length=2)
  # 宿舍号，例：507，范围：2??-7??
  room = models.CharField(max_length=3)

class Card(models.Model):
  """校园卡"""
  # 用户id
  userId = models.ForeignKey(User)
  # 卡号
  cardId = models.CharField(max_length=5, unique=True)
  # 当前余额
  balance = models.DecimalField(max_digits=7, decimal_places=2)
  # 最后一次消费金额
  lastspend = models.DecimalField(max_digits=7, decimal_places=2)
  # 最后一次消费时间
  lasttime = models.DateTimeField()
  # 最后一次消费地点
  lastposition = models.CharField(max_length=20)

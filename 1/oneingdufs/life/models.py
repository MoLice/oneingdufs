# coding=utf-8
"""oneingdufs.life.models 校园生活模型
|- Card 校园卡
|- Water 订水

@author: MoLice<sf.molice@gmail.com>
"""

from django.db import models
from django.contrib.auth.models import User
# project import

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

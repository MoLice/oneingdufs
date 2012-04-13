# coding=utf-8
"""oneingdufs.life.models 校园生活模型
|- Life 在校生活相关的个人数据
|- Card 校园卡
|- GdufsLife 后勤留言

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

class GdufsLife(models.Model):
  """后勤留言"""
  CAMPUS = (
    ('南校', '南校',),
    ('北校', '北校',),
  )
  TYPES = (
    ('宿舍', '宿舍',),
    ('教学', '教学',),
    ('饭堂', '饭堂',),
    ('门诊', '门诊',),
    ('其他', '其他',),
  )
  # 留言者
  userId = models.ForeignKey(User)
  # 邮箱
  email = models.EmailField()
  # 留言标题
  title = models.CharField(max_length=30)
  # 留言内容
  content = models.TextField()
  # 校区
  campus = models.CharField(max_length=2, choices=CAMPUS, default='南校')
  # 区域
  types = models.CharField(max_length=2, choices=TYPES, default='宿舍')
  # 留言时间
  create_date = models.DateTimeField(auto_now_add=True)
  # 是否已回复
  reply_alreay = models.BooleanField(default=False)
  # 回复时间
  reply_date = models.DateTimeField(auto_now=True)
  # 回复内容
  reply_content = models.TextField(null=True)
  # 回复人
  reply_userId = models.IntegerField(null=True)

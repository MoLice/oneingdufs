# coding=utf-8
"""oneingdufs.personalinfo.models 个人信息模型

@author: MoLice<sf.molice@gmail.com>
@createdate: 2012-01-30
|- Student 学生模型
|- AtSchool 学生行政档案数据模型
"""

from django.db import models
from django.contrib.auth.models import User
# project import
from oneingdufs.models import Profile
from oneingdufs.administration.models import ClassList

class Student(Profile):
  """用户模型，以学生为角色设计
  
  扩展自django User
  """
  # 手机
  telnum = models.CharField(max_length=11, null=True)
  # 短号
  cornet = models.CharField(max_length=10, null=True)
  # qq
  qq = models.CharField(max_length=12, null=True)
  # 状态
  state = models.CharField(max_length=10, null=True)

  def __str__(self):
    return self.studentId

class AtSchool(models.Model):
  """在校的个人信息，行政档案方面的"""
  # identity字段选择值
  IDENTITY_CHOICES = (
    ('0', '学生'),
    ('1', '教师'),
  )
  # 用户，与用户表关联
  userId = models.ForeignKey(User)
  # 学号
  studentId = models.CharField(max_length=11, unique=True)
  # 数字广外密码
  mygdufsPwd = models.CharField(max_length=20)
  # 真名
  truename = models.CharField(max_length=20, null=True)
  # 出生年月
  born = models.DateField(null=True)
  # 入学年月
  enroll = models.DateField(null=True)
  # 班级，与班级表关联
  classId = models.ForeignKey(ClassList, null=True)
  # 身份
  identity = models.CharField(max_length=1, choices=IDENTITY_CHOICES, default='0')

  def __str__(self):
    return self.truename

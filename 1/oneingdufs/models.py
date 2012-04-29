# coding=utf-8
"""oneingdufs.models 全局模型

@author MoLice<sf.molice@gmail.com>
|- UserBase 扩展User的元类
|- UserExtra 扩展User的类
|- GroupBase 拓展Group的元类
|- GroupExtra 拓展Group的类
"""

from django.db import models
from django.contrib.auth.models import User, Group

class UserBase(type):
  """用于扩展User的元类"""
  def __new__(cls, name, bases, attrs):
    module = attrs.pop('__module__')
    parents = [b for b in bases if isinstance(b, UserBase)]
    if parents:
      fields = []
      for obj_name, obj in attrs.items():
        if isinstance(obj, models.Field): fields.append(obj_name)
        User.add_to_class(obj_name, obj)
    
    return super(UserBase, cls).__new__(cls, name, bases, attrs)

class UserExtra(object):
  """扩展User的类，由UserBase元类实现

  方法：继承UserExtra即可自定义User模型，定义后的类无需使用，只要存在那么一个类即可
  """
  __metaclass__ = UserBase

class GroupBase(type):
  """用于扩展Group的元类"""
  def __new__(cls, name, bases, attrs):
    module = attrs.pop('__module__')
    parents = [b for b in bases if isinstance(b, GroupBase)]
    if parents:
      fields = []
      for obj_name, obj in attrs.items():
        if isinstance(obj, models.Field): fields.append(obj_name)
        Group.add_to_class(obj_name, obj)
    
    return super(GroupBase, cls).__new__(cls, name, bases, attrs)

class GroupExtra(object):
  """拓展Group类"""
  __metaclass__ = GroupBase

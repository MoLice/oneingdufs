# coding=utf-8
"""oneingdufs.models 全局模型

@author MoLice<sf.molice@gmail.com>
|- ProfileBase 扩展User的元类
|- Profile 扩展User的类
"""

from django.db import models
from django.contrib.auth.models import User

class ProfileBase(type):
  """用于扩展User的元类"""
  def __new__(cls, name, bases, attrs):
    module = attrs.pop('__module__')
    parents = [b for b in bases if isinstance(b, ProfileBase)]
    if parents:
      fields = []
      for obj_name, obj in attrs.items():
        if isinstance(obj, models.Field): fields.append(obj_name)
        User.add_to_class(obj_name, obj)
    
    return super(ProfileBase, cls).__new__(cls, name, bases, attrs)

class Profile(object):
  """扩展User的类，由ProfileBase元类实现

  方法：继承Profile即可自定义User模型
  """
  __metaclass__ = ProfileBase

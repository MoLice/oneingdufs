# coding=utf-8
"""oneingdufs.functions 常用函数合集

@author MoLice<sf.molice@gmail.com>
|- create_user(username, password, **kwargs) 创建User实例并存储到数据库
"""

import datetime
from django.contrib.auth.models import User

# 创建User实例并存储到数据库
# @param {String} username 用户名，必须
# @param {String} password 密码，必须
# @param **kwargs email|is_staff|is_active|is_superuser|telnum|cornet|qq|state
# @return {User} 返回创建成功的用户对象
def create_user(username, password, **kwargs):
  now = datetime.datetime.now()

  # 将参数覆盖默认值
  opts = {
    'email': '',
    'is_staff': False,
    'is_active': True,
    'is_superuser': False,
    'telnum': None,
    'cornet': None,
    'qq': None,
    'state': None,
  }
  for arg in kwargs:
    if arg in opts:
      opts[arg] = kwargs[arg]

  # 处理Email，将域名转为小写
  try:
    email_name, domain_part = opts['email'].strip().split('@', 1)
  except ValueError:
    pass
  else:
    opts['email'] = '@'.join([email_name, domain_part.lower()])

  # 创建User实例
  user = User(username=username, email=opts['email'], is_staff=opts['is_staff'],
              is_active=opts['is_active'], is_superuser=opts['is_superuser'],
              telnum=opts['telnum'], cornet=opts['cornet'], qq=opts['qq'],
              state=opts['state'], last_login=now, date_joined=now)
  # 设置密码
  user.set_password(password)

  # 存储用户
  user.save()

  return user

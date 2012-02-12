# coding=utf-8
"""oneingdufs.functions 常用函数合集

@author MoLice<sf.molice@gmail.com>
|- create_user(username, password, **kwargs) 创建User实例并存储到数据库
|- getRedirect(request) 用于表单，根据传入的request返回重定向的url
"""

import datetime
import re
import urlparse
from django.contrib.auth.models import User
# project import
from oneingdufs import settings

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

# 用于表单，根据传入的request返回重定向的url
# @param {request} request
# @return {String} 返回的重定向url
def getRedirect(request):
  referer = request.META.get('HTTP_REFERER', '')
  # 如果存在referer且其值和当前路径不一致，则直接返回referer，否则进行下一步分析
  if referer:
    parse_result = urlparse.urlparse(referer)
    if parse_result[1]:
      if parse_result[1] == request.get_host():
        if parse_result[2] != request.path:
          # 若存在域名则判断是否同域且路径名和当前路径不一致
          return referer
        else:
          # 路径名一致则检查next查询字符串
          query_next = re.match(r'next=(?P<next>[^&]*)', parse_result[4]).group('next')
          if query_next:
            return query_next
    else:
      if parse_result[2] != request.path:
        # 若不存在域名则只需判断路径名是否和当前路径不一致
        return referer

  # 从表单中的redirect_to字段取url进行分析
  post_redirect = request.POST.get('redirect_to', '')
  if post_redirect:
    parse_result = urlparse.urlparse(post_redirect)
    if parse_result[1]:
      if parse_result[1] != request.get_host():
        # 不同域，直接跳出
        return settings.LOGIN_REDIRECT_URL
      elif parse_result[2] != request.path:
        # 同域且路径名不一致则直接返回路径名
        return parse_result[2]
      else:
        # 同域同路径名，则看是否带有next查询字符串
        query_next = re.match(r'next=(?P<next>[^&]*)', parse_result[4]).group('next')
        if query_next:
          return query_next
  # 最终均无法通过检查则返回settings.LOGIN_REDIRECT_URL
  return settings.LOGIN_REDIRECT_URL

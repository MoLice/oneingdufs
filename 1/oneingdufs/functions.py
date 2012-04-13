# coding=utf-8
"""oneingdufs.functions 常用函数合集

@author MoLice<sf.molice@gmail.com>
|- create_user(username, password, **kwargs) 创建User实例并存储到数据库
|- getRedirect(request) 用于表单，根据传入的request返回重定向的url
|- getChoicesTuple() 从学院、专业、班级模型获取元组以供表单select控件使用
|- checkMyGdufsAuth() 发送post请求，验证数字广外账号密码
"""

import datetime
import re
import urlparse
import urllib
import urllib2
from django.contrib.auth.models import User, Group
# project import
from oneingdufs import settings

# 创建User实例并存储到数据库
# @example create_user(username='username', 'password'='123', studentId='2008', apn_username='123', groups=[])
# @param {String} username 用户名，必须
# @param {String} password 密码，必须
# @param {String} studentId 学号，必须
# @param {String} apn_username 在apn服务器注册的用户名
# @param **kwargs email|is_staff|is_active|is_superuser|telnum|cornet|qq|groups
# @return {User} 返回创建成功的用户对象
def create_user(username, password, studentId, apn_username, **kwargs):
  now = datetime.datetime.now()

  # 将参数覆盖默认值
  opts = {
    'email': '',
    'is_staff': False,
    'is_active': True,
    'is_superuser': False,
    'truename': None,
    'telnum': None,
    'cornet': None,
    'qq': None,
    'groups': [],
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
  user = User(username=username, studentId=studentId, apn_username=apn_username, email=opts['email'],
              is_staff=opts['is_staff'], is_active=opts['is_active'],
              is_superuser=opts['is_superuser'], truename=opts['truename'],
              telnum=opts['telnum'], cornet=opts['cornet'], qq=opts['qq'],
              last_login=now, date_joined=now)
  # 设置密码
  user.set_password(password)

  # 添加群组
  if len(opts['groups']) > 0:
    groups = opts['groups']
    for gId in groups:
      g = Group.objects.filter(id=gId)
      if g.count() != 0:
        user.groups.add(g)

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
          query_next = re.match(r'next=(?P<next>[^&]*)', parse_result[4])
          if query_next and query_next.group('next'):
            return query_next.group('next')
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

# 从学院、专业、班级模型获取元组以供表单select控件使用 
# @param {Model} models 从哪个models获取
# @param {Tuple|Boolean} foreignKey 一个元组，存储该模型的外键，用于过滤数据，默认为None，例：('facultyId', '1',)
# @param {Boolean} hasEmpty 是否要添加空选项，默认为True
# @param {String} emptyText 空选项的提示文字，默认为'请选择...'
# @return {Tuple} 返回一个choices元组
def getChoicesTuple(models, foreignKey=None, hasEmpty=True, emptyText='请选择...'):
  if foreignKey:
    exec 'models_all = models.objects.filter(%s=%s)' % (foreignKey[0], foreignKey[1])
  else:
    models_all = models.objects.all()
  models_length = models_all.count()
  models_list = []
  for i in range(0, models_length):
    models_list.append((str(models_all[i].id), models_all[i].name,))
  if hasEmpty:
    models_list.append(('', emptyText,))
  return tuple(models_list)

# 发送post请求，验证数字广外账号密码
# @param {String} username 数字广外用户名
# @param {String} password 数字广外密码
# @return {Boolean} 验证成功则返回True，否则返回False
def checkMyGdufsAuth(username, password):
  url = 'http://auth.gdufs.edu.cn/pkmslogin.form'
  query = {
    'username': username,
    'password': password,
    'login-form-type': 'pwd',
  }
  data = urllib.urlencode(query)
  request = urllib2.Request(url, data)
  try:
    response = urllib2.urlopen(request)
    result = response.read()
    # 数字广外登录成功时返回的页面内会包含这一句，假如这一句更改了则验证规则也得修改
    if re.findall(r'Your login was successful', result):
      return True
    return False
  except urllib2.URLError, e:
    return False

# coding=utf-8
"""oneingdufs.home.api 用户中心api

@author MoLice<sf.molice@gmail.com>
|- register 注册
|- login 登录
|- logout 退出
|- info 个人信息表单
|- group 我的团体
"""

from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
import time
import django.utils.simplejson as json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group
# project import
from oneingdufs.decorators import apicall_validator
# 导入form表单
from oneingdufs.home.forms import *
# 导入常用函数集合
import oneingdufs.functions as _fn
# 导入模型
import oneingdufs.personalinfo.models as pm
import oneingdufs.life.models as lm
import oneingdufs.common.models as am

def register(request):
  """/api/home/register/ 注册
  如果表单验证通过则注册用户并登录，返回username和sessionid
  如果表单验证未通过则返回表单错误信息formErrors
  接收data结构：
    {
      'username': '',
      'password': '',
      'studentId': '',
      'mygdufs_pwd': '',
      'apn_username': '',//非必须
      'groups': [1,2,3],//非必须，群组的id
    }
  返回data结构：
    {
      'success': True,
      'resultMsg': '',
      'sessionid': '',
      'username': ''
    }
  """
  if request.method == 'POST':
    data = json.loads(request.POST.get('data', '{}'))
    form = Register_form(data)
    if form.is_valid():
      # 验证通过，存储用户并登陆，同时返回sessionid
      user = _fn.create_user(username=data['username'], password=data['password'], studentId=data['studentId'], apn_username=data.get('apn_username', ''), groups=data.get('groups', []))
      atschool = pm.AtSchool(userId=user,mygdufs_pwd=data['mygdufs_pwd'])
      atschool.save()
      # 登录
      return login(request, data={
        'username': data['username'],
        'password': data['password'],
      })
    return HttpResponse(json.dumps({
      'success': False,
      'resultMsg': '表单验证错误',
      'formErrors': form.errors,
      'data': data,
    }))
  else:
    return HttpResponse(json.dumps({
      'success': False,
      'resultMsg': '请求方式出错，只能为POST',
    }))

def login(request, data=None):
  """/api/home/login/ 登录
  登录成功则返回sessionid和username，表单验证失败则返回formErrors
  接收data结构：
    {
      'username':'',
      'password': '',
      'apn_username': '',
    }
  返回data结构：
    {
      'success': True,
      'resultMsg': '登录成功',
      'sessionid': '',
      'username': '',
      'studentId': '',
      'user_info': {
        'email': '',
        'truename': '',
        'phone': '',
        'cornet': '',
        'qq': '',
      },
      'user_roomaddress': {
        'building': '',
        'room': '',
      },
    }
  """
  if request.method == 'POST':
    if data == None:
      data = json.loads(request.POST.get('data', '{}'))
    form = Login_form(data=data)
    if form.is_valid():
      auth_login(request, authenticate(username=data.get('username', ''), password=data.get('password', '')))
      user = request.user
      # 判断是否需要更新apn_username
      if data.get('apn_username', '') != '':
        user.apn_username = data['apn_username']
        user.save()
      # 登录成功要返回的数据
      result = {
        'success': True,
        'resultMsg': '登录成功',
        'sessionid': request.session.session_key,
        'username': user.username,
        'studentId': user.studentId,
        'user_info': {
          'email': '' if user.email == None else user.email,
          'truename': '' if user.truename == None else user.truename,
          'phone': '' if user.phone == None else user.phone,
          'cornet': '' if user.cornet == None else user.cornet,
          'qq': '' if user.qq == None else user.qq,
        },
        'user_roomaddress': {},
      }
      life = lm.Life.objects.filter(userId=user)
      if len(life) != 0:
        result['user_roomaddress']['building'] = life[0].building
        result['user_roomaddress']['room'] = life[0].room
      return HttpResponse(json.dumps(result))
    else:
      # 表单验证错误，用户名或密码不正确
      if not User.objects.filter(username__iexact=data.get('username', '')):
        return HttpResponse(json.dumps({
          'success': False,
          'resultMsg': '该昵称不存在，请检查输入或注册新账号',
          'formErrors': form.errors,
        }))
      return HttpResponse(json.dumps({
        'success': False,
        'resultMsg': '密码错误',
        'formErrors': form.errors,
      }))
  else:
    return HttpResponse(json.dumps({
      'success': False,
      'resultMsg': '请求方式出错，只能为POST',
    }))

@apicall_validator('ALL')
def logout(request, data=None):
  """/api/home/logout/ 退出"""
  request.user.apn_username = ''
  request.user.save()
  auth_logout(request)
  return HttpResponse(json.dumps({
    'success': True,
    'resultMsg': '已退出登录',
  }))

@apicall_validator('ALL')
def info(request, data=None):
  """/api/home/info/ 个人信息表单
  GET: 返回用户数据formData
  POST: 保存成功则返回success=True，表单验证失败则返回formErrors
  接收的data结构：
    {
      'email': '',
      'truename': '',
      'phone': '',
      'cornet': '',
      'qq': '',
    }
  返回的data结构：
    {
      'success': True,
      'resultMsg': '保存成功',
    }
  """
  user = request.user
  if request.method == 'GET':
    # 读取用户数据并返回
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '读取成功',
      'username': user.username,
      'studentId': user.studentId,
      'data': {
        'email': user.email,
        'truename': user.truename,
        'phone': user.phone,
        'cornet': user.cornet,
        'qq': user.qq,
      }}))
  # 保存表单数据
  form = Info_form(data=data, user=user)
  if form.is_valid():
    data = form.cleaned_data
    # user对象无法迭代，无法使用['key']方式访问，因此只能一个一个写
    user.email = data['email']
    user.truename = data['truename']
    user.phone = data['phone']
    user.cornet = data['cornet']
    user.qq = data['qq']
    if request.user.is_authenticated(): 
      return HttpResponse('is auth')
    else:
      return HttpResponse('not auth')
    user.save()
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '保存成功',
    }))
  else:
    return HttpResponse(json.dumps({
      'success': False,
      'resultMsg': '表单验证失败',
      'formErrors': form.errors,
    }))

@apicall_validator('ALL')
def group(request, data=None):
  """/home/group/ 我的团体，GET则返回该登录用户参加的团体，POST则将该用户加入到某个团体
  
  GET=>
  返回data格式：
  {
    'success': True,
    'resultMsg': '成功获取团体信息',
    'group': [
      {
        'id': 0,
        'name': '',
        'timestamp': '',
        'member': [
          {
            'id': 0,
            'username': '',
            'apn_enabled': false,
          },
        ],
      },
    ],
  }
  POST=>
  接收data格式：
  {
    'id': 0,
    'name': '',
  }
  返回data格式：
  {
    'success': True,
    'resultMsg': '成功加入' + groupname,
  }
  """
  if request.method == 'GET':
    # 读取该用户所属团体
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '成功获取团体信息',
      'group': getJsonFromGroups(request.user.groups.all()),
    }))
  else:
    # 将用户添加到团体
    return HttpResponse('{}')

def getJsonFromUsers(users):
  """将查询到的用户数组转换为json格式，被getJsonFromGroups()调用"""
  result = []
  for u in users:
    result.append({
      'id': u.id,
      'username': u.username,
      'apn_enabled': False if u.apn_username == None or u.apn_username == '' else true,
    })
  return result

def getJsonFromGroups(groups):
  """将查询到的用户所属group转换为json格式"""
  result = []
  for g in groups:
    result.append({
      'id': g.id,
      'name': g.name,
      'timestamp': str(g.timestamp),
      'member': getJsonFromUsers(g.user_set.all()),
    })
  return result

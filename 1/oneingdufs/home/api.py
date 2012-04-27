# coding=utf-8
"""oneingdufs.home.api 用户中心api

@author MoLice<sf.molice@gmail.com>
|- register 注册
|- login 登录
|- logout 退出
|- info 个人信息表单
"""

from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
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
      if User.objects.filter(apn_username__iexact=data['apn_username']):
        return HttpResponse(json.dumps({
          'success': False,
          'resultMsg': '该手机已注册过，请勿重复注册',
        }))
      # 验证通过，存储用户并登陆，同时返回sessionid
      user = _fn.create_user(username=data['username'], password=data['password'], studentId=data['studentId'], apn_username=data['apn_username'], groups=data.get('groups', []))
      atschool = pm.AtSchool(userId=user,mygdufs_pwd=data['mygdufs_pwd'])
      atschool.save()
      # 登录
      return login(request, data={
        'username': data['username'],
        'password': data['password'],
      })
    return HttpResponse(json.dumps({
      'success': False,
      'resultMsg': '表单验证错误1',
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
  接收data结构：{'username':'', 'password': ''}
  返回data结构：{'success': True, 'resultMsg': '', 'sessionid': '', 'username': ''}
  """
  if request.method == 'POST':
    if data == None:
      data = json.loads(request.POST.get('data', '{}'))
    form = Login_form(data=data)
    if form.is_valid():
      auth_login(request, authenticate(username=data.get('username', ''), password=data.get('password', '')))
      return HttpResponse(json.dumps({
        'success': True,
        'resultMsg': '登录成功',
        'sessionid': request.session.session_key,
        'username': request.user.username,
      }))
    return HttpResponse(json.dumps({
      'success': False,
      'resultMsg': '表单验证错误2',
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
  """
  user = request.user
  if request.method == 'GET':
    # 读取用户数据并返回
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '读取成功',
      'username': user.username,
      'studentId': user.studentId,
      'formData': {
        'email': user.email,
        'truename': user.truename,
        'telnum': user.telnum,
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
    user.telnum = data['telnum']
    user.cornet = data['cornet']
    user.qq = data['qq']
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
def atschool(request, data=None):
  """/api/home/atschool/ 在校相关
  GET: 返回用户在校相关数据formData
  POST: 保存成功则返回success=True，表单验证失败则返回formErrors
  """
  if request.method == 'GET':
    pm_atschool = pm.AtSchool.objects.get(userId=request.user)
  return HttpResponse('{}')

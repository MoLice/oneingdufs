# coding=utf-8
"""oneingdufs.home.api 用户中心api

@author MoLice<sf.molice@gmail.com>
|- test 测试用
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
from django.contrib.auth.decorators import login_required
# project import
from oneingdufs.decorators import apicall_validator
# 导入form表单
from oneingdufs.home.forms import *
# 导入常用函数集合
import oneingdufs.functions as _fn
# 导入模型
import oneingdufs.personalinfo.models as pm
import oneingdufs.administration.models as am

@apicall_validator('ALL')
def test(request, data=None):
  #data = request.REQUEST.get('data', '{"username":"","password_re":"1","mygdufs_pwd":"1","studentId":"20","password":"1"}')
  return HttpResponse(str(data))

@apicall_validator
def register(request, data=None):
  """/api/home/register/ 注册
  如果表单验证通过则注册用户并登录，返回username和sessionid
  如果表单验证未通过则返回表单错误信息formErrors
  """
  form = Register_form(data)
  if form.is_valid():
    # 验证通过，存储用户并登陆，同时返回sessionid
    data = form.cleaned_data
    user = _fn.create_user(username=data['username'], password=data['password'], studentId=data['studentId'])
    user.save()
    atschool = pm.AtSchool(userId=user,mygdufsPwd=data['mygdufs_pwd'])
    atschool.save()
    # 登录
    return login(request, data={
      'username': data['username'],
      'password': data['password'],
    })
    # 登录用户
    #auth_login(request, authenticate(username=user.username, password=data['password']))
    #return HttpResponse(json.dumps({
    #  'success': True,
    #  'resultMsg': '注册成功并登录',
    #  'sessionid': request.session.session_key,
    #  'username': request.user.username,
    #}))
  return HttpResponse(json.dumps({
    'success': False,
    'resultMsg': '表单验证错误',
    'formErrors': form.errors,
  }))

@apicall_validator
def login(request, data=None):
  """/api/home/login/ 登录
  登录成功则返回sessionid和username，表单验证失败则返回formErrors
  """
  form = Login_form(data)
  if form.is_valid():
    auth_login(request, form.get_user())
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '登录成功',
      'sessionid': request.sessionid.session_key,
      'username': request.user.username,
    }))
  return HttpResponse(json.dumps({
    'success': False,
    'resultMsg': '表单验证错误',
    'formErrors': form.errors,
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

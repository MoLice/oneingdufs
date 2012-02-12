# coding=utf-8
"""oneingdufs.home.views 用户视图

@author MoLice<sf.molice@gmail.com>
|- index 用户中心
|- register 注册
|- login 登录
|- logout 注销
"""

import urlparse
from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# project import
# 导入项目设置
from oneingdufs.settings import LOGIN_REDIRECT_URL
# 导入form表单
from oneingdufs.home.forms import *
# 导入常用函数集合
from oneingdufs.functions import create_user
# 导入模型
from oneingdufs.personalinfo.models import AtSchool

@login_required
def index(request):
  """/home/ 用户中心首页"""
  template_val = {}
  return render_to_response('home/index.html',
      template_val,
      context_instance=RequestContext(request))

def register(request):
  """/home/register/ 注册"""
  template_val = {}
  if request.method == 'GET':
    # GET方法，显示注册表单
    template_val['form'] = Register_form()

    return render_to_response('home/register.html',
        template_val,
        context_instance=RequestContext(request))
  else:
    # POST方法，提交注册表单，进行数据验证并插入到数据库
    register_form = Register_form(request.POST)
    if register_form.is_valid():
      # 验证通过，存储用户并转向
      data = register_form.cleaned_data
      user = create_user(username=data['username'], password=data['password'])
      user.save()
      atschool = AtSchool(userId=user, studentId=data['studentId'], mygdufsPwd=data['mygdufs_pwd'])
      atschool.save()
      # login this user
      auth_login(request, authenticate(username=user.username, password=data['password']))
      # url来源为/home/register/则转向到首页，否则转向到来源页
      if 'HTTP_REFERER' in request.META and urlparse.urlparse(request.META['HTTP_REFERER'])[2] == '/home/register/':
        return HttpResponseRedirect('/')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER', LOGIN_REDIRECT_URL))
    else:
      # 验证失败，修改表单
      template_val['form'] = register_form
      return render_to_response('home/register.html',
        template_val,
        context_instance=RequestContext(request))

def login(request):
  """/home/login/ 登录"""
  template_val = {}

  if request.method == "GET":
    if request.user.is_authenticated():
      return HttpResponseRedirect('/home/')
    template_val['form'] = Login_form()
    return render_to_response('home/login.html',
        template_val,
        context_instance=RequestContext(request))
  else:
    # 从url获取登录成功后要重定向的路径，默认值为settings.LOGIN_REDIRECT_URL
    redirect_to = request.REQUEST.get('next', LOGIN_REDIRECT_URL)
    form = Login_form(data=request.POST)
    if form.is_valid():
      hostname = urlparse.urlparse(redirect_to)[1]
      if hostname and hostname != request.get_host():
        # next字段转向非同域url
        redirect_to = LOGIN_REDIRECT_URL
      # login the user
      auth_login(request, form.get_user())
      return HttpResponseRedirect(redirect_to)
    else:
      template_val['form'] = form
      return render_to_response('home/login.html',
          template_val,
          context_instance=RequestContext(request))

def logout(request):
  """/home/logout/ 注销"""
  auth_logout(request)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', LOGIN_REDIRECT_URL))

# coding=utf-8
"""oneingdufs.home.views 用户视图

@author MoLice<sf.molice@gmail.com>
|- index 用户中心
|- register 注册
|- login 登录
|- logout 注销
|- info 基本信息表单
|- atschool 在校相关
|- settings 账号设置
|- security 账号安全
|- relation 关联修改
"""

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
import oneingdufs.functions as _fn
# 导入模型
import oneingdufs.personalinfo.models as pm
import oneingdufs.common.models as cm

@login_required
def index(request):
  """/home/ 用户中心首页"""
  return HttpResponseRedirect('/home/info/')
  
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
      user = _fn.create_user(username=data['username'], password=data['password'], studentId=data['studentId'])
      user.save()
      atschool = pm.AtSchool(userId=user, mygdufsPwd=data['mygdufs_pwd'])
      atschool.save()
      # login this user
      auth_login(request, authenticate(username=user.username, password=data['password']))
      return HttpResponseRedirect(_fn.getRedirect(request))
    else:
      # 验证失败，修改表单
      template_val['form'] = register_form
      return render_to_response('home/register.html',
        template_val,
        context_instance=RequestContext(request))

def login(request):
  """/home/login/ 登录"""
  template_val = {}

  if request.method == 'GET':
    if request.user.is_authenticated():
      return HttpResponseRedirect(_fn.getRedirect(request))
    template_val['form'] = Login_form()
    return render_to_response('home/login.html',
        template_val,
        context_instance=RequestContext(request))
  else:
    form = Login_form(data=request.POST)
    if form.is_valid():
      # login the user
      auth_login(request, form.get_user())
      return HttpResponseRedirect(_fn.getRedirect(request))
    else:
      template_val['form'] = form
      return render_to_response('home/login.html',
          template_val,
          context_instance=RequestContext(request))

def logout(request):
  """/home/logout/ 注销"""
  auth_logout(request)
  return HttpResponseRedirect(_fn.getRedirect(request))

@login_required
def info(request):
  """/home/info/ 基本信息表单"""
  template_val = {}
  user = request.user
  if request.method == 'GET':
    # GET，显示基本信息表单
    template_val['form'] = Info_form(initial={
      "email": user.email,
      "truename": user.truename,
      "telnum": user.telnum,
      "cornet": user.cornet,
      "qq": user.qq,
    })
    return render_to_response('home/index.html',
        template_val,
        context_instance=RequestContext(request))
  else:
    # POST，验证通过则保存修改
    form = Info_form(data=request.POST, user=user)
    if form.is_valid():
      data = form.cleaned_data
      # user无法迭代，无法使用key方式访问，只能一个一个写
      user.email = data['email']
      user.truename = data['truename']
      user.telnum = data['telnum']
      user.cornet = data['cornet']
      user.qq = data['qq']
      user.save()
      return HttpResponseRedirect('/home/info/')
    else:
      template_val['form'] = form
      return render_to_response('home/index.html',
          template_val,
          context_instance=RequestContext(request))

@login_required
def atschool(request):
  """/home/atschool/ 在校相关"""
  template_val = {}
  if request.method == 'GET':
    pm_atschool = pm.AtSchool.objects.get(userId=request.user)
    pm_major = ''
    pm_faculty = ''
    choices = {}
    # 假如存在班级id则读取对应的学院班级专业值及候选项
    if pm_atschool.classId:
      pm_major = cm.Major.objects.get(id=pm_atschool.classId.id)
      pm_faculty = cm.Faculty.objects.get(id=pm_major.facultyId.id)
      # set choices
      choices = {
          'major': _fn.getChoicesTuple(Major, foreignKey=('facultyId', str(pm_faculty.id),)),
          'classlist': _fn.getChoicesTuple(ClassList, foreignKey=('majorId', str(pm_major.id),)),
      }
    # 填充form
    template_val['form'] = AtSchool_form(initial={
      'born': pm_atschool.born,
      'enroll': pm_atschool.enroll,
      'faculty': pm_faculty and str(pm_faculty.id),
      'major': pm_major and str(pm_major.id),
      'classlist': pm_atschool.classId and str(pm_atschool.classId.id),
    })
    # 动态设置候选项
    if choices:
      for key in choices:
        template_val['form'].fields[key].choices = choices[key]
  else:
    # POST
    form = AtSchool_form(request.POST)
    if form.is_valid():
      return HttpResponse('验证通过')
    else:
      template_val['form'] = form
  return render_to_response('home/atschool.html',
      template_val,
      context_instance=RequestContext(request))

@login_required
def settings(request):
  """/home/settings/ 账号设置"""
  return HttpResponseRedirect('/home/settings/security/')

@login_required
def security(request):
  """/home/settings/security/ 账号安全"""
  template_val = {}
  return render_to_response('home/security.html',
      template_val,
      context_instance=RequestContext(request))

@login_required
def relation(request):
  """/home/settings/relation/ 关联修改"""
  template_val = {}
  return render_to_response('home/relation.html',
      template_val,
      context_instance=RequestContext(request))

# coding=utf-8
"""oneingdufs.views 全局视图

@author MoLice<sf.molice@gmail.com>
|- index 全站首页
|- about 关于
|- manage 管理工具集
|- test 测试
"""

from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
import re
import urllib
import urllib2
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
# project import
import oneingdufs.functions as _fn
from oneingdufs.home.forms import Login_form
from oneingdufs.administration.models import *

def index(request):
  """网站首页
  假如未登录则显示登录表单，假如已登录则显示主站内容
  """
  template_val = {}

  if request.user.is_authenticated():
    # 已登录
    return render_to_response('globals/index.html',
        template_val,
        context_instance=RequestContext(request))
  else:
    # 未登录
    template_val['form'] = Login_form()
    return render_to_response('globals/index_login.html',
        template_val,
        context_instance=RequestContext(request))

def about(request):
  """关于
  包括本站、制作人员等
  """
  return render_to_response('globals/about.html')

def manage(request):
  """管理工具集，包括测试信息的添加等操作"""
  if request.GET.get('token', '') == 'molice':
    # 验证成功
    progress = {'group':False,'user':False}
    result = ''
    # 增加群组
    if not Group.objects.filter(name__iexact='校学生会'):
      Group(name='学生后勤服务信息中心').save()
      Group(name='校学生会').save()
      Group(name='08计算机4班').save()
      progress['group'] = True
      result += '添加群组成功；'
    else:
      result += '群组已存在；'
    # 增加用户
    if not User.objects.filter(username__iexact='molice'):
      user = _fn.create_user(username='molice', password='tobethesame', studentId='20081000139', apn_username='', groups=[1,2,3])
      progress['user'] = True
      result += '添加molice成功'
    else:
      result += 'molice已存在'
    return HttpResponse(result)
  return HttpResponse('无权限')

def test(request):
  import oneingdufs.life.forms as f
  template_val = {'form': f.GdufsLife()}
  return render_to_response('life/gdufslife.html', template_val)

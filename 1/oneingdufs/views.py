# coding=utf-8
"""oneingdufs.views 全局视图

@author MoLice<sf.molice@gmail.com>
|- index 全站首页
|- about 关于
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
from django.contrib.auth.models import User
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

def test(request):
  url="http://localhost:7070/notification.do?action=send"
  query = {
    'broadcast': 'Y',
    'username': '',
    'title': 'From Django',
    'message': 'hello world',
    'uri': '',
  }
  data = urllib.urlencode(query)
  request = urllib2.Request(url, data)
  #request.add_header('Cookie', 'JSESSIONID=6l94xiargbfs1hfgek5mnyd6w;')
  try:
    response = urllib2.urlopen(request)
    result = response.read()
    return HttpResponse(result)
  except urllib2.URLError, e:
    return HttpResponse('error, ' + str(e))
  return HttpResponse(request.META.get("X_TYPE", "null"))

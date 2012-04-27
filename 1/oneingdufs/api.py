# coding=utf-8
"""oneingdufs.api 全局api

@author MoLice<sf.molice@gmail.com>
|- test 测试用
|- getcsrftoken 通过cookie获取csrftoken
|- updateapnusername 客户端重连或者重新注册用户时，更新该用户名到关联账号
"""

from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
import time
import urllib
import urllib2
import django.utils.simplejson as json
from django.contrib.auth.models import User
# project import
from oneingdufs.decorators import apicall_validator
from oneingdufs.life.models import Life

def test(request, data=None):
  life = Life.objects.filter(userId=request.user)
  return HttpResponse('{}')

# 无需登录
def getcsrftoken(request):
  """/api/getcsrftoken/ 提供客户端从Set-Cookie头部中获取csrftoken
  出于节省流量的考虑，返回数据尽量压缩体积
  """
  return HttpResponse('{}')



@apicall_validator()
def updateapnusername(request, data=None):
  """/api/updateapnusername/ 客户端重连或者重新注册用户时，更新该用户名到关联账号"""
  if data.get('username', None):
    request.user.apn_username = data['username']
    request.user.save()
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '更新成功',
    }))
  return HttpResponse(json.dumps({
    'success': False,
    'resultMsg': '更新失败',
  }))

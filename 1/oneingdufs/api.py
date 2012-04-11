# coding=utf-8
"""oneingdufs.api 全局api

@author MoLice<sf.molice@gmail.com>
|- test 测试用
|- getcsrftoken 通过cookie获取csrftoken
|- sendnotification 发送notification到AndroidPN
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

def test(request, data=None):
  data = request.REQUEST.get('data', '{"username":"","resultMsg":"do","password_re":"1","mygdufs_pwd":"1","studentId":"20","password":"1"}')
  return HttpResponse(data)

# 无需登录
def getcsrftoken(request):
  """/api/getcsrftoken/ 提供客户端从Set-Cookie头部中获取csrftoken
  出于节省流量的考虑，返回数据尽量压缩体积
  """
  return HttpResponse('{}')

@apicall_validator()
def sendnotification(request, data=None):
  """/api/sendnotification/ 接收客户端发来的消息，将其转发到AndroidPN服务器，由APN推送到目标机器
  客户端发送来的消息规格:
  {
    'to': 'MoLice1',
    'title': '消息标题',
    'message': '消息正文',
    'type': 'msg|no',
    'date': ''
  }
  发送到APN的消息格式:
  {
    'broadcast': 'N', # 不允许用户发送广播
    'username': '57cdfca236ab4cddba1fd81d200a26b3', # 要发送到的用户的APN用户名
    'title': 'from=MoLice;date=应用服务器当前时间;type=上面的type值;title=消息标题;', # 这些字段在Android客户端进行解析
    'message': '消息正文',
    'uri': '', # 不允许Android客户端发送uri，可以http:、https:、tel:、geo:开头
  }
  """
  # AndroidPN服务器地址
  apn_url = 'http://localhost:7070/notification.do?action=send'
  # 当前时间
  current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
  
  # 初始化接收到的用户消息
  if not 'type' in data or not data['type']:
    data['type'] = 'msg'
  if not 'title' in data:
    data['title'] = '来自OneInGDUFS的新消息'
  if not 'to' in data:
    data['to'] = request.user.apn_username
  if not 'message' in data:
    data['message'] = ''

  # 如果Android客户端发送来的json里没包含'to'，则将'to'设置为当前用户自己，此时消息将被推送回用户自己，由客户端判断则可知是否出错
  send_msg = {
    'broadcast': 'N',
    'username': User.objects.get(username=data['to']).apn_username,
    'title': 'from=%s;date=%s;type=%s;title=%s;' % (request.user.username, current_time, data['type'], data['title'],),
    'message': data['message'],
    'uri': '',
  }
  # 发送数据到AndroidPN服务器
  send_data = urllib.urlencode(send_msg)
  send_request = urllib2.Request(apn_url, send_data)
  try:
    send_response = urllib2.urlopen(send_request)
    send_result = send_response.read()
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': 'OK',
    }))
  except urllib2.URLError, e:
    return HttpResponse(json.dumps({
      'success': False,
      'resultMsg': '连接APN出错, ' + str(e),
    }))

# 无需登录
def updateapnusername(request):
  """/api/updateapnusername/ 客户端重连或者重新注册用户时，更新该用户名到关联账号"""
  data = json.loads(request.REQUEST.get('data', '{}'))
  if data['username']:
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

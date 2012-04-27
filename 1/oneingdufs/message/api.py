# coding=utf-8
"""oneingdufs.message.api 消息api

@author MoLice<sf.molice@gmail.com>
|- index 发送消息
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

@apicall_validator()
def index(request, data=None):
  """/api/message/ 接收客户端发来的消息，将其转发到AndroidPN服务器，由APN推送到目标机器
  客户端发送来的消息规格:
  {
    'username': 'MoLice1',
    'title': '消息标题',
    'content': '消息正文',
    'type': 'msg|no',
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
  # AndroidPN控制页面地址
  apn_url = 'http://localhost:7070/notification.do?action=send'
  # 当前时间
  current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
  
  # 初始化接收到的用户消息
  if not 'type' in data or not data['type']:
    data['type'] = 'msg'
  if not 'title' in data:
    data['title'] = '来自OneInGDUFS的新消息'
  if not 'username' in data:
    data['username'] = request.user.apn_username
  if not 'content' in data:
    data['content'] = ''

  # 如果Android客户端发送来的json里没包含'username'，则将'username'设置为当前用户自己，此时消息将被推送回用户自己，由客户端判断则可知是否出错
  send_msg = {
    'broadcast': 'N',
    'username': User.objects.get(username=data['username']).apn_username,
    'title': 'from=%s;date=%s;type=%s;title=%s;' % (request.user.username, current_time, data['type'], data['title'],),
    'message': data['content'],
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

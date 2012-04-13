# coding=utf-8
"""oneingdufs.life.api 校园生活api

@author MoLice<sf.molice@gmail.com>
|- roomaddress 宿舍地址
|- card 校园卡
|- gdufslife 后勤留言
"""

import re
from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
import django.utils.simplejson as json
# project import
from oneingdufs.decorators import apicall_validator
# 引入模型
import oneingdufs.life.models as lm
# 引入表单
import oneingdufs.life.forms as lf

@apicall_validator('ALL')
def roomaddress(request, data=None):
  """宿舍地址
  
  接收data结构：{'building': '13', 'room': '507'}
  返回data结构：{'success': True, 'resultMsg': '存储成功'}
  """
  if re.match(r'^\d{1}$|^1[0123]{1}$', data.get('building', '')) and re.match(r'^\d{3}$', data.get('room', '')) and re.match(r'^[234567]', data.get('room', '')):
    # 验证通过，存储到数据库
    lm.Life(userId=request.user, building=data['building'], room=data['room']).save()
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '存储成功'
    }))
  return HttpResponse(json.dumps({
    'success': False,
    'resultMsg': '选择错误，请重新填写'
  }))

@apicall_validator('GET')
def card(request, data=None):
  """校园卡
  
  返回data结构：{'success': True, 'resultMsg': '已更新', }
  """
  # 注意！从数据库读取的字段并非都是字符串，需要使用str()函数
  #card = lm.Card.objects.get(userId=request.user)
  return HttpResponse(json.dumps({
    'success': True,
    'resultMsg': '已更新',
    'cardId': '12345',#card.cardId,
    'balance': '100',#str(card.balance),
    'lastspend': '18',#str(card.lastspend),
    'lasttime': '2012-04-12 02:34:55',#str(card.lasttime),
    'lastposition': '二饭小卖部',#card.lastposition
  }))
  return HttpResponse(json.dumps({
    'success': False,
    'resultMsg': '读取失败，请稍后重试'
  }))

@apicall_validator('ALL')
def gdufslife(request, data=None):
  """后勤留言
  
  接收data格式：
  {
    'title': '',
    'content': '',
    'name': '',
    'email': '',
    'campus': '',
    'types': '',
  }
  返回data格式：
  {
    'success': True,
    'resultMsg': '',
  }
  """
  form = lf.GdufsLife(data)
  if form.is_valid():
    data = form.cleaned_data
    # 存入数据库
    record = lm.GdufsLife(
        userId=request.user,
        title=data['title'],
        content=data['content'],
        email=data['email'],
        campus=data['campus'],
        types=data['types']).save()
    # TODO 使用APN发送通知给后勤中心人员的账号
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '提交成功',
    }))
  return HttpResponse(json.dumps({
    'success': False,
    'resultMsg': '表单验证失败',
    'formErrors': form.errors,
  }))

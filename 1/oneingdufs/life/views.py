# coding=utf-8
"""oneingdufs.life.views 校园生活视图

@author MoLice<sf.molice@gmail.com>
|- index 校园生活首页
|- card 校园卡
|- water 订水
"""

from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# project import
# 模型
import oneingdufs.life.models as lm

def index(request):
  """/life/ 校园生活首页"""
  template_val = {}
  return render_to_response('life/index.html',
      template_val,
      context_instance=RequestContext(request))

@login_required
def card(request):
  """/life/card/ 校园卡"""
  template_val = {}
  card = lm.Card.objects.get(userId=request.user)
  template_val['card'] = card
  return render_to_response('life/card.html',
      template_val,
      context_instance=RequestContext(request))

@login_required
def water(request):
  """/life/water/ 订水"""
  template_val = {}
  return render_to_response('life/water.html',
      template_val,
      context_instance=RequestContext(request))

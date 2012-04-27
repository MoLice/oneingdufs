# coding=utf-8
"""oneingdufs.common.api 公共消息api

@author MoLice<sf.molice@gmail.com>
|- calendar 校历
"""

from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
import django.utils.simplejson as json
# project import
from oneingdufs.decorators import apicall_validator

@apicall_validator('ALL')
def calendar(request, data=None):
  """校历"""
  return HttpResponse('{}')

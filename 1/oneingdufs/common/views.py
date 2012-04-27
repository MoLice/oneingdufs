# coding=utf-8
"""oneingdufs.common.views 公共消息视图

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
from oneingdufs.constants import *

@apicall_validator('ALL')
def calendar(request, data=None):
  """校历"""
  return HttpResponse(json.dumps(COMMON_CALENDAR))

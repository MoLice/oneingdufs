# coding=utf-8
"""oneingdufs.study.api 在校学习

@author MoLice<sf.molice@gmail.com>
|- syllabus 我的课表
"""

from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
import django.utils.simplejson as json
# project import
from oneingdufs.decorators import apicall_validator
import oneingdufs.study.models as sm

@apicall_validator('ALL')
def syllabus(request, data=None):
  """我的课表
  
  返回的data结构：
  {
    'success': True,
    'resultMsg': '',
    'syllabus': [
      // 每天一个数组
      [
        // 当天的数组由多节课组成
        {
          'noon': 0|1|2,// 早上|下午|晚上
          'cutter': 0|1|2|3,// 前一节|后一节|3-5小节、6-8小节|7-9小节
          'content': '网络编程\n实验楼A-207',// 课程名称、上课地点
        },
        {},
      ],
    ],
  }
  """
  #study = sm.Study.object.filters(userId__iexact=request.user)
  study = {
    'syllabus': [[
        {
          'noon': 0,
          'cutter': 2,
          'content': '网络编程\n实验楼A-207',
        },
        {
          'noon': 1,
          'cutter': 0,
          'content': '综英5\nA-401',
        },
      ],[],[
        {
          'noon': 1,
          'cutter': 3,
          'content': '计算机网络\nF-501',
        },
      ],[],[
        {
          'noon': 2,
          'cutter': 0,
          'content': '影视音乐赏析\nF-118',
        },
      ],[],[]]
  }
  if study != None:
    return HttpResponse(json.dumps({
      'success': True,
      'resultMsg': '成功获取课表',
      'syllabus': study['syllabus'],
    }))
  return HttpResponse(json.dumps({
    'success': True,
    'resultMsg': '不存在课表数据',
  }))

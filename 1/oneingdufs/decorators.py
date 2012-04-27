# coding=utf-8
"""oneingdufs.decorators 函数修饰符

@author MoLice<sf.molice@gmail.com>
|- apicall_validator 检查是否符合调用api的规则（头部包含X-CSRFToken），若不符合则返回"header error"
"""
from django.http import (
  Http404,
  HttpResponse,
  HttpResponseRedirect,
)
import django.utils.simplejson as json

# {str}method POST|GET|ALL，即便不传参，也应该把括号写上
def apicall_validator(method='POST'):
  """所有/api/请求均必须添加的decorator，共完成以下功能：
  1、检查是否符合调用api的条件（COOKIES必须包含32位的sessionid和csrftoken，也即必须处于登录状态；POST头部必须包含X-CSRFToken）
  2、根据@apicall_validator传入的参数限定某种HTTP请求方式（GET/POST），不传参则默认限定POST
  3、POST请求必须包含data，GET则没有此要求
  验证失败时返回的错误信息：
  1、未登录：{'success':False,'resultMsg':'请先登录',}
  2、POST缺少X-CSRFToken：{'success':False,'resultMsg':'HTTP头部错误',} 
  3、错误的request.method：{'success':False,'resultMsg':'请求方式出错，只能为GET/POST',}
  4、POST请求缺少data：{'success':False,'resultMsg':'请求数据为空',}

  验证通过后自动获取请求体的data用json.loads()转换为对象后作为第二个参数传入到view函数中
  """
  def wrapper(fn):
    def validator(*args, **kvargs):
      # 检查是否已登录
      request = args[0]
      if not request.user.is_authenticated():
      #if len(request.COOKIES.get('sessionid', '')) != 32 or len(request.COOKIES.get('csrftoken', '')) != 32:
        return HttpResponse(json.dumps({
          'success': False,
          'resultMsg': '请先登录',
        }))
      # 检查请求方式的限定
      if method != 'ALL' and request.method != method:
        return HttpResponse(json.dumps({
          'success': False,
          'resultMsg': '请求方式出错，只能为' + method,
        }))
      else:
        # 如果是POST则检查是否存在X-CSRFToken和data
        if request.method == 'POST':
          if len(request.META.get('HTTP_X_CSRFTOKEN', '')) != 32:
            return HttpResponse(json.dumps({
              'success': False,
              'resultMsg': 'HTTP头部错误',
            }))
          if not request.POST.get('data', None):
            return HttpResponse(json.dumps({
              'success': False,
              'resultMsg': '请求数据为空',
            }))
          # POST请求验证通过，返回view函数
          return fn(request, data=json.loads(request.POST['data']))
          #return fn(*args, **kvargs)
        # GET请求不用验证，直接返回view函数
        return fn(request, data=json.loads(request.REQUEST.get('data', '{}')))
        #return fn(*args, **kvargs)
    return validator
  return wrapper

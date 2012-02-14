# coding=utf-8
"""oneingdufs.home.forms 用户表单

|- Login_form 登录表单
|- Register_form 注册表单
|- Info_form 基本信息表单
|- AtSchool_form 在校相关表单
"""

import re
from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# project import
import oneingdufs.functions as _fn
from oneingdufs.administration.models import *

class Login_form(AuthenticationForm):
  """登录表单"""
  username = forms.CharField(label='账号', max_length=20,
      widget=forms.TextInput(attrs={
        'maxlength': '20',
        'pattern': r'^(\w|\d){4,20}$',
        'required': 'required',
        'tabindex': '1',
      }))
  password = forms.CharField(label='密码',
      widget=forms.PasswordInput(attrs={
        'required': 'required',
        'tabindex': '2',
      }))
  rememberme = forms.BooleanField(label='记住我', required=False,
      widget=forms.CheckboxInput(attrs={
        'tabindex': '3',
      }))

class Register_form(forms.Form):
  """注册表单"""
  # 用户名
  username = forms.CharField(label='昵称', help_text='填写一个独一无二的昵称，一旦确定则无法更改', max_length=20,
      widget=forms.TextInput(attrs={
        'maxlength': '20',
        'pattern': r'^(\w|\d){4,20}$',
        'required': 'required',
        'placeholder': '4~20个字符',
        'tabindex': '1',
      }))
  # 密码
  password = forms.CharField(label='密码', help_text='请设置你在One in GDUFS的密码，至少6位',
      widget=forms.PasswordInput(attrs={
        'required': 'required',
        'tabindex': '2',
      }))
  # 重复密码
  password_re = forms.CharField(label='重复密码', help_text='请重复你设置的个人密码',
      widget=forms.PasswordInput(attrs={
        'required': 'required',
        'tabindex': '3',
      }))
  # 关联学号
  studentId = forms.CharField(label='关联学号', help_text='请输入你的学号，以便使用学校系统提供的功能', max_length=11,
      widget=forms.TextInput(attrs={
        'maxlength': '11',
        'pattern': r'^\d{11}$',
        'required': 'required',
        'tabindex': '4',
      }))
  # 数字广外密码
  mygdufs_pwd = forms.CharField(label='数字广外密码', help_text='输入你的数字广外密码，以便证实你的身份',
      widget=forms.PasswordInput(attrs={
        'required': 'required',
        'tabindex': '5',
      }))

  def clean(self):
    """表单验证方法集合"""
    errors = self._errors
    cleans = self.cleaned_data

    username = cleans['username']
    password = cleans['password']
    password_re = cleans['password_re']
    studentId = cleans['studentId']

    # 验证昵称是否合法、被占用
    if re.match(r'^(\w|\d){4,20}$', username) == None:
      errors['username'] = ErrorList(['只能使用英文字母、数字或下划线，长度限制为4~20个字符'])
      del cleans['username']
    elif User.objects.filter(username__iexact=username):
      errors['username'] = ErrorList(['该昵称已被使用'])
      del cleans['username']

    # 验证密码是否少于6位、过于简单
    if re.match(r'(^111111$|^123456$|^abcdef$|^asdfgh$)|^.{0,5}$', password) != None:
      errors['password'] = ErrorList(['密码过于简单，请尽量同时包含大小写字母、数字、符号并不少于6位'])
      del cleans['password']

    # 验证两次输入密码是否一致
    if password_re != password:
      errors['password_re'] = ErrorList(['两次输入密码不一致'])
      del cleans['password_re']

    # 验证学号是否合法、已存在
    if re.match(r'^20\d{9}$', studentId) == None:
      errors['studentId'] = ErrorList(['请输入一个学号'])
      del cleans['studentId']
    elif User.objects.filter(studentId__iexact=studentId):
      errors['studentId'] = ErrorList(['该学号已被关联'])
      del cleans['studentId']

    return cleans

class Info_form(forms.Form):
  """基本信息表单"""
  # 增加参数user，用于传入当前登录用户
  def __init__(self, data=None, auto_id='id_%s', initial=None, label_suffix=':',
               user=None):
    forms.Form.__init__(self, data=data, auto_id=auto_id, initial=initial, label_suffix=label_suffix)
    # login user
    self.user = user

  # 用户名、关联学号直接写死，无法更改
  # 邮箱
  email = forms.EmailField(label='邮箱', help_text='添加常用邮箱',
      required=False, error_messages={'invalid': '别骗我，这不像邮箱吧...'},
      widget=forms.TextInput(attrs={
        'type': 'email',
        'placeholder': 'admin@example.com',
        'tabindex': '1',
      }))
  # 真名
  truename = forms.CharField(label='真实姓名', help_text='需要和数字广外真实姓名相符合',
      max_length=20, required=False,
      widget=forms.TextInput(attrs={
        'maxlength': '20',
        'pattern': r'^[\u00b7\u4e00-\u9fa5]*$',
        'tabindex': '2',
      }))
  # 手机
  telnum = forms.CharField(label='手机', help_text='11位数字，添加手机号能让同学们方便地找到你',
      max_length=11, required=False,
      widget=forms.TextInput(attrs={
        'type': 'tel',
        'maxlength': '11',
        'pattern': r'^\d{11}$',
        'tabindex': '3',
      }))
  # 短号
  cornet = forms.CharField(label='短号', help_text='3~6位数字',
      max_length=6, required=False,
      widget=forms.TextInput(attrs={
        'maxlength': '6',
        'pattern': r'^\d{3,6}$',
        'tabindex': '4',
      }))
  # QQ
  qq = forms.CharField(label='QQ', max_length=10, required=False,
      widget=forms.TextInput(attrs={
        'maxlength': '10',
        'pattern': r'^\d{0,10}$',
        'tabindex': '5',
      }))

  # 所有字段均为非必填，因此需要判断值是否存在，若有值，需判断是否有更改
  def clean(self):
    """表单验证集合"""
    errors = self._errors
    cleans = self.cleaned_data
    user = self.user

    email = cleans['email']
    truename = cleans['truename']
    telnum = cleans['telnum']
    cornet = cleans['cornet']
    qq = cleans['qq']

    # 验证真名是否纯中文
    if truename and not re.match(ur'^[\u00b7\u4e00-\u9fa5]*$', unicode(truename)):
      errors['truename'] = ErrorList(['只能包含中文字符及间隔符“·”'])
      del errors['truename']

    # 验证4个字段是否有改动或unique
    tmplist = ['email', 'telnum', 'cornet', 'qq',]
    for value in tmplist:
      if not cleans[value] or self._nochange(value, cleans):
        # 提交值为空或无变动，可跳过该字段的下一步验证
        pass
      else:
        exec 'tmpresult = User.objects.filter(%s__iexact=%s)' % (value, value)
        if tmpresult:
          errors[value] = ErrorList(['该%s已被关联' % value])
          del cleans[value]

    # 验证手机号是否合法
    if 'telnum' in cleans and not re.match(r'^(\d{11})*$', telnum):
      errors['telnum'] = ErrorList(['手机号码必须为11位纯数字'])
      del cleans['telnum']

    # 验证短号是否合法
    if 'cornet' in cleans and not re.match(r'^(\d{3,6})*$', cornet):
      errors['cornet'] = ErrorList(['短号为3~6位的数字'])
      del cleans['cornet']

    # 验证QQ是否合法
    if 'qq' in cleans and not re.match(r'^\d{0,10}$', qq):
      errors['qq'] = ErrorList(['QQ号码是少于10位的数字'])
      del cleans['qq']

    return cleans

  # 因为User实例无法迭代，也即无法使用user['email']来访问，因此使用本方法来代替
  def _nochange(self, itemname, cleans):
    """判断某个字段值是否有改动"""
    user = self.user
    result = {
      'email': user.email and user.email == cleans['email'],
      'telnum': user.telnum and user.telnum == cleans['telnum'],
      'cornet': user.cornet and user.cornet == cleans['cornet'],
      'qq': user.qq and user.qq == cleans['qq'],
    }
    return result[itemname]
  
class AtSchool(forms.Form):
  """在校相关表单"""
  FACULTY_CHOICES = _fn.getChoicesTuple(Faculty, emptyText='请选择...')

  born = forms.DateField(label='出生日期', required=False,
      widget=forms.TextInput(attrs={
        'class': 'J_datepicker',
        'maxlength': '10',
        'placeholder': 'YYYY-MM-DD',
        'tabindex': '1',
      }))
  enroll = forms.DateField(label='入学年月', required=False,
      widget=forms.TextInput(attrs={
        'class': 'J_datepicker',
        'maxlength': '7',
        'placeholder': 'YYYY-MM',
        'tabindex': '2',
      }))
  faculty = forms.ChoiceField(label='学院', choices=FACULTY_CHOICES, required=False,
      widget=forms.Select(attrs={
        'style': 'width:140px;',
        'tabindex': '3',
      }))
  major = forms.ChoiceField(label='专业', choices=(('', '请选择...'),), required=False,
      widget=forms.Select(attrs={
        'style': 'width:140px;',
        'tabindex': '4',
      }))
  classlist = forms.ChoiceField(label='班级', choices=(('', '...'),), required=False,
      widget=forms.Select(attrs={
        'style': 'width:60px;',
        'tabindex': '5',
      }))

  def clean(self):
    """表单验证集合"""
    errors = self._errors
    cleans = self.cleaned_data

    born = cleans['born']
    enroll = cleans['enroll']
    faculty = cleans['faculty']
    major = cleans['major']
    classlist = cleans['classlist']

    # 只要三个框有一个非空，则三个均须非空
    if faculty or major or classlist:
      if not faculty:
        errors['faculty'] = ErrorList(['请选择学院'])
        del cleans['faculty']
      if not major:
        errors['major'] = ErrorList(['请选择专业'])
        del cleans['major']
      if not classlist:
        errors['classlist'] = ErrorList(['请选择班级'])
        del cleans['classlist']

    return cleans

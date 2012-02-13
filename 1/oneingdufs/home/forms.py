# coding=utf-8
"""oneingdufs.home.forms 用户表单

|- Login_form 登录表单
|- Register_form 注册表单
|- Home_form 基本信息表单
|- AtSchool_form 在校相关表单
"""

import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

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
  username = forms.CharField(label='昵称', help_text='填写一个独一无二的昵称，4~20个字符', max_length=20,
      widget=forms.TextInput(attrs={
        'maxlength': '20',
        'pattern': r'^(\w|\d){4,20}$',
        'required': 'required',
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
  # 保存验证通过的密码，以提供重复密码验证
  password_clear = ''

  def clean_username(self):
    """验证用户名是否被占用、合法"""
    username = self.cleaned_data['username']
    users = User.objects.filter(username__iexact=username)
    if users:
      raise forms.ValidationError('该昵称已被使用')
    if re.match(r'^(\w|\d){4,20}$', username) == None:
      raise forms.ValidationError('只能使用英文字母、数字或下划线，长度限制为4~20')
    return username

  def clean_password(self):
    """验证密码是否少于6位、过于简单"""
    pwd = self.cleaned_data['password']
    simplePwd = ('111111', '123456', 'abcdef', 'asdfgh',)
    if len(pwd) < 6:
      self.password_clear = None
      raise forms.ValidationError('密码少于6位')
    for value in simplePwd:
      if pwd == value:
        self.password_clear = None
        raise forms.ValidationError('密码过于简单')
    # 保存验证过的密码，以便和重复密码核对
    self.password_clear = pwd
    return pwd

  def clean_password_re(self):
    """验证两次输入密码是否一致"""
    pwd_re = self.cleaned_data['password_re']
    if self.password_clear == None:
      return pwd_re
    if pwd_re != self.password_clear:
      raise forms.ValidationError('两次输入的密码不一致')
    return pwd_re

  def clean_studentId(self):
    """验证学号是否合法、是否已存在"""
    studentId = self.cleaned_data['studentId']
    if re.match(r'^20\d{9}$', studentId) == None:
      raise forms.ValidationError('请输入一个学号')
    if User.objects.filter(studentId__iexact=studentId):
      raise forms.ValidationError('该学号已被关联')
    return studentId

class Home_form(forms.Form):
  """基本信息表单"""
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
        'placeholder': '张某某',
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
  
  def clean_email(self):
    """验证是否已存在邮箱"""
    email = self.cleaned_data['email']
    if not email:
      return email
    if User.objects.filter(email__iexact=email):
      raise forms.ValidationError('该邮箱已被关联')
    return email

  def clean_truename(self):
    """验证真名是否纯中文"""
    truename = self.cleaned_data['truename']
    if not truename:
      return truename
    if not re.match(ur'^[\u00b7\u4e00-\u9fa5]*$', unicode(truename)):
      raise forms.ValidationError('只能包含中文字符及间隔符“·”')
    return truename

  def clean_telnum(self):
    """验证是否为手机号、是否已存在"""
    telnum = self.cleaned_data['telnum']
    if not telnum:
      return telnum
    if not re.match(r'^(\d{11})*$', telnum):
      raise forms.ValidationError('手机号码必须为11位纯数字')
    if User.objects.filter(telnum__iexact=telnum):
      raise forms.ValidationError('该手机已被关联')
    return telnum

  def clean_cornet(self):
    """验证是否为短号、是否已存在"""
    cornet = self.cleaned_data['cornet']
    if not cornet:
      return cornet
    if not re.match(r'^(\d{3,6})*$', cornet):
      raise forms.ValidationError('短号为3~6位的数字')
    if User.objects.filter(cornet__iexact=cornet):
      raise forms.ValidationError('该短号已被关联')
    return cornet

  def clean_qq(self):
    """验证是否为QQ、是否已存在"""
    qq = self.cleaned_data['qq']
    if not qq:
      return qq
    if not re.match(r'^\d{0,10}$', qq):
      raise forms.ValidationError('QQ号码是少于10位的数字')
    if User.objects.filter(qq__iexact=qq):
      raise forms.ValidationError('该QQ已被关联')
    return qq

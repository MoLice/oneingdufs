# coding=utf-8
"""oneingdufs.home.forms 用户表单

|- Login_form 登录表单
|- Register_form 注册表单
"""

import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class Login_form(AuthenticationForm):
  """登录表单"""
  username = forms.CharField(label='账号', max_length=20)
  password = forms.CharField(label='密码', widget=forms.PasswordInput)
  rememberme = forms.BooleanField(label='记住我', required=False)

class Register_form(forms.Form):
  """注册表单"""
  username = forms.CharField(label='昵称', help_text='填写一个独一无二的昵称')
  password = forms.CharField(label='密码', help_text='请设置你在One in GDUFS的密码，至少6位', widget=forms.PasswordInput)
  password_re = forms.CharField(label='重复密码', help_text='请重复你设置的个人密码', widget=forms.PasswordInput)
  studentId = forms.CharField(label='学号', help_text='请输入你的学号，以便使用学校系统提供的功能')
  mygdufs_pwd = forms.CharField(label='数字广外密码', help_text='输入你的数字广外密码，以便证实你的身份', widget=forms.PasswordInput)
  password_clear = ''

  def clean_username(self):
    """验证用户名是否被占用"""
    # TODO 只允许英文、数字及下划线
    users = User.objects.filter(username__iexact=self.cleaned_data['username'])
    if not users:
      return self.cleaned_data['username']
    raise forms.ValidationError('该昵称已被使用')

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
    studentId = self.cleaned_data['studentId']
    if re.match(r'^20\d{9}$', studentId) == None:
      raise forms.ValidationError('请输入一个学号')
    return studentId

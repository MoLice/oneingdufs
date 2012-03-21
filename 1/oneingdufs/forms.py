# coding=utf-8
"""oneingdufs.forms 全局表单

@author MoLice<sf.molice@gmail.com>
|- EmailInput 自定义widgets
"""

from django import forms

class EmailInput(forms.TextInput):
  """<input type='email' />"""
  input_type = 'email'

class TelInput(forms.TextInput):
  """<input type='tel' />"""
  input_type = 'tel'

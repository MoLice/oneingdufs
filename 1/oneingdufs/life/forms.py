# coding=utf-8
"""oneingdufs.life.forms 校园生活forms

@author MoLice<sf.molice@gmail.com>
|- Water 订水
|- GdufsLife 后勤留言
"""

from django import forms
# project import

class Water(forms.Form):
  """订水表单"""
  BUILDING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
  )
  LAYER_CHOICES = (
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
  )
  TIME_CHOICES = (
    ('1', '11:30-12:30'),
    ('2', '12:30-13:30'),
  )
  # 宿舍
  building = forms.ChoiceField(label='栋', choices=BUILDING_CHOICES)
  layer = forms.ChoiceField(label='层', choices=LAYER_CHOICES)
  room = forms.ChoiceField(label='', choices=(('01', '01'),('02', '02')))
  number = forms.ChoiceField(label='桶', choices=(('2','2'),('1','1'),))
  time = forms.ChoiceField(label='时段', choices=TIME_CHOICES)

class GdufsLife(forms.Form):
  CAMPUS = (
    ('南校', '南校',),
    ('北校', '北校',),
  )
  TYPES = (
    ('宿舍', '宿舍',),
    ('教学', '教学',),
    ('饭堂', '饭堂',),
    ('门诊', '门诊',),
    ('其他', '其他',),
  )
  title = forms.CharField(label='标题', help_text='留言的标题', max_length=30)
  content = forms.CharField(label='内容', help_text='意见建议或问题反映，请填写详细的时间、地点、经过', widget=forms.TextInput)
  name = forms.CharField(label='姓名', max_length=20)
  email = forms.EmailField(label='邮箱', help_text='留言得到回复后我们将发送通知邮件到此邮箱')
  campus = forms.ChoiceField(label='校区', choices=CAMPUS)
  types = forms.ChoiceField(label='区域', choices=TYPES)

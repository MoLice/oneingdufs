# coding=utf-8
"""oneingdufs.life.forms 校园生活forms

@author MoLice<sf.molice@gmail.com>
|- Water 订水
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

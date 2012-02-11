# coding=utf-8
from django.db import models

class Faculty(models.Model):
  """学院"""
  name = models.CharField(max_length=20, unique=True)

  def __str__(self):
    return self.name

class Major(models.Model):
  """专业"""
  name = models.CharField(max_length=20, unique=True)
  facultyId = models.ForeignKey('Faculty')

  def __str__(self):
    return self.name

class ClassList(models.Model):
  """班级"""
  name = models.CharField(max_length=20, unique=True)
  majorId = models.ForeignKey('Major')

  def __str__(self):
    return self.name

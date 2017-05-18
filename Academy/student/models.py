#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Department(models.Model):
    dno = models.CharField(max_length = 20)
    dname = models.CharField(max_length = 20,null = False)
    def __unicode__(self):
        return '%s,%s'%(self.dno,self.dname)

class Teacher(models.Model):
    tno = models.CharField(max_length = 20)
    tname = models.CharField(max_length = 20,null = False)
    department = models.ForeignKey(Department)

    def __unicode__(self):
        return '%s,%s'%(self.tno,self.tname)

class Student(models.Model):
    sno = models.CharField(max_length = 20)
    sname = models.CharField(max_length = 20,null = False)
    telenum = models.CharField(max_length = 20,null = True)
    department = models.ForeignKey(Department)
    def __unicode__(self):
        return '%s,%s'%(self.sno,self.sname)

class Course(models.Model):
    cno = models.CharField(max_length = 20)
    cname = models.CharField(max_length = 20,null = False)
    credit = models.IntegerField(null=False)
    department = models.ForeignKey(Department)
    def __unicode__(self):
        return '%s'%(self.cno)

class Opencourse(models.Model):
    term = models.IntegerField(null=False)
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher)
    time = models.CharField(max_length = 30,null = False)
    class Meta:
            unique_together = ('term','course','teacher')
    primary = ('term','course','teacher')
    def __unicode__(self):
        return '%d,%s,%s'%(self.term,self.course,self.teacher)

class Selection(models.Model):
    student = models.ForeignKey(Student)
    opencourse = models.ForeignKey(Opencourse)
    usual = models.FloatField(null=True)
    exam = models.FloatField(null=True)
    total = models.FloatField(null=True)
    class Meta:
            unique_together = ('student','opencourse')
    primary = ('student','opencourse')
    def __unicode__(self):
        return '%f'%(self.total)

# Create your models here.

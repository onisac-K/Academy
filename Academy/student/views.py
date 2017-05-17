# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from student.models import Selection
from student.models import Teacher
from student.models import Department
from student.models import Opencourse
from student.models import Student
from student.models import Course
# Create your views here.


def student(req):
    username = req.session.get('username')
    course_info = list(Selection.objects.filter(student__sno = username))
    
    for i in course_info:
        print i.opencourse.course.cname

    #studentname = Student.objects.filter(sno = username).get(id = 1).sname
    personalInfo = Student.objects.filter(sno = username).get(id = 1)
    return render(req, 'student/student.html',{'course_info':course_info,'personalInfo':personalInfo})

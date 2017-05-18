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

class SelectForm(forms.Form):
    courseNo = forms.CharField(label='courseNo',max_length=100)
    teacherNo = forms.CharField(label='teacherNo',max_length=100)


#选课
def select(req):
    if req.method == 'POST':
        sf = SelectForm(req.POST)
        if sf.is_valid():
            #获得表单数据
            courseNo = sf.cleaned_data['courseNo']
            teacherNo = sf.cleaned_data['teacherNo']
            print(courseNo)
            print(teacherNo)
            #添加到数据库
            username = req.session.get('username')
            print(username)
            course = Opencourse.objects.filter(course__cno = courseNo)
            student = Student.objects.filter(sno = username)
            for courseItem in course:
                for studentItem in student:
                    Selection.objects.create(student = studentItem,opencourse = courseItem,usual=0,exam=0,total=0)
                    # print(student.sno)
            return HttpResponse(select)
    else:
        sf = SelectForm()
    return render(req, 'student/student.html',{'sf':sf})


def student(req):
    # nowtime = 163
    username = req.session.get('username')
    course_info = list(Selection.objects.filter(student__sno = username))
    # open_info = []
    open_info = list(Opencourse.objects.filter(term = 163))

    for i in course_info:
        print i.opencourse.course.cname
    # for i in open_info:
    #     print i.course.cname

    #studentname = Student.objects.filter(sno = username).get(id = 1).sname
    personalInfo = Student.objects.filter(sno = username).get(id = 1)
    return render(req, 'student/student.html',{'course_info':course_info,'personalInfo':personalInfo,'open_info':open_info})

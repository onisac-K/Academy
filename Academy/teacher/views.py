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


def teacher(req):
    username = req.session.get('username')
    #print(username)
    student_info = Selection.objects.filter(opencourse__teacher__tno = username)
    student_list = list(student_info)
    openlist = list(Opencourse.objects.filter(teacher__tno = username))
    print openlist
    teacherinf = Teacher.objects.filter(tno = username).get(id = 1)
    teachername = teacherinf.tname

    if req.method == 'POST':
        buttonlist = req.POST.getlist('key','')
        print buttonlist[0]
        for i in openlist:
            if (int)(i.id) == (int)(buttonlist[0]):
                course = i
                print course.course.cname
        print course
        thiscourse_student_list = Selection.objects.filter(opencourse = course)
        print thiscourse_student_list
        return render(req, 'teacher/score.html',{'thiscourse_student_list':thiscourse_student_list,'opencourse':course,'openlist':openlist,'teachername':teachername})

    #for i in student_list :
    #    print i.student.sno,i.student.sname,i.student.telenum,i.student.department.dname

    #print teachername
    return render(req, 'teacher/teacher.html',{'student_list':student_list,'openlist':openlist,'teachername':teachername})

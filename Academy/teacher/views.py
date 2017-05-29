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
        req.session['cno'] = course.course.cno
        response = HttpResponseRedirect('/teacher/score/')
        return response

    #for i in student_list :
    #    print i.student.sno,i.student.sname,i.student.telenum,i.student.department.dname

    #print teachername
    return render(req, 'teacher/teacher.html',{'student_list':student_list,'openlist':openlist,'teachername':teachername})

def score(req):
    cno = req.session.get('cno')
    username = req.session.get('username')
    course = Opencourse.objects.filter(course__cno = cno).filter(teacher__tno = username)[0];
    student_info = Selection.objects.filter(opencourse__teacher__tno = username)
    student_list = list(student_info)
    openlist = list(Opencourse.objects.filter(teacher__tno = username))
    teacherinf = Teacher.objects.filter(tno = username).get(id = 1)
    teachername = teacherinf.tname
    thiscourse_student_list = Selection.objects.filter(opencourse__course__cno = cno).order_by("student__sno")
    if req.method == 'POST':
        for i in thiscourse_student_list:
            openInf = req.POST.getlist(i.student.sno,'')
            usual = (float)(openInf[0])
            exam = (float)(openInf[1])
            rate = i.opencourse.rate
            total = exam*rate + usual*(1-rate)
            grade = total
            if grade < 60:
                gpa='0'
            elif grade < 64:
                gpa='1.0'
            elif grade < 66:
                gpa='1.5'
            elif grade < 68:
                gpa='1.8'
            elif grade < 72:
                gpa='2.0'
            elif grade < 75:
                gpa='2.3'
            elif grade < 78:
                gpa='2.7'
            elif grade < 82:
                gpa='3.0'
            elif grade < 85:
                gpa='3.3'
            elif grade < 90:
                gpa='3.7'
            else:
                gpa='4.0'
            print usual,exam,rate,total
            i.usual = usual
            i.exam = exam
            i.total = total
            i.gpa = gpa
            i.save()
            print openInf
            response = HttpResponseRedirect('/teacher/score/')
            return response
    return render(req, 'teacher/score.html',{'thiscourse_student_list':thiscourse_student_list,'opencourse':course,'openlist':openlist,'teachername':teachername})

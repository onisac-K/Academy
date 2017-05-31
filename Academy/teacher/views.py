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
nowterm = 163
highest = 0.0
lowest = 100.0
average_grade = 0.0
average_point = 0.0
upper_people = 0
lower_people = 0
Size = 0
def teacher(req):
    username = req.session.get('username')
    student_info = Selection.objects.filter(opencourse__teacher__tno = username)
    student_list = list(student_info)
    openlist = list(Opencourse.objects.filter(teacher__tno = username).filter(term = nowterm))
    teacherinf = Teacher.objects.filter(tno = username).get(id = 1)
    teachername = teacherinf.tname

    if req.method == 'POST':
        buttonlist = req.POST.getlist('key','')
        for i in openlist:
            if (int)(i.id) == (int)(buttonlist[0]):
                course = i
        req.session['cno'] = course.course.cno
        response = HttpResponseRedirect('/teacher/score/')
        return response

    return render(req, 'teacher/teacher.html',{'openlist':openlist,'teachername':teachername})

def score(req):
    cno = req.session.get('cno')
    username = req.session.get('username')
    course = Opencourse.objects.filter(course__cno = cno).filter(teacher__tno = username)[0];
    student_info = Selection.objects.filter(opencourse__teacher__tno = username)
    student_list = list(student_info)
    openlist = list(Opencourse.objects.filter(teacher__tno = username))
    teacherinf = Teacher.objects.filter(tno = username).get(id = 1)
    teachername = teacherinf.tname
    thiscourse_student_list = list(Selection.objects.filter(opencourse__course__cno = cno).filter(opencourse__teacher__tno = username).filter(opencourse__term = nowterm).order_by("student__sno"))
    highest = 0.0
    lowest = 100.0
    average_grade = 0.0
    average_point = 0.0
    upper_people = 0
    lower_people = 0
    cnt = 0
    for i in thiscourse_student_list:
        if not(i.total is None):
            average_grade = average_grade + i.total
            highest = max(highest,i.total)
            lowest = min(lowest,i.total)

            if i.total >= 60.0:
                upper_people = upper_people + 1
            else:
                lower_people = lower_people + 1

        if not(i.gpa is None):
            cnt += 1
            average_point = average_point + float(i.gpa)

    average_grade /= cnt
    average_point /= cnt

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
            i.usual = usual
            i.exam = exam
            i.total = total
            i.gpa = gpa
            i.save()
            response = HttpResponseRedirect('/teacher/score/')
        return response
    
    return render(req, 'teacher/score.html',{'lower_people':lower_people,'upper_people':upper_people,'lowest':lowest,'highest':highest,'average_point':average_point,'average_grade':average_grade,'thiscourse_student_list':thiscourse_student_list,'opencourse':course,'openlist':openlist,'teachername':teachername})

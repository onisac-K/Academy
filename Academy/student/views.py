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

nowterm = 163

def select(req):
    query_info = {}
    username = req.session.get('username')
    select_info = list(Selection.objects.filter(student__sno = username,opencourse__term = nowterm))
    # array = [[0] * 5] * 13
    matrix = [[0 for i in range(5)] for i in range(13)]
    dict = {'Mon':0,'Tue':1,'Wen':2,'Thu':3,'Fri':4}
    for item in select_info:
        day = item.opencourse.time[:3]
        start = int(item.opencourse.time[5])
        end = int(item.opencourse.time[7])

        for i in range(start-1,end):
            matrix[i][dict[day]] = 1

    personalInfo = Student.objects.filter(sno = username).get(id = 1)

    if req.method == 'POST':
        buttonlist = req.POST.getlist('key','')

        if (int)(buttonlist[0]) == -1:
            courseNo = req.POST.get('courseNo')
            courseName = req.POST.get('courseName')
            teacherName = req.POST.get('teacherName')
            username = req.session.get('username')
            query_info = list(Opencourse.objects.filter(term = nowterm,course__cno__contains = courseNo,course__cname__contains = courseName,teacher__tname__contains = teacherName))
        else:
            courseNo = buttonlist[0][:8]
            teacherNo = buttonlist[0][8:]
            student = Student.objects.filter(sno = username)
            opencourse = Opencourse.objects.filter(course__cno = courseNo).filter(teacher__tno = teacherNo)

            for item in opencourse:
                day = item.time[:3]
                start = int(item.time[5])
                end = int(item.time[7])
                for i in range(start-1,end):
                    if matrix[i][dict[day]] == 1:
                        return HttpResponseRedirect('/student/selection')

            for courseItem in opencourse:
                for studentItem in student:
                    Selection.objects.create(student = studentItem,opencourse = courseItem,usual=0,exam=0,total=0)

            return HttpResponseRedirect('/student/selection')

    return render(req, 'student/selection.html',{'query_info':query_info,'select_info':select_info,'personalInfo':personalInfo})

def drop(req):
    username = req.session.get('username')
    select_info = list(Selection.objects.filter(student__sno = username,opencourse__term = nowterm))
    personalInfo = Student.objects.filter(sno = username).get(id = 1)

    if req.method == 'POST':
        buttonlist = req.POST.getlist('key','')
        courseNo = buttonlist[0][:8]
        teacherNo = buttonlist[0][8:]
        student = Student.objects.filter(sno = username)
        opencourse = Opencourse.objects.filter(course__cno = courseNo).filter(teacher__tno = teacherNo)

        for courseItem in opencourse:
            for studentItem in student:
                Selection.objects.filter(student = studentItem,opencourse = courseItem).delete()

        return HttpResponseRedirect('/student/drop')

    return render(req, 'student/drop.html',{'select_info':select_info,'personalInfo':personalInfo})

def grade(req):
    username = req.session.get('username')
    personalInfo = Student.objects.filter(sno = username).get(id = 1)
    select_info = list(Selection.objects.filter(student__sno = username))

    return render(req, 'student/grade.html',{'select_info':select_info,'personalInfo':personalInfo})

def student(req):
    username = req.session.get('username')
    personalInfo = Student.objects.filter(sno = username).get(id = 1)
    return render(req, 'student/student.html',{'personalInfo':personalInfo})

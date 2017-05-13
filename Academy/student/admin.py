# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from student.models import Department
from student.models import Teacher
from student.models import Student
from student.models import Course
from student.models import Opencourse
from student.models import Selection
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Opencourse)
admin.site.register(Selection)
# Register your models here.

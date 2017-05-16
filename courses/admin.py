# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Course, Lesson
# Register your models here.
#Lesson inside of Course
class LessonInline(admin.TabularInline):
    model = Lesson

class CourseAdmin(admin.ModelAdmin):
    #redoslijed atributa za kurs
    fieldsets = [
	('About the Course', {'fields': ['course_name']}),
	('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}), 
    ]
    inlines = [LessonInline]
    list_display = ('course_name', 'pub_date')

admin.site.register(Course, CourseAdmin)

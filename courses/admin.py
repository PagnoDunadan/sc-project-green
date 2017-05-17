from __future__ import unicode_literals

from django.contrib import admin
from .models import Course, Lesson, Text


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0

class TextInline(admin.TabularInline):
    model = Text
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
    ('About the Course', {'fields': ['course_name']}),
    ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}), 
    ]
    inlines = [LessonInline]
    list_display = ('course_name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['course_name']

class LessonAdmin(admin.ModelAdmin):
    fieldsets = [
    ('About the Lesson', {'fields': ['lesson_name']}),
    ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}), 
    ]
    inlines = [TextInline]
    list_display = ('lesson_name', 'course', 'pub_date')
    list_filter = ['course']
    search_fields = ['lesson_name']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)

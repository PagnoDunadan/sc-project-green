from __future__ import unicode_literals

from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    owner = models.CharField(max_length=100, null=True)
    course_picture = models.URLField(max_length=300)

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.lesson_name


class Text(models.Model):
    content = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_video = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return self.content

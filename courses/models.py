# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    
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
    text_key = models.ForeignKey(Lesson)

class Video(models.Model):
    URL = models.URLField(max_length=50)
    video_key = models.ForeignKey(Lesson)


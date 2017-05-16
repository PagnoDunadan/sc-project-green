# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Course, Lesson
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'courses/main.html'
    context_object_name = 'latest_courses_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:5]

class DetailView(generic.ListView):
    #model = Course
    template_name = 'courses/detail.html'

    context_object_name = 'latest_lessons_list'

    def get_queryset(self):
        return Lesson.objects.filter(course__id=4)


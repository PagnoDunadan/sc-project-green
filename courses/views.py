from __future__ import unicode_literals
from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Lesson, Text



class CoursesView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/main.html'
    context_object_name = 'latest_courses_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')


class CreateCourseView(LoginRequiredMixin, generic.CreateView):
    model = Course
    fields = ['course_name']

    def form_valid(self, form):
        form.instance.pub_date = datetime.now()
        return super(CreateCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:courses')


class UpdateCourseView(LoginRequiredMixin, generic.UpdateView):
    model = Course
    fields = ['course_name']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('courses:courses')


class DeleteCourseView(LoginRequiredMixin, generic.DeleteView):
    model = Course

    def get_success_url(self):
        return reverse_lazy('courses:courses')


class CourseView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/course.html'
    context_object_name = 'latest_lessons_list'

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['pk'])


class CreateLessonView(LoginRequiredMixin, generic.CreateView):
    model = Lesson
    fields = ['lesson_name']

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.course_id = self.kwargs['pk']
        lesson.pub_date = datetime.now()
        return super(CreateLessonView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:course', kwargs = {'pk' : self.kwargs['pk'] })


class UpdateLessonView(LoginRequiredMixin, generic.UpdateView):
    model = Lesson
    fields = ['lesson_name']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('courses:course', kwargs = {'pk' : self.object.course_id })


class DeleteLessonView(LoginRequiredMixin, generic.DeleteView):
    model = Lesson

    def get_success_url(self):
        return reverse_lazy('courses:course', kwargs = {'pk' : self.object.course_id })


class LessonView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/lesson.html'
    context_object_name = 'lesson_content'

    def get_queryset(self):
        return Text.objects.filter(lesson_id=self.kwargs['pk']).order_by('-priority')


class CreateTextView(LoginRequiredMixin, generic.CreateView):
    model = Text
    fields = ['content', 'is_video', 'priority']

    def form_valid(self, form):
        text = form.save(commit=False)
        text.lesson_id = self.kwargs['pk']
        return super(CreateTextView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:lesson', kwargs = {'pk' : self.kwargs['pk'] })


class TextUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Text
    fields = ['content', 'is_video', 'priority']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('courses:lesson', kwargs = {'pk' : self.object.lesson_id })

class TextDelete(LoginRequiredMixin, generic.DeleteView):
    model = Text

    def get_success_url(self):
        return reverse_lazy('courses:lesson', kwargs = {'pk' : self.object.lesson_id })

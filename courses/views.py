from __future__ import unicode_literals
from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

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

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs['course_id'])

    def get_success_url(self):
        return reverse_lazy('courses:courses')

    def get_context_data(self, **kwargs):
        context = super(UpdateCourseView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class DeleteCourseView(LoginRequiredMixin, generic.DeleteView):
    model = Course

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs['course_id'])

    def get_success_url(self):
        return reverse_lazy('courses:courses')

    def get_context_data(self, **kwargs):
        context = super(DeleteCourseView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class CourseView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/course.html'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.get(id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class LessonsView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/lessons.html'
    context_object_name = 'latest_lessons_list'

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super(LessonsView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class CreateLessonView(LoginRequiredMixin, generic.CreateView):
    model = Lesson
    fields = ['lesson_name']

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.course_id = self.kwargs['course_id']
        lesson.pub_date = datetime.now()
        return super(CreateLessonView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:lessons', kwargs = {'course_id' : self.kwargs['course_id'] })

    def get_context_data(self, **kwargs):
        context = super(CreateLessonView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class UpdateLessonView(LoginRequiredMixin, generic.UpdateView):
    model = Lesson
    fields = ['lesson_name']
    template_name_suffix = '_update_form'

    def get_object(self):
        return get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])

    def get_success_url(self):
        return reverse_lazy('courses:lessons', kwargs = {'course_id' : self.object.course_id })

    def get_context_data(self, **kwargs):
        context = super(UpdateLessonView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        return context


class DeleteLessonView(LoginRequiredMixin, generic.DeleteView):
    model = Lesson

    def get_object(self):
        return get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])

    def get_success_url(self):
        return reverse_lazy('courses:lessons', kwargs = {'course_id' : self.object.course_id })

    def get_context_data(self, **kwargs):
        context = super(DeleteLessonView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        return context


class LessonView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/lesson.html'
    context_object_name = 'lesson_content'

    def get_queryset(self):
        return Text.objects.filter(lesson_id=self.kwargs['lesson_id']).order_by('-priority')

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        return context


class CreateTextView(LoginRequiredMixin, generic.CreateView):
    model = Text
    fields = ['content', 'is_video', 'priority']

    def form_valid(self, form):
        text = form.save(commit=False)
        text.lesson_id = self.kwargs['lesson_id']
        return super(CreateTextView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:lesson', kwargs = {'course_id' : self.kwargs['course_id'], 'lesson_id' : self.kwargs['lesson_id'] })

    def get_context_data(self, **kwargs):
        context = super(CreateTextView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        return context


class UpdateTextView(LoginRequiredMixin, generic.UpdateView):
    model = Text
    fields = ['content', 'is_video', 'priority']
    template_name_suffix = '_update_form'

    def get_object(self):
        return get_object_or_404(Text, pk=self.kwargs['text_id'])

    def get_success_url(self):
        return reverse_lazy('courses:lesson', kwargs = {'course_id' : self.kwargs['course_id'], 'lesson_id' : self.kwargs['lesson_id'] })

    def get_context_data(self, **kwargs):
        context = super(UpdateTextView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        context['text_id'] = self.kwargs['text_id']
        return context


class DeleteTextView(LoginRequiredMixin, generic.DeleteView):
    model = Text

    def get_object(self):
        return get_object_or_404(Text,pk=self.kwargs['text_id'])

    def get_success_url(self):
        return reverse_lazy('courses:lesson', kwargs = {'course_id' : self.kwargs['course_id'], 'lesson_id' : self.kwargs['lesson_id'] })

    def get_context_data(self, **kwargs):
        context = super(DeleteTextView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        context['text_id'] = self.kwargs['text_id']
        return context

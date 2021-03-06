from __future__ import unicode_literals
from datetime import datetime
import sys

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.views import generic

from .models import Course, Lesson, Text, Exam, Submission


def handler403(request):
    response = render_to_response('403.html', {}, context_instance=RequestContext(request))
    response.status_code = 403
    return response


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response


class UrlRequired(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            Course.objects.get(pk=self.kwargs['course_id'])
        except Course.DoesNotExist:
            raise Http404

        if 'lesson_id' in kwargs:
            try:
                Lesson.objects.get(pk=self.kwargs['lesson_id'])
            except Lesson.DoesNotExist:
                raise Http404
            if (kwargs['course_id'] != str(Lesson.objects.values_list('course_id', flat=True).get(pk=self.kwargs['lesson_id']))):
                raise Http404

        if 'text_id' in kwargs:
            try:
                Text.objects.get(pk=self.kwargs['text_id'])
            except Text.DoesNotExist:
                raise Http404
            if (kwargs['lesson_id'] != str(Text.objects.values_list('lesson_id', flat=True).get(pk=self.kwargs['text_id']))):
                raise Http404
        return super(UrlRequired, self).dispatch(request, *args, **kwargs)


class CourseOwnerRequired(object):
    def dispatch(self, request, *args, **kwargs):
        if (self.request.user.id != Course.objects.values_list('course_owner', flat=True).get(pk=self.kwargs['course_id'])):
            raise PermissionDenied
        return super(CourseOwnerRequired, self).dispatch(request, *args, **kwargs)


class CoursesView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/main.html'
    context_object_name = 'latest_courses_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')


class CreateCourseView(LoginRequiredMixin, generic.CreateView):
    model = Course
    fields = ['course_name', 'course_picture', 'course_about']

    def form_valid(self, form):
        form.instance.pub_date = datetime.now()
        form.instance.course_owner = self.request.user
        return super(CreateCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:course', kwargs = {'course_id' : self.object.id })


class UpdateCourseView(LoginRequiredMixin, generic.UpdateView):
    model = Course
    fields = ['course_name', 'course_picture', 'course_about']
    template_name_suffix = '_update_form'

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs['course_id'])

    def get_success_url(self):
        return reverse_lazy('courses:course', kwargs = {'course_id' : self.kwargs['course_id'] })

    def get_context_data(self, **kwargs):
        context = super(UpdateCourseView, self).get_context_data(**kwargs)
        if (self.request.user != context['course'].course_owner):
            raise Http404
        context['course_id'] = self.kwargs['course_id']
        context['course_name'] = context['course'].course_name
        return context


class DeleteCourseView(LoginRequiredMixin, generic.DeleteView):
    model = Course

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs['course_id'])

    def get_success_url(self):
        return reverse_lazy('courses:courses')

    def get_context_data(self, **kwargs):
        context = super(DeleteCourseView, self).get_context_data(**kwargs)
        if (self.request.user != context['course'].course_owner):
            raise Http404
        context['course_id'] = self.kwargs['course_id']
        context['course_name'] = context['course'].course_name
        return context


class CourseView(LoginRequiredMixin, generic.ListView):
    template_name = 'courses/course.html'
    context_object_name = 'course'

    def get_queryset(self):
        return get_object_or_404(Course, pk=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['course_name'] = context['course'].course_name
        return context


class LessonsView(LoginRequiredMixin, UrlRequired, generic.ListView):
    template_name = 'courses/lessons.html'
    context_object_name = 'latest_lessons_list'

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super(LessonsView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['course_owner'] = Course.objects.values_list('course_owner', flat=True).get(pk=self.kwargs['course_id'])
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        return context


class CreateLessonView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.CreateView):
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
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        return context


class UpdateLessonView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.UpdateView):
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
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        context['lesson_name'] = context['lesson'].lesson_name
        return context


class DeleteLessonView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.DeleteView):
    model = Lesson

    def get_object(self):
        return get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])

    def get_success_url(self):
        return reverse_lazy('courses:lessons', kwargs = {'course_id' : self.object.course_id })

    def get_context_data(self, **kwargs):
        context = super(DeleteLessonView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        context['lesson_name'] = context['lesson'].lesson_name
        return context


class LessonView(LoginRequiredMixin, UrlRequired, generic.ListView):
    template_name = 'courses/lesson.html'
    context_object_name = 'lesson_content'

    def get_queryset(self):
        return Text.objects.filter(lesson_id=self.kwargs['lesson_id']).order_by('-priority')

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['lesson_id'] = self.kwargs['lesson_id']
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        context['lesson_name'] = Lesson.objects.values_list('lesson_name', flat=True).get(pk=self.kwargs['lesson_id'])
        context['course_owner'] = Course.objects.values_list('course_owner', flat=True).get(pk=self.kwargs['course_id'])
        return context


class CreateTextView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.CreateView):
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
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        context['lesson_name'] = Lesson.objects.values_list('lesson_name', flat=True).get(pk=self.kwargs['lesson_id'])
        return context


class UpdateTextView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.UpdateView):
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
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        context['lesson_name'] = Lesson.objects.values_list('lesson_name', flat=True).get(pk=self.kwargs['lesson_id'])
        return context


class DeleteTextView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.DeleteView):
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
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        context['lesson_name'] = Lesson.objects.values_list('lesson_name', flat=True).get(pk=self.kwargs['lesson_id'])
        return context


#################################################   EXAMS PROTOTYPE   ##################################################

class ExamView(LoginRequiredMixin, UrlRequired, generic.ListView):
    template_name = 'courses/exam.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Exam.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super(ExamView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        context['course_owner'] = Course.objects.values_list('course_owner', flat=True).get(pk=self.kwargs['course_id'])
        return context


class CreateQuestionView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.CreateView):
    model = Exam
    fields = ['question', 'first_answer', 'second_answer', 'third_answer', 'fourth_answer', 'correct_answer']

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:exam', kwargs = {'course_id' : self.kwargs['course_id'] })

    def get_context_data(self, **kwargs):
        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        return context


class UpdateQuestionView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.UpdateView):
    model = Exam
    fields = ['question', 'first_answer', 'second_answer', 'third_answer', 'fourth_answer', 'correct_answer']
    template_name_suffix = '_update_form'

    def get_object(self):
        return get_object_or_404(Exam, pk=self.kwargs['question_id'])

    def get_success_url(self):
        return reverse_lazy('courses:exam', kwargs = {'course_id' : self.kwargs['course_id'] })

    def get_context_data(self, **kwargs):
        context = super(UpdateQuestionView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['question_id'] = context['exam'].id
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        return context


class DeleteQuestionView(LoginRequiredMixin, UrlRequired, CourseOwnerRequired, generic.DeleteView):
    model = Exam

    def get_object(self):
        return get_object_or_404(Exam, pk=self.kwargs['question_id'])

    def get_success_url(self):
        return reverse_lazy('courses:exam', kwargs = {'course_id' : self.kwargs['course_id'] })

    def get_context_data(self, **kwargs):
        context = super(DeleteQuestionView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['question_id'] = context['exam'].id
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        return context


class StartExam(LoginRequiredMixin, UrlRequired, generic.ListView):
    template_name = 'courses/exam_start.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Exam.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super(StartExam, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        if 'slug' in self.kwargs:
            context['error_message'] = self.kwargs['slug']
            context['slug'] = self.kwargs['slug']
        context['course_name'] = Course.objects.values_list('course_name', flat=True).get(pk=self.kwargs['course_id'])
        return context


def SubmitExam(request, course_id):
    questions = Exam.objects.filter(course_id=course_id)

    for question in questions:
        try:
            Submission.objects.create(exam=question, student=request.user, answer=request.POST[str(question.id)][0])
        except KeyError:
            error_message = "noanswer"
            return HttpResponseRedirect(reverse('courses:exam_error', args=(course_id, error_message)))
    else:
        return HttpResponseRedirect(reverse('courses:exam', args=(course_id,)))

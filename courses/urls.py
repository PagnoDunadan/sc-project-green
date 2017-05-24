from django.conf.urls import url

from . import views

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.CoursesView.as_view(), name='courses'), # /courses/
    url(r'^new/$', views.CreateCourseView.as_view(), name='create_course'), # /courses/new/
    url(r'^(?P<course_id>[0-9]+)/edit/$', views.UpdateCourseView.as_view(), name='update_course'), # /courses/1/edit/
    url(r'^(?P<course_id>[0-9]+)/delete/$', views.DeleteCourseView.as_view(), name='delete_course'), # /courses/1/delete/
    url(r'^(?P<course_id>[0-9]+)/$', views.CourseView.as_view(), name='course'), # /courses/1/
    url(r'^(?P<course_id>[0-9]+)/lessons/$', views.LessonsView.as_view(), name='lessons'), # /courses/1/lessons/
    url(r'^(?P<course_id>[0-9]+)/lessons/create/$', views.CreateLessonView.as_view(), name='create_lesson'), # /courses/1/lessons/create/
    url(r'^(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/edit/$', views.UpdateLessonView.as_view(), name='update_lesson'), # /courses/1/lessons/1/update/
    url(r'^(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/delete/$', views.DeleteLessonView.as_view(), name='delete_lesson'), # /courses/1/lessons/1/delete/
    url(r'^(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/$', views.LessonView.as_view(), name='lesson'), # /courses/1/lessons/1/
    url(r'^(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/text/create/$', views.CreateTextView.as_view(), name='create_text'), # /courses/1/lessons/1/text/create/
    url(r'^(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/text/(?P<text_id>[0-9]+)/edit/$', views.UpdateTextView.as_view(), name='update_text'), # /courses/1/lessons/1/text/1/edit/
    url(r'^(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/text/(?P<text_id>[0-9]+)/delete/$', views.DeleteTextView.as_view(), name='delete_text'), # /courses/1/lessons/1/text/1/delete/
    url(r'^(?P<course_id>[0-9]+)/exam/$', views.ExamView.as_view(), name='exam'), # /courses/1/exam/
    url(r'^(?P<course_id>[0-9]+)/exam/questions/$', views.ExamView.as_view(), name='exam_questions'), # /courses/1/exam/questions/
    url(r'^(?P<course_id>[0-9]+)/exam/questions/new$', views.CreateQuestionView.as_view(), name='new_question'), # /courses/1/exam/questions/new
    url(r'^(?P<course_id>[0-9]+)/exam/questions/(?P<question_id>[0-9]+)/update$', views.UpdateQuestionView.as_view(), name='update_question'), # /courses/1/exam/questions/1/update
    url(r'^(?P<course_id>[0-9]+)/exam/questions/(?P<question_id>[0-9]+)/delete$', views.DeleteQuestionView.as_view(), name='delete_question'), # /courses/1/exam/questions/1/delete
]

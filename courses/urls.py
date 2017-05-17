from django.conf.urls import url

from . import views

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.CoursesView.as_view(), name='courses'),
    url(r'^course/create$', views.CreateCourseView.as_view(), name='create_course'),
    url(r'^course/(?P<pk>[0-9]+)/edit$', views.UpdateCourseView.as_view(), name='update_course'),
    url(r'^course/(?P<pk>[0-9]+)/delete$', views.DeleteCourseView.as_view(), name='delete_course'),
    url(r'^course/(?P<pk>[0-9]+)/$', views.CourseView.as_view(), name='course'),
    url(r'^course/(?P<pk>[0-9]+)/lesson/create/$', views.CreateLessonView.as_view(), name='create_lesson'),
    url(r'^lesson/(?P<pk>[0-9]+)/edit$', views.UpdateLessonView.as_view(), name='update_lesson'),
    url(r'^lesson/(?P<pk>[0-9]+)/delete$', views.DeleteLessonView.as_view(), name='delete_lesson'),
    url(r'^lesson/(?P<pk>[0-9]+)/$', views.LessonView.as_view(), name='lesson'),
    url(r'^lesson/(?P<pk>[0-9]+)/text/create/$', views.CreateTextView.as_view(), name='create_text'),
    url(r'^text/(?P<pk>[0-9]+)/edit$', views.TextUpdate.as_view(), name='text_update'),
    url(r'^text/(?P<pk>[0-9]+)/delete$', views.TextDelete.as_view(), name='text_delete'),
]

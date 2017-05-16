from django.conf.urls import url

from . import views

app_name = 'courses'
urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='courses'),
    url(r'^$', views.IndexView.as_view(), name='courses'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #ulr(r'^(?P<course_id>[0-9]+)/lessons/$', views.lessons, name='lessons'),
]

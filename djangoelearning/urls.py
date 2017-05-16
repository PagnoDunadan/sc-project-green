"""djangoelearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='homepage/index.html'), name='home'),
    #url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    #url(r'^login/$', auth_views.login, {'template_name': './registration/login.html'}, name='login'),
    #url(r'^logout/$', auth_views.logout, name='logout'),
    #url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logged_out.html'}, name='logout'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^courses/', include('courses.urls')),
    url(r'^admin/', admin.site.urls),
]

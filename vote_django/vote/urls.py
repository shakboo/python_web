# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'vote'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^question/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^all/$', views.all,name='all'),
]
#coding=utf-8

from django.conf.urls import url
from . import views

app_name = 'regress'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r"^detail/(?P<version>.+)/$", views.detail, name="detail"),
    url(r'^pot/(?P<pk>.+)/$', views.pot, name="pot"),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Question(models.Model):
    author = models.ForeignKey(User,verbose_name='发起人')
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField('标题', max_length=50)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vote:detail', kwargs={'pk':self.pk})

    #默认时间降序排列
    class Meta:
        ordering = ['-created_time']

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField('问题',max_length=200)
    votes = models.IntegerField(default=0)


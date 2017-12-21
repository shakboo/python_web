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
    #需要加一个标识来确认此用户已经投过票
    already_votes = models.CharField(max_length=1000,default="")

    CHOOSE_BOX = (
        (u'choose_vote',u'投票'),
        (u'choose_qa',u'问答'),
    )

    choose = models.CharField('类型',max_length=15,choices=CHOOSE_BOX,default="投票")

    def __unicode__(self):
        return self.title

    #进行投票问卷详情页跳转
    def get_absolute_url(self):
        return reverse('vote:detail', kwargs={'pk':self.pk})

    #进行投票问卷结果详情页跳转
    def get_absolute_already_url(self):
        return reverse('vote:result',kwargs={'pk':self.pk})


    #默认时间降序排列
    class Meta:
        ordering = ['-created_time']

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField('问题',max_length=200)

    votes = models.IntegerField(default=0)
    who_votes = models.CharField(max_length=1000,default="",blank=True)


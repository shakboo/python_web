# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass

class Version(models.Model):
    version = models.DateField(u'周版本')

    def __unicode__(self):
        return unicode(self.version)

class Context(models.Model):
    version = models.ForeignKey(Version)
    count = models.CharField(u'第几次回归', choices=[(u'第一次回归',u'第一次回归'),(u'第二次回归',u'第二次回归'),], default='第一次回归',max_length=10)
    rangen = models.CharField(u'范围', choices=[(u'灰度',u'灰度'),(u'非灰度',u'非灰度'),(u'小组',u'小组'),], default=u'灰度',max_length=10)
    title = models.TextField(u'内容', max_length=200)
    detail = models.TextField(u'补充说明', max_length=200)
    status = models.BooleanField(u'状态', default=False)
    handler = models.CharField(u'确认人', max_length=10,default='')
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

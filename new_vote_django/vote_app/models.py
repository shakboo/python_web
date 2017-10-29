# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
#向后兼容Django版本
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User,Question,Choice

admin.site.register(User)


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title','author']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
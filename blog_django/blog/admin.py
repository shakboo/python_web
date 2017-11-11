# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']

#新增的PostAdmin在这里注册进来
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

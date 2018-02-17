# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User, Version, Context

# Register your models here.

admin.site.register(User)

class ContextInline(admin.StackedInline):
    model = Context
    exclude = ('status', 'handler')
    extra = 2

class VersionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['version', 'leader', 'remark']}),
    ]
    inlines = [ContextInline]

admin.site.register(Version, VersionAdmin)

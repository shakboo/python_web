# -*- coding: utf-8 -*-

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #指定表单需要显示的字段
        fields = ['name','email','url','text']
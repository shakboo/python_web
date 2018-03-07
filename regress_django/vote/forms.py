#coding=utf-8
from django.forms import ModelForm
from .models import Question

class QuestionForm(ModelForm):
	class Meta:
		model = Question
		exclude = ['author','already_votes']
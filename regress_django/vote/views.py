# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Question
from .forms import QuestionForm
from regress.models import User

# Create your views here.

def index(request):
	questionList = Question.objects.all().order_by('-created_time')
	username = str(request.user.username)

	voteList = []
	for question in questionList:
		if question.already_votes.find(username) == -1:
			voteList.append[0]
		else:
			voteList.append[1]
	voteDict = zip(questionList, voteList)

	if request.method == 'POST':
		pass
	else:
		form = QuestionForm()
		return render(request, 'vote/index.html', context={
				'questionList' : questionList,
				'form' : form,
			})

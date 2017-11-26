# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect,reverse
from .forms import RegisterForm,QuestionForm,ChoiceForm
from .models import Question

# Create your views here.

def index(request):
    question_list = Question.objects.all().order_by('-created_time')[:10]
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        #form_Choice = ChoiceForm(request.POST)
        if form.is_valid():    #and form_Choice.is_valid()
            qform = form.save(commit=False)
            qform.save()
            #cform = form_Choice.save(commit=False)
            #cform.question = qform
            #cform.save()

            #清除提交的表单内容
            return HttpResponseRedirect(reverse('index'))

    else:
        form = QuestionForm()
        #form_Choice = ChoiceForm()
    return render(request, 'index.html',context={
        'question_list' : question_list,
        'form' : form,
        #'form_Choice' : form_Choice
    })

def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        form = RegisterForm(request.POST)

        # 验证数据合法性
        if form.is_valid():
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')

    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'vote/register.html', context={'form': form, 'next' : redirect})

def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = QuestionForm()
    return render(request,'vote/detail.html',context={
        'question':question,
        'form' : form
    })




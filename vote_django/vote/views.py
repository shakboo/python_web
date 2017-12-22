# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect,reverse
from .forms import RegisterForm,QuestionForm,ChoiceForm
from .models import Question
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage


#主界面视图函数
def index(request):
    question_list = Question.objects.all().order_by('-created_time')[:10]
    username = str(request.user.username)


    al_vote_list = []
    for question in question_list:
        if question.already_votes.find(username) == -1:
            al_vote_list.append(0)
        else:
            al_vote_list.append(1)

    #该字典用来记录该问题下该用户的投票情况
    question_list = zip(question_list,al_vote_list)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # 需要获取用户Choice输入数目和内容，并添加到数据库
        Choice_list = request.POST.getlist("Choice_text",'')

        if form.is_valid():
            qform = form.save(commit=False)
            qform.save()
            for Choice in Choice_list:
                choiceForm = ChoiceForm()
                cform = choiceForm.save(commit=False)
                cform.choice_text = Choice
                cform.question = qform
                cform.save()

            #清除提交的表单内容
            return HttpResponseRedirect(reverse('index'))

    else:
        form = QuestionForm()
    return render(request, 'index.html',context={
        'question_list' : question_list,
        'form' : form,
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

#处理detail界面的发起投票
def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = QuestionForm()
    #处理投票结果

    #获得用户选择的choice的ID
    try:
        #加上这句是为了防止try被判定为true，应对无选项提交
        prevent_jump = question.choice_set.get(pk=request.POST['choice'])

        selected_choices = request.POST.getlist('choice')
    except:
        #当用户无任何选项提交时的处理
        return render(request, 'vote\detail.html',context={
            'question' : question,
            'form' : form,
        })

    #投票成功时的处理
    else:
        for selected_choice_id in selected_choices:
            selected_choice = question.choice_set.get(pk=selected_choice_id)
            if selected_choice.who_votes.find(str(request.user.username)) == -1:
                if question.choose == 'choose_vote':
                    selected_choice.votes += 1
                    selected_choice.question = question
                    #记录下选择此选项的用户
                    selected_choice.who_votes += str(request.user.username)
                    selected_choice.who_votes += "; "
                    selected_choice.save()
                elif question.choose == 'choose_qa':
                    selected_choice.choice_answer += request.POST[str(selected_choice_id)] + "  --" + str(request.user.username)
                    selected_choice.choice_answer += "\r\n"

                    selected_choice.who_votes += str(request.user.username)
                    selected_choice.who_votes += "; "
                    selected_choice.save()

            #记录下回答过该问题的用户
            if question.already_votes.find(str(request.user.username)) == -1:
                question.already_votes += str(request.user.username)
                question.already_votes += "; "
                question.save()


        return HttpResponseRedirect(reverse('index'))

def all(request):
    question_list = Question.objects.all().order_by('-created_time')
    username = str(request.user.username)
    form = QuestionForm()
    #分页
    paginator = Paginator(question_list,10,0)
    page = request.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)

    #返回该数据是为了用来方便记录页码
    cus_list_page = customer

    #同样确认该登录用户的投票状态
    al_vote_list = []
    for question in customer:
        if question.already_votes.find(username) == -1:
            al_vote_list.append(0)
        else:
            al_vote_list.append(1)
    customer = zip(customer, al_vote_list)

    return render(request, 'vote/all.html',context={
        'cus_list' : customer,
        'cus_list_page' : cus_list_page,
        'form' : form,
    })

#投票详情界面
def result(request,pk):
    question = get_object_or_404(Question, pk=pk)
    form = QuestionForm()
    return render(request, 'vote/result.html', context={
        'question' : question,
        'form' : form,
    })





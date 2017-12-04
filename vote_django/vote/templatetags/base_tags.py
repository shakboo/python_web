#coding=utf-8

from ..forms import QuestionForm, ChoiceForm
from django import template
from django.shortcuts import render,HttpResponseRedirect,reverse

register = template.Library()

@register.simple_tag
def base_recent_form(request):
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
        'form' : form,
    })
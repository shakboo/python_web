# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from .models import User, Version, Context
from .forms import RegisterForm
from django.contrib import messages
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.

def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'regress/register.html', context={
        'form' : form,
        'next' : redirect,
    })

def index(request):
    versionList = Version.objects.all().order_by('-version')
    paginator = Paginator(versionList,15,0)
    page = request.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request, 'index.html', context={
        'versionList' : versionList,
        'customer' : customer,
    })

def detail(request, version):
    versionList = Version.objects.all().order_by('-version')
    for i in range(len(versionList)):
        if unicode(versionList[i]) == version:
            contextList = Context.objects.filter(version=versionList[i])
            versionNow = versionList[i]
            break
    return render(request, 'regress/detail.html', context={
        'contextList' : contextList,
        'versionNow' : versionNow,
    })

def pot(request, pk):
    context = get_object_or_404(Context, pk=pk)
    if context.handler == '':
        msg_text = '认领成功!'
        context.status = True
        context.handler = str(request.user.nickname)
        context.save()
    else:
        msg_text = '已经有人认领了!'
    messages.add_message(request, messages.INFO, msg_text)
    return HttpResponseRedirect(reverse("regress:detail",kwargs={'version':context.version}))

def popo(request, pk):
    from popo import sendMsg
    version = get_object_or_404(Version, pk=pk)
    version = version.version
    from datetime import datetime
    version = version.strftime('%Y-%m-%d')
    url = "http://10.240.108.40/regress/detail/" + version  #先用localhost代替
    message =  '请各位前往'+url+"查看"+version+"版本的回归内容。"
    sendMsg('wb.zhouxiebo@mesg.corp.netease.com',message)
    return HttpResponseRedirect(reverse("index"))
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from .models import User, Version, Context
from .forms import RegisterForm
from django.contrib import messages

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
    return render(request, 'index.html', context={
        'versionList' : versionList,
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
    context.status = True
    msg_text = '认领成功!' if context.handler == '' else '已经有人认领啦!'
    context.handler = str(request.user.nickname) if context.handler == '' else context.handler
    messages.add_message(request, messages.INFO, msg_text) 
    context.save()
    return HttpResponseRedirect(reverse("regress:detail",kwargs={'version':context.version}))

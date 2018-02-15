# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from .models import User, Version, Context
from .forms import RegisterForm

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
    if request.method == 'POST':
        version = request.POST.get('version')
        for i in range(len(versionList)):
            if unicode(versionList[i]) == version:
                contextList = Context.objects.filter(version=versionList[i])
                versionNow = versionList[i]
                break
    else:
        versionNow = versionList[0] if versionList else None
        contextList = Context.objects.filter(version=versionNow)

    return render(request, 'index.html',context={
        'versionList' : versionList,
        'contextList' : contextList,
        'versionNow' : versionNow,
    })

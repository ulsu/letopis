# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from forms import *
from django.http import HttpResponseRedirect
from django.shortcuts import render

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
            go_next = request.GET['next'] if 'next' in request.GET else '/'
            return HttpResponseRedirect(request.GET['next'])
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'next': request.GET['next'] if 'next' in request.GET else '/',
        })

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/')
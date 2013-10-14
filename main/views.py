# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.contrib.auth.models import User
from django.http import HttpResponse
from models import *
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    tasks = Task.objects.filter(parent=None)
    t = loader.get_template("index.html")
    c = RequestContext(request, {'tasks': tasks})
    return HttpResponse(t.render(c))
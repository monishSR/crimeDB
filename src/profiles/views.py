# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

from django.urls import reverse

# Create your views here.
def home(request):
    context = {}
    template = 'home.html'

    return render(request, template, context)


@login_required
def userProfile(request):
    user = request.user
    context = {'user': user}
    template = 'profile.html'
    return render(request, template, context)

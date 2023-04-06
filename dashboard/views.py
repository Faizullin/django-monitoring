# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import *
import time, psutil
from dashboard_api.views import getStatData

@login_required()
def index(request):
    context = {'segment': 'dashboard:index'}
    html_template = loader.get_template('dashboard/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
def profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {'segment': 'dashboard:profile', 'user': user }
    html_template = loader.get_template('dashboard/profile.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
def servers(request, server):
    context = {
        'segment': server,
        'data': { },
        'servers': ['server0','server1']
    }
    context = getStatData(context)
    return render(request, f'dashboard/servers/{server}-stats.html', context)

@login_required()
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('dashboard/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('dashboard/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('dashboard/page-500.html')
        return HttpResponse(html_template.render(context, request))



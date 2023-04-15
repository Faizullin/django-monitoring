from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import *
import time, psutil
from dashboard_api.views import getStatData
from .context_processors import default_context

@login_required()
def index(request):
    context = default_context()
    context.update({'segment': 'dashboard:index'})
    html_template = loader.get_template('dashboard/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
def profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = default_context()
    context.update({'segment': 'dashboard:profile', 'user': user })
    html_template = loader.get_template('dashboard/profile.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
def servers(request, server):
    context = default_context()
    if not server in context['servers']:
        raise Http404
    context.update({
        'segment': server,
        'server_stats_api_domain': context['servers'][server],
    })
    context.update(getStatData())
    return render(request, f'dashboard/servers/server-stats.html', context)

@login_required()
def pages(request):
    context = {}
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



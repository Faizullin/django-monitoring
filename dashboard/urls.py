# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from dashboard import views
 

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('user',include('dashboard.tables.user.urls')),
    path('servers/<str:server>', views.servers, name='servers'),
]


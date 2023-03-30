
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from . import views
 

app_name = 'dashboard_api'

urlpatterns = [
    path('monitoring/', views.ApiServerData.as_view(), name='api-monitoring'),
    path('monitoring/start_record/', views.apiStartRecord, name='api-monitoring-start-record'),
]
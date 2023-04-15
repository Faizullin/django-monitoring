from django.urls import path
from . import views

app_name = 'storage_drive'

urlpatterns = [
    path('add/', views.file_create, name='add'),
    path('remove/', views.file_delete, name='remove'),
    path('list/', views.FileListView.as_view(), name='list'),
    path('<int:pk>/download/', views.FileDownloadView.as_view(), name='download'),
]
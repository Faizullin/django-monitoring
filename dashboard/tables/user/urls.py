from django.urls import path
from . import views

urlpatterns = [
    path('',views.UserListView.as_view(), name='user_index'),
    path('create', views.user_create, name='user_create'),
    path('update/<int:pk>', views.user_edit, name='user_edit'),
    path('delete/<int:pk>', views.user_delete, name='user_delete'),
]
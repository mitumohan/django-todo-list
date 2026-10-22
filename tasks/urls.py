from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='list'),
    path('add/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='edit'),
    path('<int:pk>/toggle/', views.task_toggle, name='toggle'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
]

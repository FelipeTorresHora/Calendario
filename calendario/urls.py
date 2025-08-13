from django.urls import path
from . import views

urlpatterns = [
    # Rotas de Autenticação
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register_new_user, name='register'),
    
    # Rotas de Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Rotas de Tarefas
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/day/<str:date>/', views.get_day_tasks, name='get_day_tasks'),

    # Rotas de Lembretes
    path('reminders/create/', views.reminder_create, name='reminder_create'),
    path('reminders/<int:pk>/update/', views.reminder_update, name='reminder_update'),
    path('reminders/<int:pk>/delete/', views.reminder_delete, name='reminder_delete'),

    # Dashboard de métricas
    path('metrics/', views.dashboard_metrics, name='dashboard_metrics'),
    
    # URLs dos Desafios
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenges/create/', views.challenge_create, name='challenge_create'),
    path('challenges/<int:pk>/edit/', views.challenge_edit, name='challenge_edit'),
    
    # URLs para API de Tarefas (mantidas do código anterior)
    path('tasks/day/<str:date>/', views.get_day_tasks, name='get_day_tasks'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
]
from django.urls import path
from . import views

urlpatterns = [
    # Rotas de Autenticação
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register_new_user, name='register'),
    
    # Rotas de Dashboard e Páginas Principais
    path('', views.dashboard, name='home'),  # Dashboard agora é a página principal
    path('dashboard/', views.dashboard, name='dashboard'),  # Mantém compatibilidade
    path('calendario/', views.calendar_view, name='calendar_view'),  # Nova visualização expandida do calendário

    # Rotas de Tarefas
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/day/<str:date>/', views.get_day_tasks, name='get_day_tasks'),

    # Rotas de Lembretes
    path('reminders/create/', views.reminder_create, name='reminder_create'),
    path('reminders/<int:pk>/update/', views.reminder_update, name='reminder_update'),
    path('reminders/<int:pk>/delete/', views.reminder_delete, name='reminder_delete'),

    # Cave Mode metrics
    path('cave-metrics/', views.cave_metrics, name='cave_metrics'),
    
    # URLs dos Objetivos (Cave Mode)
    path('objectives/', views.objective_list, name='objective_list'),
    path('objectives/create/', views.objective_create, name='objective_create'),
    path('objectives/<int:pk>/edit/', views.objective_edit, name='objective_edit'),
    path('objectives/<int:pk>/toggle/', views.objective_toggle, name='objective_toggle'),
    path('objectives/<int:pk>/delete/', views.objective_delete, name='objective_delete'),
    
    # URLs para API de Tarefas (mantidas do código anterior)
    path('tasks/day/<str:date>/', views.get_day_tasks, name='get_day_tasks'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    
    # API endpoint para estatísticas do dashboard
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
]
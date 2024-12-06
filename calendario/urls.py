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

    # Rotas de Lembretes
    path('reminders/create/', views.reminder_create, name='reminder_create'),
    path('reminders/<int:pk>/update/', views.reminder_update, name='reminder_update'),
    path('reminders/<int:pk>/delete/', views.reminder_delete, name='reminder_delete'),
]

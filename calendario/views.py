from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
import json
from .models import Task, Reminder, Objective
from .forms import TaskForm, ReminderForm, CustomUserCreationForm, ObjectiveForm, QuickTaskForm
from .cache_utils import CacheManager
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods

def invalidate_user_cache(user_id):
    """Invalidate all cache entries for a specific user"""
    CacheManager.invalidate_user_cache(user_id)

def home(request):
    # Home agora redireciona para dashboard que é a página principal
    return redirect('dashboard')

def register_new_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Erro ao registrar. Verifique os dados")
    else:
        form = CustomUserCreationForm()
    return render(request, 'calendario/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Email ou senha inválidos")
    return render(request, 'calendario/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    """Cave Mode Dashboard - focused on objectives and personal tracking"""
    from datetime import date, timedelta
    from collections import defaultdict
    
    # Buscar objetivos ativos
    objectives = Objective.objects.filter(user=request.user, is_active=True).order_by('created_at')
    
    # Calcular estatísticas
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_done=True).count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Contar tarefas por tipo
    objective_tasks_count = Task.objects.filter(user=request.user, objective__isnull=False).count()
    additional_tasks_count = Task.objects.filter(user=request.user, objective__isnull=True).count()
    
    # Calcular melhor sequência (streak)
    best_streak = 0
    if objectives.exists():
        best_streak = max([obj.get_streak_count() for obj in objectives])
    
    # Gerar dados do heatmap (últimos 12 meses = 365 dias)
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    
    # Dados gerais do heatmap (todas as tarefas concluídas)
    heatmap_data = defaultdict(int)
    completed_tasks_query = Task.objects.filter(
        user=request.user,
        is_done=True,
        date__gte=start_date,
        date__lte=end_date
    )
    
    for task in completed_tasks_query:
        date_str = task.date.strftime('%Y-%m-%d')
        heatmap_data[date_str] += 1
    
    # Dados do heatmap por objetivo
    objectives_heatmap_data = {}
    for objective in objectives:
        obj_data = defaultdict(int)
        obj_tasks = completed_tasks_query.filter(objective=objective)
        
        for task in obj_tasks:
            date_str = task.date.strftime('%Y-%m-%d')
            obj_data[date_str] += 1
        
        objectives_heatmap_data[str(objective.id)] = dict(obj_data)
    
    context = {
        'objectives': objectives,
        'objectives_count': objectives.count(),
        'completion_rate': round(completion_rate, 1),
        'objective_tasks_count': objective_tasks_count,
        'additional_tasks_count': additional_tasks_count,
        'best_streak': best_streak,
        'heatmap_data': json.dumps(dict(heatmap_data)),
        'objectives_heatmap_data': json.dumps(objectives_heatmap_data),
    }
    
    return render(request, 'calendario/cave_dashboard.html', context)


@login_required
def calendar_view(request):
    """Expanded calendar view for comprehensive task visualization"""
    # Get all user tasks for the current month and surrounding months
    from datetime import date, timedelta
    import json
    
    # Get tasks for a wider date range (3 months around current month)
    today = date.today()
    start_date = date(today.year, today.month, 1) - timedelta(days=90)
    end_date = date(today.year, today.month, 1) + timedelta(days=120)
    
    tasks = Task.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).select_related('objective').order_by('date', 'is_done')
    
    # Get reminders
    reminders = Reminder.objects.filter(user=request.user).order_by('date')
    
    # Serialize tasks for JavaScript
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'description': task.description,
            'date': task.date.strftime('%Y-%m-%d'),
            'is_done': task.is_done,
            'objective_title': task.objective.title if task.objective else None,
            'is_objective_task': task.is_objective_task
        })
    
    context = {
        'tasks': tasks,
        'reminders': reminders,
        'tasks_json': json.dumps(tasks_data),
    }
    
    return render(request, 'calendario/calendar_expanded.html', context)


@login_required
def task_create(request):
    """Create task with Cave Mode objective linking"""
    if request.method == 'POST':
        form = QuickTaskForm(request.POST, user=request.user)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            
            # Set task type flag
            task.is_objective_task = bool(task.objective)
            task.save()
            
            messages.success(request, 'Tarefa criada com sucesso!')
            invalidate_user_cache(request.user.id)
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = QuickTaskForm(user=request.user)

    return render(request, 'calendario/task_form.html', {'form': form})

@login_required
def get_day_tasks(request, date):
    """Get tasks for a specific date with objective information and daily objectives"""
    from datetime import datetime
    
    # Get regular tasks for the date
    tasks = Task.objects.filter(
        user=request.user,
        date=date
    ).select_related('objective').order_by('is_done', '-id')
    
    # Get active objectives
    objectives = Objective.objects.filter(
        user=request.user, 
        is_active=True
    ).order_by('created_at')
    
    tasks_data = []
    
    # Add regular tasks
    for task in tasks:
        task_data = {
            'id': task.id,
            'type': 'task',
            'description': task.description,
            'date': task.date.strftime('%Y-%m-%d'),
            'is_done': task.is_done,
            'objective_id': task.objective.id if task.objective else None,
            'objective_title': task.objective.title if task.objective else None,
            'is_objective_task': task.is_objective_task
        }
        tasks_data.append(task_data)
    
    # Add daily objectives as checkable items
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    for objective in objectives:
        # Check if there's already a task for this objective today
        existing_task = tasks.filter(objective=objective).first()
        
        if not existing_task:
            # Create a virtual daily objective entry
            objective_data = {
                'id': f'objective-{objective.id}',
                'type': 'daily_objective',
                'description': f'{objective.title}',
                'date': date,
                'is_done': False,
                'objective_id': objective.id,
                'objective_title': objective.title,
                'is_objective_task': True,
                'is_daily_check': True
            }
            tasks_data.append(objective_data)
        else:
            # Mark existing task as daily objective
            for task_data in tasks_data:
                if task_data['id'] == existing_task.id:
                    task_data['is_daily_check'] = True
                    break
    
    # Sort: daily objectives first, then regular tasks
    tasks_data.sort(key=lambda x: (x.get('type') != 'daily_objective', x.get('is_done', False)))
    
    return JsonResponse({
        'tasks': tasks_data
    })

@login_required
@require_http_methods(['POST'])
def complete_task(request, task_id):
    """Toggle task completion status"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = not task.is_done  # Toggle instead of just marking as done
    task.save()
    
    # Invalidate cache after completing task
    invalidate_user_cache(request.user.id)
    
    return JsonResponse({
        'success': True,
        'is_done': task.is_done
    })

@login_required
def dashboard_stats(request):
    """API endpoint to get updated dashboard statistics"""
    from datetime import date, timedelta
    from collections import defaultdict
    
    # Buscar objetivos ativos
    objectives = Objective.objects.filter(user=request.user, is_active=True)
    
    # Calcular estatísticas
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_done=True).count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Contar tarefas por tipo
    additional_tasks_count = Task.objects.filter(user=request.user, objective__isnull=True).count()
    
    # Calcular melhor sequência (streak)
    best_streak = 0
    if objectives.exists():
        best_streak = max([obj.get_streak_count() for obj in objectives])
    
    # Gerar dados do heatmap atualizados
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    
    heatmap_data = defaultdict(int)
    completed_tasks_query = Task.objects.filter(
        user=request.user,
        is_done=True,
        date__gte=start_date,
        date__lte=end_date
    )
    
    for task in completed_tasks_query:
        date_str = task.date.strftime('%Y-%m-%d')
        heatmap_data[date_str] += 1
    
    return JsonResponse({
        'success': True,
        'completion_rate': round(completion_rate, 1),
        'additional_tasks_count': additional_tasks_count,
        'best_streak': best_streak,
        'heatmap_data': dict(heatmap_data),
    })

@login_required
def task_update(request, pk):
    """Update task with Cave Mode objective linking"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.is_objective_task = bool(task.objective)
            task.save()
            # Invalidate cache after updating task
            invalidate_user_cache(request.user.id)
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'calendario/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    # Invalidate cache after deleting task
    invalidate_user_cache(request.user.id)
    messages.success(request, 'Tarefa excluída com sucesso!')
    return redirect('dashboard')

@login_required
def reminder_create(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, 'Lembrete criado com sucesso!')
            return redirect('dashboard')
    else:
        form = ReminderForm()
    return render(request, 'calendario/reminder_form.html', {'form': form})

@login_required
def reminder_update(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lembrete atualizado com sucesso!')
            return redirect('dashboard')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'calendario/reminder_form.html', {'form': form})

@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.delete()
    messages.success(request, 'Lembrete excluído com sucesso!')
    return redirect('dashboard')

@login_required
def cave_metrics(request):
    """Cave Mode metrics with heatmap visualization"""
    # Cache key specific to user
    cache_key = f'cave_metrics_{request.user.id}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        # Obter objetivos do usuário
        objectives = Objective.objects.filter(user=request.user, is_active=True)
        
        # Calcular métricas para tarefas
        total_tasks = Task.objects.filter(user=request.user).count()
        completed_tasks = Task.objects.filter(user=request.user, is_done=True).count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Métricas de objetivos
        objective_tasks = Task.objects.filter(user=request.user, objective__isnull=False)
        additional_tasks = Task.objects.filter(user=request.user, objective__isnull=True)
        
        # Métricas por período (últimos 365 dias para heatmap)
        year_ago = datetime.now().date() - timedelta(days=365)
        tasks_last_year = Task.objects.filter(
            user=request.user,
            date__gte=year_ago
        )
        
        # Dados para heatmap (estilo GitHub)
        heatmap_data = {}
        current_date = year_ago
        end_date = datetime.now().date()
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            day_tasks = tasks_last_year.filter(date=current_date)
            completed_count = day_tasks.filter(is_done=True).count()
            heatmap_data[date_str] = completed_count
            current_date += timedelta(days=1)
        
        # Métricas de streak para cada objetivo
        objective_streaks = []
        for obj in objectives:
            streak = obj.get_streak_count()
            objective_streaks.append({
                'title': obj.title,
                'streak': streak,
                'heatmap_data': obj.get_completion_data_last_year()
            })

        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': round(completion_rate, 2),
            'objectives_count': objectives.count(),
            'objective_tasks_count': objective_tasks.count(),
            'additional_tasks_count': additional_tasks.count(),
            'heatmap_data': json.dumps(heatmap_data),
            'objective_streaks': objective_streaks,
            'objectives': objectives
        }
        
        # Cache for 10 minutes
        cache.set(cache_key, context, 600)
    
    return render(request, 'calendario/cave_metrics.html', context)

@login_required
def objective_list(request):
    """Enhanced objectives and task management page"""
    from datetime import date, timedelta
    import json
    
    # Get objectives
    active_objectives = Objective.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('created_at')
    
    inactive_objectives = Objective.objects.filter(
        user=request.user,
        is_active=False
    ).order_by('-created_at')
    
    # Get recent tasks (last 30 days) for task management
    today = date.today()
    start_date = today - timedelta(days=30)
    
    recent_tasks = Task.objects.filter(
        user=request.user,
        date__gte=start_date
    ).select_related('objective').order_by('-date', 'is_done')
    
    # Get pending tasks (future + today's incomplete)
    pending_tasks = Task.objects.filter(
        user=request.user,
        date__gte=today,
        is_done=False
    ).select_related('objective').order_by('date')
    
    # Task statistics
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_done=True).count()
    
    # Tasks by objective statistics
    objective_task_stats = []
    for objective in active_objectives:
        obj_total = Task.objects.filter(user=request.user, objective=objective).count()
        obj_completed = Task.objects.filter(user=request.user, objective=objective, is_done=True).count()
        obj_pending = Task.objects.filter(user=request.user, objective=objective, is_done=False, date__gte=today).count()
        
        objective_task_stats.append({
            'objective': objective,
            'total_tasks': obj_total,
            'completed_tasks': obj_completed,
            'pending_tasks': obj_pending,
            'completion_rate': (obj_completed / obj_total * 100) if obj_total > 0 else 0
        })
    
    context = {
        'active_objectives': active_objectives,
        'inactive_objectives': inactive_objectives,
        'recent_tasks': recent_tasks,
        'pending_tasks': pending_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'objective_task_stats': objective_task_stats,
    }
    return render(request, 'calendario/objective_list.html', context)

@login_required
def objective_create(request):
    """Create new Cave Mode objective"""
    if request.method == 'POST':
        form = ObjectiveForm(request.POST)
        
        if form.is_valid():
            objective = form.save(commit=False)
            objective.user = request.user
            objective.save()
            
            messages.success(request, 'Objetivo criado com sucesso!')
            return redirect('objective_list')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ObjectiveForm()
    
    return render(request, 'calendario/objective_form.html', {
        'form': form,
        'is_edit': False
    })

@login_required
def objective_edit(request, pk):
    """Edit Cave Mode objective"""
    objective = get_object_or_404(Objective, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ObjectiveForm(request.POST, instance=objective)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Objetivo atualizado com sucesso!')
            return redirect('objective_list')
    else:
        form = ObjectiveForm(instance=objective)
    
    return render(request, 'calendario/objective_form.html', {
        'form': form,
        'is_edit': True,
        'objective': objective
    })

@login_required
def objective_toggle(request, pk):
    """Toggle objective active/inactive status"""
    objective = get_object_or_404(Objective, pk=pk, user=request.user)
    objective.is_active = not objective.is_active
    objective.save()
    
    status = "ativado" if objective.is_active else "desativado"
    messages.success(request, f'Objetivo {status} com sucesso!')
    return redirect('objective_list')

@login_required
def objective_delete(request, pk):
    """Delete Cave Mode objective"""
    objective = get_object_or_404(Objective, pk=pk, user=request.user)
    objective.delete()
    messages.success(request, 'Objetivo excluído com sucesso!')
    return redirect('objective_list')

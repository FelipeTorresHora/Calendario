from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Task, Reminder, Challenge, ChallengeTask
from .forms import TaskForm, ReminderForm, CustomUserCreationForm, ChallengeForm, ChallengeTaskForm, ChallengeTaskFormSet
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods


def home(request):
    if request.method == 'GET':
        return redirect('dashboard')
    return render(request, 'calendario/home.html')

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
    # Buscar apenas os lembretes para exibir na lateral
    reminders = Reminder.objects.filter(user=request.user).order_by('date')
    
    # Buscar todas as tarefas para o calendário
    tasks = Task.objects.filter(user=request.user).order_by('date')
    
    # Preparar dados das tarefas para o calendário
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'description': task.description,
            'date': task.date.strftime('%Y-%m-%d'),
            'is_done': task.is_done
        })
    
    context = {
        'tasks': tasks,
        'reminders': reminders,
        'tasks_json': json.dumps(tasks_data, cls=DjangoJSONEncoder)
    }
    
    return render(request, 'calendario/dashboard.html', context)

@login_required
def get_day_tasks(request, date):
    tasks = Task.objects.filter(
        user=request.user,
        date=date
    ).order_by('is_done', 'date')
    
    return JsonResponse({
        'tasks': list(tasks.values())
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        date_str = request.POST.get('date')  # Data única para tarefa sem recorrência
        recurrence_type = request.POST.get('recurrence_type', 'none')
        
        try:
            # Processar data inicial
            if recurrence_type == 'none':
                if not date_str:
                    messages.error(request, 'Data é obrigatória')
                    return redirect('dashboard')
                start_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                start_date_str = request.POST.get('start_date')
                if not start_date_str:
                    messages.error(request, 'Data de início é obrigatória')
                    return redirect('dashboard')
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

            # Processar data final (opcional)
            end_date = None
            end_date_str = request.POST.get('end_date')
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Processar dias da semana para recorrência semanal
            weekdays = request.POST.getlist('weekdays')

            if recurrence_type == 'none':
                # Criar uma única tarefa
                Task.objects.create(
                    user=request.user,
                    description=description,
                    date=start_date,
                )
            else:
                # Criar tarefas recorrentes
                current_date = start_date
                while current_date <= (end_date or start_date):
                    create_task = False

                    if recurrence_type == 'daily':
                        create_task = True
                    elif recurrence_type == 'weekly':
                        create_task = str(current_date.weekday()) in weekdays
                    elif recurrence_type == 'monthly':
                        create_task = True

                    if create_task:
                        Task.objects.create(
                            user=request.user,
                            description=description,
                            date=current_date,
                        )

                    if recurrence_type == 'monthly':
                        # Avançar para o mesmo dia do próximo mês
                        if current_date.month == 12:
                            current_date = current_date.replace(year=current_date.year + 1, month=1)
                        else:
                            current_date = current_date.replace(month=current_date.month + 1)
                    else:
                        current_date += timedelta(days=1)

            messages.success(request, 'Tarefa(s) criada(s) com sucesso!')
            return redirect('dashboard')

        except ValueError as e:
            messages.error(request, f'Erro ao processar as datas: {str(e)}')
            return redirect('dashboard')

    return render(request, 'calendario/task_form.html', {'form': TaskForm()})

@login_required
def get_day_tasks(request, date):
    tasks = Task.objects.filter(
        user=request.user,
        date=date
    ).order_by('is_done', '-id')
    
    return JsonResponse({
        'tasks': list(tasks.values())
    })

@login_required
@require_http_methods(['POST'])
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = True
    task.save()
    
    return JsonResponse({
        'success': True
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'calendario/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
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
def dashboard_metrics(request):
    # Obter todos os desafios do usuário
    challenges = Challenge.objects.filter(user=request.user)
    
    # Calcular métricas para tarefas
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_done=True).count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Métricas de desafios
    active_challenges = challenges.filter(status='active').count()
    completed_challenges = challenges.filter(status='completed').count()
    
    # Métricas por período (últimos 30 dias)
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    tasks_last_30_days = Task.objects.filter(
        user=request.user,
        date__gte=thirty_days_ago
    )
    
    # Agrupamento de conclusão por dia
    completion_by_day = {}
    for task in tasks_last_30_days:
        day = task.date.strftime('%Y-%m-%d')
        if day not in completion_by_day:
            completion_by_day[day] = {'total': 0, 'completed': 0}
        completion_by_day[day]['total'] += 1
        if task.is_done:
            completion_by_day[day]['completed'] += 1
    
    # Métricas de desafios ativos
    active_challenges_data = []
    for challenge in challenges.filter(status='active'):
        active_challenges_data.append({
            'title': challenge.title,
            'completion_rate': challenge.get_completion_rate(),
            'days_remaining': (challenge.end_date - datetime.now().date()).days
        })

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': round(completion_rate, 2),
        'active_challenges': active_challenges,
        'completed_challenges': completed_challenges,
        'completion_by_day': json.dumps(completion_by_day),
        'active_challenges_data': active_challenges_data
    }
    
    return render(request, 'calendario/dashboard_metrics.html', context)

@login_required
def challenge_list(request):
    active_challenges = Challenge.objects.filter(
        user=request.user,
        status='active'
    ).order_by('start_date')
    
    completed_challenges = Challenge.objects.filter(
        user=request.user,
        status='completed'
    ).order_by('-end_date')
    
    context = {
        'active_challenges': active_challenges,
        'completed_challenges': completed_challenges
    }
    return render(request, 'calendario/challenge_list.html', context)

@login_required
def challenge_create(request):
    if request.method == 'POST':
        challenge_form = ChallengeForm(request.POST)
        task_formset = ChallengeTaskFormSet(request.POST, prefix='tasks', queryset=ChallengeTask.objects.none())
        
        if challenge_form.is_valid() and task_formset.is_valid():
            challenge = challenge_form.save(commit=False)
            challenge.user = request.user
            challenge.save()
            
            # Salvar as tarefas do desafio
            tasks = task_formset.save(commit=False)
            for task in tasks:
                task.challenge = challenge
                task.save()
            
            # Criar tarefas diárias para todo o período do desafio
            current_date = challenge.start_date
            while current_date <= challenge.end_date:
                for challenge_task in challenge.challenge_tasks.all():
                    Task.objects.create(
                        user=request.user,
                        description=challenge_task.description,
                        date=current_date,
                        challenge_task=challenge_task
                    )
                current_date += timedelta(days=1)
            
            messages.success(request, 'Desafio criado com sucesso!')
            return redirect('challenge_list')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        challenge_form = ChallengeForm()
        task_formset = ChallengeTaskFormSet(prefix='tasks', queryset=ChallengeTask.objects.none())
    
    return render(request, 'calendario/challenge_form.html', {
        'form': challenge_form,
        'task_formset': task_formset,
        'is_edit': False
    })

@login_required
def challenge_edit(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, user=request.user)
    
    if challenge.status != 'active':
        messages.error(request, 'Não é possível editar um desafio já iniciado.')
        return redirect('challenge_list')
    
    if request.method == 'POST':
        challenge_form = ChallengeForm(request.POST, instance=challenge)
        task_formset = ChallengeTaskFormSet(
            request.POST,
            prefix='tasks',
            queryset=challenge.challenge_tasks.all()
        )
        
        if challenge_form.is_valid() and task_formset.is_valid():
            challenge_form.save()
            tasks = task_formset.save(commit=False)
            
            # Lidar com exclusões
            for obj in task_formset.deleted_objects:
                obj.delete()
            
            # Salvar tarefas novas/modificadas
            for task in tasks:
                task.challenge = challenge
                task.save()
            
            messages.success(request, 'Desafio atualizado com sucesso!')
            return redirect('challenge_list')
    else:
        challenge_form = ChallengeForm(instance=challenge)
        task_formset = ChallengeTaskFormSet(
            prefix='tasks',
            queryset=challenge.challenge_tasks.all()
        )
    
    return render(request, 'calendario/challenge_form.html', {
        'form': challenge_form,
        'task_formset': task_formset,
        'is_edit': True
    })

@login_required
def challenge_delete(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, user=request.user)
    challenge.delete()
    messages.success(request, 'Desafio excluído com sucesso!')
    return redirect('challenge_list')

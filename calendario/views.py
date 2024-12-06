from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Task, Reminder
from .forms import TaskForm, ReminderForm, CustomUserCreationForm
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date


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

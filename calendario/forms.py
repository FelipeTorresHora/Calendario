from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task, Reminder, Objective

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'date', 'is_done', 'objective']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['objective'].queryset = Objective.objects.filter(user=user, is_active=True)
        self.fields['objective'].required = False
        self.fields['objective'].empty_label = "Tarefa adicional (não vinculada a objetivo)"

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'content', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'title': forms.TextInput(attrs={'placeholder': 'Título do lembrete'}),
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Conteúdo do lembrete'}),
        }

class ObjectiveForm(forms.ModelForm):
    """Form for creating and editing Cave Mode objectives"""
    class Meta:
        model = Objective
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome do objetivo (ex: Exercitar-se diariamente)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Descreva seu objetivo em detalhes (opcional)'
            }),
        }
        
class QuickTaskForm(forms.ModelForm):
    """Simplified form for quick task addition in Cave Mode"""
    class Meta:
        model = Task
        fields = ['description', 'date', 'objective']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={
                'placeholder': 'Descreva sua tarefa...',
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['objective'].queryset = Objective.objects.filter(user=user, is_active=True)
        self.fields['objective'].required = False
        self.fields['objective'].empty_label = "Tarefa adicional"
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task, Reminder, Challenge, ChallengeTask

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'date', 'is_done']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'content', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# forms.py

from django import forms
from django.forms import modelformset_factory
from .models import Challenge, ChallengeTask

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ChallengeTaskForm(forms.ModelForm):
    class Meta:
        model = ChallengeTask
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da tarefa'})
        }

# Definindo o formset após as classes de formulário
ChallengeTaskFormSet = modelformset_factory(
    ChallengeTask,
    form=ChallengeTaskForm,
    extra=1,
    can_delete=True,
    fields=('description',)
)
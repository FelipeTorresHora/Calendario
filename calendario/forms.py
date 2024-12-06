from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task, Reminder

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

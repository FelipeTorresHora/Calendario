from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Task(models.Model):
    RECURRENCE_CHOICES = [
        ('none', 'Sem recorrência'),
        ('daily', 'Diariamente'),
        ('weekly', 'Semanalmente'),
        ('monthly', 'Mensalmente'),
    ]

    WEEKDAYS = [
        (0, 'Segunda'),
        (1, 'Terça'),
        (2, 'Quarta'),
        (3, 'Quinta'),
        (4, 'Sexta'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    date = models.DateField()
    is_done = models.BooleanField(default=False)
    recurrence_type = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='none')
    recurrence_end_date = models.DateField(null=True, blank=True)
    recurrence_days = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.description
    
class Reminder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

class Challenge(models.Model):
    STATUS_CHOICES = [
        ('active', 'Em Andamento'),
        ('completed', 'Concluído'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_completion_rate(self):
        total_tasks = self.challenge_tasks.count() * self.get_total_days()
        completed_tasks = Task.objects.filter(
            challenge_task__challenge=self,
            is_done=True
        ).count()
        
        return (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    def get_total_days(self):
        return (self.end_date - self.start_date).days + 1

class ChallengeTask(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='challenge_tasks')
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.challenge.title} - {self.description}"
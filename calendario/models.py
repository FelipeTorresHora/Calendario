from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

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

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Task(models.Model):
    """Tasks can be linked to objectives (cave mode) or standalone (additional tasks)"""
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
    
    # Cave Mode: Link to objective or standalone additional task
    objective = models.ForeignKey('Objective', on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    is_objective_task = models.BooleanField(default=False, help_text='True if this is a daily cave mode objective task')

    def __str__(self):
        if self.objective:
            return f"{self.objective.title}: {self.description}"
        return self.description
        
    @property
    def task_type(self):
        """Return whether this is an objective task or additional task"""
        return "objective" if self.objective else "additional"
    
class Reminder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

class Objective(models.Model):
    """Cave Mode objectives - long-term goals to track daily"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='objectives')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
        
    def get_streak_count(self):
        """Calculate current streak of consecutive days with completed tasks"""
        from datetime import date, timedelta
        current_date = date.today()
        streak = 0
        
        while True:
            daily_tasks = Task.objects.filter(
                user=self.user,
                date=current_date,
                objective=self,
                is_done=True
            )
            
            if daily_tasks.exists():
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
                
        return streak
        
    def get_completion_data_last_year(self):
        """Get completion data for GitHub-style heatmap"""
        from datetime import date, timedelta
        from collections import defaultdict
        
        end_date = date.today()
        start_date = end_date - timedelta(days=365)
        
        completion_data = defaultdict(int)
        
        tasks = Task.objects.filter(
            user=self.user,
            objective=self,
            date__gte=start_date,
            date__lte=end_date,
            is_done=True
        )
        
        for task in tasks:
            date_str = task.date.strftime('%Y-%m-%d')
            completion_data[date_str] += 1
            
        return dict(completion_data)
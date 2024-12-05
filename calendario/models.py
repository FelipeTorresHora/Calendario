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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    date = models.DateField()
    description = models.TextField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.description
    
class Reminder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

#only real change was adding foreign key to the todo table
# Create your models here.

class AppUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    due_date = models.DateField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='todos')

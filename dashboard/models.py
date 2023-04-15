from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True,blank=True)
    address = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField("email", unique=True, blank=True)
    used_space = models.FloatField('used space', null=False, default=0)

class SystemData(models.Model):
    cpu_temp = models.FloatField()
    cpu_percent = models.FloatField()
    mem_percent = models.FloatField()
    disk_percent = models.FloatField()
    timestamp = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CPU: {self.cpu_percent}%, Memory: {self.mem_percent}%, Disk: {self.disk_percent}%, Timestamp: {self.timestamp}"
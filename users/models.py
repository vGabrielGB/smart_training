from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_client = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {'Gerente' if self.is_manager else 'Cliente'}"
# Create your models here.

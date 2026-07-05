from django.db import models
from django.conf import settings

class Plan(models.fields.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente de Verificación'),
        ('active', 'Solvente (Activa)'),
        ('expired', 'Moroso (Vencida)'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Datos del pago móvil para que el gerente verifique
    payment_reference = models.CharField(max_length=50)
    payment_date = models.DateField(auto_now_add=True)
    bank_origin = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.get_status_display()}"
# Create your models here.

from django.db import models
from django.conf import settings
from datetime import timedelta

class Plan(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Plan")
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Plan")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio ($)")
    duracion_dias = models.PositiveIntegerField(default=30, verbose_name="Duración en Días", help_text="Ejemplo: 30 para un mes estándar.")

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Suscripcion(models.Model):
    ESTADOS_CHOICES = (
        ('pendiente', 'Pendiente de Verificación'),
        ('activa', 'Solvente (Activa)'),
        ('vencida', 'Moroso (Vencida)'),
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='suscripciones', 
        verbose_name="Cliente"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name="Plan Contratado")
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    estado = models.CharField(max_length=15, choices=ESTADOS_CHOICES, default='pendiente', verbose_name="Estado de Suscripción")
    
    # Registro de Pago Móvil
    referencia = models.CharField(max_length=50, verbose_name="Número de Referencia")
    banco_origen = models.CharField(max_length=50, verbose_name="Banco de Origen", help_text="Banco desde donde el cliente realizó el pago.")
    captura_pago = models.ImageField(upload_to='capturas_planes/', verbose_name="Captura de Pantalla (Comprobante)")
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Reporte")

    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"

    def __str__(self):
        return f"{self.usuario.username} - {self.plan.nombre} ({self.get_estado_display()})"

    def save(self, *args, **kwargs):
        # Si el gerente activa la suscripción y define la fecha de inicio, se calcula el vencimiento automáticamente
        if self.estado == 'activa' and self.fecha_inicio and not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.plan.duracion_dias)
        super().save(*args, **kwargs)

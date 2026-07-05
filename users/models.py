from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # "Interruptores" de rol
    is_client = models.BooleanField(default=True, verbose_name="Es Cliente")
    is_manager = models.BooleanField(default=False, verbose_name="Es Gerente")
    is_trainer = models.BooleanField(default=False, verbose_name="Es Entrenador")
    
    # Datos generales
    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Cédula de Identidad")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        # Un helper visual para el panel de administración
        rol = "Gerente" if self.is_manager else "Entrenador" if self.is_trainer else "Cliente"
        return f"{self.username} - {rol}"

# Aquí aplicamos tu idea de separar los datos específicos:
class PerfilCliente(models.Model):
    # Se conecta 1 a 1 con el CustomUser
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='perfil_cliente')
    
    # Atributos específicos del cliente
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    condiciones_medicas = models.TextField(blank=True, help_text="Alergias, lesiones previas, etc.")
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    
    class Meta:
        verbose_name = "Perfil de Cliente"
        verbose_name_plural = "Perfiles de Clientes"

    def __str__(self):
        return f"Perfil Cliente: {self.usuario.username}"

class PerfilEntrenador(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='perfil_entrenador')
    
    especialidad = models.CharField(max_length=100, help_text="Ej: Musculación, CrossFit, Cardio")
    experiencia_anios = models.PositiveSmallIntegerField(default=0, verbose_name="Años de experiencia")
    
    class Meta:
        verbose_name = "Perfil de Entrenador"
        verbose_name_plural = "Perfiles de Entrenadores"

    def __str__(self):
        return f"Entrenador: {self.usuario.username}"

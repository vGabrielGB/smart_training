from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistroClienteForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Aquí definimos qué datos le pedimos al momento de registrarse
        fields = ('username', 'email', 'cedula', 'telefono')
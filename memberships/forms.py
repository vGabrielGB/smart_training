from django import forms
from .models import Suscripcion, Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['nombre', 'descripcion', 'precio', 'duracion_dias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-input'}),
            'duracion_dias': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ['plan', 'referencia', 'banco_origen', 'captura_pago']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-select'}),
            'referencia': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. 1234567890'}),
            'banco_origen': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Banco Mercantil'}),
            'captura_pago': forms.FileInput(attrs={'class': 'form-file-input'}),
        }

from django import forms
from .models import Producto, Orden

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-input'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input'}),
            'imagen': forms.FileInput(attrs={'class': 'form-file-input'}),
        }

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['referencia', 'banco_origen', 'captura_pago']
        widgets = {
            'referencia': forms.TextInput(attrs={'class': 'form-input'}),
            'banco_origen': forms.TextInput(attrs={'class': 'form-input'}),
            'captura_pago': forms.FileInput(attrs={'class': 'form-file-input'}),
        }

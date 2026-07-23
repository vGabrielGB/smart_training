from django.shortcuts import render
from .models import Plan

def inicio(request):
    # Traemos todos los planes de la base de datos
    planes = Plan.objects.all()
    
    # Se los pasamos a la plantilla index.html
    return render(request, 'index.html', {'planes': planes})
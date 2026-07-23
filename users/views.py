from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroClienteForm
from .models import PerfilCliente

def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            # 1. Guardamos al usuario en la base de datos
            usuario = form.save()
            
            # 2. Le creamos su Perfil de Cliente vacío automáticamente
            PerfilCliente.objects.create(usuario=usuario)
            
            # 3. Lo logueamos automáticamente y lo enviamos al inicio
            login(request, usuario)
            return redirect('inicio')
    else:
        form = RegistroClienteForm()
    
    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(username=username, password=password)
            
            if usuario is not None:
                login(request, usuario)
                return redirect('inicio')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
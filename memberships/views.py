from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from .models import Plan, Suscripcion
from .forms import SuscripcionForm, PlanForm

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    return render(request, 'landing.html')

@login_required
def inicio(request):
    planes = Plan.objects.all()
    form = SuscripcionForm()
    suscripcion_actual = Suscripcion.objects.filter(
        usuario=request.user, 
        estado__in=['activa', 'pendiente']
    ).first()

    if request.method == 'POST':
        if suscripcion_actual:
            messages.warning(request, "Ya tienes una suscripción activa o en proceso.")
            return redirect('inicio')
            
        form = SuscripcionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_suscripcion = form.save(commit=False)
            nueva_suscripcion.usuario = request.user
            nueva_suscripcion.estado = 'pendiente'
            nueva_suscripcion.save()
            messages.success(request, "Tu pago ha sido reportado exitosamente. En breve será verificado.")
            return redirect('inicio')
                
    return render(request, 'dashboard_inicio.html', {
        'planes': planes,
        'form': form,
        'suscripcion': suscripcion_actual
    })

# Función de verificación para el gerente
def check_is_manager(user):
    return user.is_authenticated and getattr(user, 'is_manager', False)

@login_required
def dashboard_cliente(request):
    # Buscamos si el usuario ya tiene una suscripción activa o pendiente
    suscripcion_actual = Suscripcion.objects.filter(
        usuario=request.user, 
        estado__in=['activa', 'pendiente']
    ).first()

    if request.method == 'POST':
        if suscripcion_actual:
            messages.warning(request, "Ya tienes una suscripción activa o en proceso.")
            return redirect('dashboard_cliente')
            
        form = SuscripcionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_suscripcion = form.save(commit=False)
            nueva_suscripcion.usuario = request.user
            nueva_suscripcion.estado = 'pendiente' # Estado por defecto
            nueva_suscripcion.save()
            messages.success(request, "Tu pago ha sido reportado exitosamente. En breve será verificado.")
            return redirect('dashboard_cliente')
    else:
        form = SuscripcionForm()

    context = {
        'suscripcion': suscripcion_actual,
        'form': form,
    }
    return render(request, 'memberships/dashboard_cliente.html', context)


@user_passes_test(check_is_manager)
def dashboard_gerente(request):
    # Traemos solo las suscripciones pendientes
    suscripciones_pendientes = Suscripcion.objects.filter(estado='pendiente').order_by('fecha_reporte')
    
    # Importamos Orden aquí para evitar import circular si es necesario, pero mejor hacerlo arriba
    from store.models import Orden
    ordenes_pendientes = Orden.objects.filter(estado='pendiente').order_by('creado_el')
    
    context = {
        'suscripciones': suscripciones_pendientes,
        'ordenes': ordenes_pendientes,
    }
    return render(request, 'memberships/dashboard_gerente.html', context)


@user_passes_test(check_is_manager)
def aprobar_suscripcion(request, suscripcion_id):
    # Solo permitimos peticiones POST por seguridad
    if request.method == 'POST':
        suscripcion = get_object_or_404(Suscripcion, id=suscripcion_id, estado='pendiente')
        
        # Al cambiar estado a activa y definir fecha inicio, el método save() 
        # de tu modelo calculará la fecha_fin automáticamente.
        suscripcion.estado = 'activa'
        suscripcion.fecha_inicio = timezone.now().date()
        suscripcion.save()
        
        messages.success(request, f"La suscripción de {suscripcion.usuario.username} ha sido aprobada con éxito.")
        
    return redirect('dashboard_gerente')

@user_passes_test(check_is_manager)
def rechazar_suscripcion(request, suscripcion_id):
    if request.method == 'POST':
        suscripcion = get_object_or_404(Suscripcion, id=suscripcion_id, estado='pendiente')
        suscripcion.estado = 'vencida'  # Opcional: Podría ser 'rechazada' si se añade al choice
        suscripcion.save()
        messages.success(request, f"La suscripción de {suscripcion.usuario.username} ha sido rechazada.")
        
    return redirect('dashboard_gerente')

@user_passes_test(check_is_manager)
def gestionar_planes(request):
    planes = Plan.objects.all()
    
    if request.method == 'POST':
        if 'crear' in request.POST:
            form = PlanForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Plan creado exitosamente.")
                return redirect('gestionar_planes')
        elif 'eliminar' in request.POST:
            plan = get_object_or_404(Plan, id=request.POST.get('plan_id'))
            plan.delete()
            messages.success(request, "Plan eliminado.")
            return redirect('gestionar_planes')
        elif 'editar' in request.POST:
            plan = get_object_or_404(Plan, id=request.POST.get('plan_id'))
            form = PlanForm(request.POST, instance=plan)
            if form.is_valid():
                form.save()
                messages.success(request, "Plan actualizado.")
                return redirect('gestionar_planes')
    else:
        form = PlanForm()
        
    return render(request, 'memberships/gestionar_planes.html', {
        'planes': planes,
        'form': form
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Producto, Orden, DetalleOrden
from .forms import ProductoForm, OrdenForm

def check_is_manager(user):
    return user.is_authenticated and getattr(user, 'is_manager', False)

def tienda_inicio(request):
    productos = Producto.objects.all()
    # Contador de carrito para mostrar en navbar
    carrito = request.session.get('carrito', {})
    cantidad_carrito = sum(carrito.values())
    
    return render(request, 'store/tienda.html', {
        'productos': productos,
        'cantidad_carrito': cantidad_carrito
    })

@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})
    
    pid = str(producto_id)
    if pid in carrito:
        carrito[pid] += 1
    else:
        carrito[pid] = 1
        
    request.session['carrito'] = carrito
    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect('tienda_inicio')

@login_required
def ver_carrito(request):
    carrito_session = request.session.get('carrito', {})
    items_carrito = []
    total_compra = 0
    
    for pid, cantidad in carrito_session.items():
        producto = get_object_or_404(Producto, id=int(pid))
        subtotal = producto.precio * cantidad
        total_compra += subtotal
        items_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })
        
    if request.method == 'POST':
        if not items_carrito:
            messages.error(request, "Tu carrito está vacío.")
            return redirect('ver_carrito')
            
        form = OrdenForm(request.POST, request.FILES)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.usuario = request.user
            orden.total = total_compra
            orden.estado = 'pendiente'
            orden.save()
            
            for item in items_carrito:
                DetalleOrden.objects.create(
                    orden=orden,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['producto'].precio
                )
            
            # Limpiar carrito
            request.session['carrito'] = {}
            messages.success(request, "Orden enviada. En breve será verificada.")
            return redirect('tienda_inicio')
    else:
        form = OrdenForm()
        
    return render(request, 'store/carrito.html', {
        'items': items_carrito,
        'total': total_compra,
        'form': form
    })

@login_required
def vaciar_carrito(request):
    request.session['carrito'] = {}
    messages.info(request, "Carrito vaciado.")
    return redirect('tienda_inicio')

@user_passes_test(check_is_manager)
def gestionar_productos(request):
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        if 'crear' in request.POST:
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Producto creado exitosamente.")
                return redirect('gestionar_productos')
        elif 'eliminar' in request.POST:
            producto = get_object_or_404(Producto, id=request.POST.get('producto_id'))
            producto.delete()
            messages.success(request, "Producto eliminado.")
            return redirect('gestionar_productos')
        elif 'editar' in request.POST:
            producto = get_object_or_404(Producto, id=request.POST.get('producto_id'))
            form = ProductoForm(request.POST, request.FILES, instance=producto)
            if form.is_valid():
                form.save()
                messages.success(request, "Producto actualizado.")
                return redirect('gestionar_productos')
            
    else:
        form = ProductoForm()
        
    return render(request, 'store/gestionar_productos.html', {
        'productos': productos,
        'form': form
    })

@user_passes_test(check_is_manager)
def aprobar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(Orden, id=orden_id, estado='pendiente')
        orden.estado = 'completada'
        orden.save()
        messages.success(request, f"La orden #{orden.id} ha sido aprobada.")
    return redirect('dashboard_gerente')

@user_passes_test(check_is_manager)
def rechazar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(Orden, id=orden_id, estado='pendiente')
        orden.estado = 'cancelada'
        orden.save()
        messages.success(request, f"La orden #{orden.id} ha sido rechazada.")
    return redirect('dashboard_gerente')

from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda_inicio, name='tienda_inicio'),
    path('gestionar/', views.gestionar_productos, name='gestionar_productos'),
    path('aprobar_orden/<int:orden_id>/', views.aprobar_orden, name='aprobar_orden'),
    path('rechazar_orden/<int:orden_id>/', views.rechazar_orden, name='rechazar_orden'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('gerente/', views.dashboard_gerente, name='dashboard_gerente'),
    path('gerente/aprobar/<int:suscripcion_id>/', views.aprobar_suscripcion, name='aprobar_suscripcion'),
    path('gerente/rechazar/<int:suscripcion_id>/', views.rechazar_suscripcion, name='rechazar_suscripcion'),
    path('gerente/planes/', views.gestionar_planes, name='gestionar_planes'),
]

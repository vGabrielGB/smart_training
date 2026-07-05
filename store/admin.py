from django.contrib import admin
from .models import Producto, Orden, DetalleOrden

admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
# Register your models here.

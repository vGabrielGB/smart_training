from django.db import models
from django.conf import settings

class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio ($)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Inventario / Stock")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen del Producto")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    ESTADOS_ORDEN = (
        ('pendiente', 'Pendiente de Verificación'),
        ('completada', 'Pagado y Entregado'),
        ('cancelada', 'Cancelada'),
    )
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Cliente")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total de la Orden ($)")
    estado = models.CharField(max_length=15, choices=ESTADOS_ORDEN, default='pendiente', verbose_name="Estado de la Orden")
    
    # Registro de Pago Móvil para la compra
    referencia = models.CharField(max_length=50, verbose_name="Número de Referencia")
    banco_origen = models.CharField(max_length=50, verbose_name="Banco de Origen")
    captura_pago = models.ImageField(upload_to='capturas_tienda/', verbose_name="Captura de Pantalla (Comprobante)")
    creado_el = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la Orden")

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles', verbose_name="Orden")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario ($)")

    class Meta:
        verbose_name = "Detalle de la Orden"
        verbose_name_plural = "Detalles de las Órdenes"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Orden #{self.orden.id})"
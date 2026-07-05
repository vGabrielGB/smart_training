from django.contrib import admin
from .models import Plan, Suscripcion

# Le decimos a Django que queremos ver estas tablas en el panel de administración
admin.site.register(Plan)
admin.site.register(Suscripcion)

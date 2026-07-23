from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PerfilCliente, PerfilEntrenador

# Registramos nuestro usuario personalizado con la seguridad por defecto de Django
admin.site.register(CustomUser, UserAdmin)

# Registramos los perfiles
admin.site.register(PerfilCliente)
admin.site.register(PerfilEntrenador)
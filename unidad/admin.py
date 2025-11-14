from django.contrib import admin
from .models import Unidad

# ❌ Eliminar el registro normal
# @admin.register(Unidad)
# class UnidadAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'descripcion')

# ✅ Registrar el modelo pero ocultarlo completamente
admin.site.unregister(Unidad) if admin.site.is_registered(Unidad) else None
from django.contrib import admin
from .models import Unidad

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
from django.contrib import admin

# Register your models here.

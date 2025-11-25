from django.contrib import admin
from .models import Menu, MenuProducto, Pedido, PedidoItem

class MenuProductoInline(admin.TabularInline):
    model = MenuProducto
    extra = 1

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria_menu', 'precio_base', 'descuento', 'disponible']
    list_filter = ['categoria_menu', 'disponible']
    search_fields = ['nombre', 'descripcion']
    inlines = [MenuProductoInline]

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ['precio_unitario', 'descuento_aplicado']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'cliente_nombre', 'estado', 'total', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['numero_pedido', 'cliente_nombre']
    readonly_fields = ['numero_pedido', 'subtotal', 'descuento_total', 'total']
    inlines = [PedidoItemInline]
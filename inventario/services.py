from django.utils import timezone
from .models import InventarioDiario, MovimientoInventario, HistorialStock


def descontar_stock_por_venta(pedido, usuario=None):
    hoy = timezone.now().date()

    # Buscar inventario abierto del día
    inventario = InventarioDiario.objects.filter(
        fecha=hoy,
        estado='abierto'
    ).order_by('-fecha_apertura').first()

    if not inventario:
        # No hay inventario abierto hoy — no hacemos nada
        return

    # Recorrer los items del pedido
    for item in pedido.items.select_related('menu').all():
        menu = item.menu
        if not menu:
            continue

        # Recorrer los productos de este menú
        for menu_producto in menu.menu_productos.select_related(
            'producto', 'producto__unidad'
        ).all():
            producto = menu_producto.producto

            # Solo procesamos productos por UNIDAD
            # tipo_inventario es una property que depende de unidad.tipo
            if not producto.unidad or producto.unidad.tipo != 'unidad':
                continue

            # Buscar el movimiento de este producto en el inventario de hoy
            try:
                movimiento = MovimientoInventario.objects.get(
                    inventario_diario=inventario,
                    producto=producto
                )
            except MovimientoInventario.DoesNotExist:
                # Producto no registrado en el inventario de hoy — omitir
                continue

            # Calcular cantidad a descontar
            cantidad_a_descontar = item.cantidad
            if hasattr(menu_producto, 'cantidad') and menu_producto.cantidad:
                cantidad_a_descontar = item.cantidad * menu_producto.cantidad

            stock_anterior = producto.stock

            # Registrar consumo en el movimiento de inventario
            movimiento.registrar_consumo_venta(cantidad_a_descontar)

            # Actualizar stock del producto
            producto.refresh_from_db()
            nuevo_stock = max(0, producto.stock - cantidad_a_descontar)
            producto.stock = nuevo_stock
            producto.save()

            # Registrar en historial
            HistorialStock.objects.create(
                producto=producto,
                tipo_movimiento='salida',
                cantidad=cantidad_a_descontar,
                stock_anterior=stock_anterior,
                stock_nuevo=nuevo_stock,
                referencia=f"Pedido #{pedido.numero_pedido}",
                observaciones=f"Descuento automático por venta — {menu.nombre}",
                usuario=str(usuario) if usuario else 'Sistema'
            )
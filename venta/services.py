from decimal import Decimal
from venta.models import Venta, VentaItem

def crear_venta_desde_pedido(pedido):

    if hasattr(pedido, 'venta'):
        return pedido.venta  # ya existe

    venta = Venta.objects.create(
        pedido=pedido,
        mesero=pedido.mesero,
        cliente_nombre=pedido.cliente_nombre,
        cliente_factura=None,
        tipo_pedido=pedido.tipo_pedido,
        mesa=pedido.mesa if pedido.tipo_pedido == 'mesa' else None,
        subtotal=pedido.subtotal,
        descuento_total=pedido.descuento_total,
        total=pedido.total,
    )

    # 🔥 AQUÍ ESTABA EL ERROR — FALTABA ESTO
    for item in pedido.items.all():
        VentaItem.objects.create(
            venta=venta,
            nombre=item.menu.nombre,  # ajusta si tu campo se llama diferente
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            subtotal=item.precio_unitario * item.cantidad
        )

    return venta

def finalizar_venta_y_pedido(venta):
    venta.estado = 'pagado'
    venta.save()

    pedido = venta.pedido
    pedido.estado = 'terminado'
    pedido.save()
from decimal import Decimal

def actualizar_venta_desde_pedido(pedido):

    if not hasattr(pedido, 'venta'):
        return

    venta = pedido.venta

    # Actualizar totales
    venta.subtotal = pedido.subtotal
    venta.descuento_total = pedido.descuento_total
    venta.total = pedido.total
    venta.save()

    # 🔥 Eliminar items anteriores
    venta.items.all().delete()

    # 🔥 Volver a crear items actualizados
    for item in pedido.items.all():
        VentaItem.objects.create(
            venta=venta,
            nombre=item.menu.nombre,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            subtotal=item.precio_unitario * item.cantidad
        )



"""
Funciones que el asistente puede ejecutar sobre la base de datos.
Cada función retorna un dict con los datos listos para responder.
"""
from django.utils import timezone
from django.db.models import Sum, Count, Q
from decimal import Decimal


# ── STOCK Y PRODUCTOS ──────────────────────────────────────────────────────────

def consultar_stock(nombre_producto: str = None):
    """Consulta el stock de uno o todos los productos."""
    from producto.models import Producto

    qs = Producto.objects.select_related('categoria', 'unidad')
    if nombre_producto:
        qs = qs.filter(nombre__icontains=nombre_producto)

    productos = [    {
        "type": "function",
        "function": {
            "name": "mesas_ocupadas",
            "description": "Muestra qué mesas tienen pedidos activos ahora mismo y cuántas están libres.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_pedido",
            "description": "Consulta el estado y detalle de un pedido específico por su número (ej: PED-00015).",
            "parameters": {
                "type": "object",
                "properties": {
                    "numero_pedido": {"type": "string", "description": "Número del pedido a consultar"}
                },
                "required": ["numero_pedido"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cambiar_estado_pedido",
            "description": "Cambia el estado de un pedido. Estados válidos: pendiente, preparando, listo, entregado, cancelado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numero_pedido": {"type": "string", "description": "Número del pedido"},
                    "nuevo_estado": {"type": "string", "description": "Nuevo estado: pendiente, preparando, listo, entregado, cancelado"}
                },
                "required": ["numero_pedido", "nuevo_estado"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "top_ventas",
            "description": "Retorna los productos más vendidos en los últimos N días.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dias": {"type": "integer", "description": "Número de días hacia atrás. Default: 7"},
                    "limite": {"type": "integer", "description": "Cuántos productos mostrar. Default: 10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ventas_por_mesero",
            "description": "Muestra el total de ventas agrupado por mesero en los últimos N días.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dias": {"type": "integer", "description": "Número de días hacia atrás. Default: 7"}
                },
                "required": []
            }
        }
    },
]
    for p in qs:
        productos.append({
            'id': p.id,
            'nombre': p.nombre,
            'stock': float(p.stock or 0),
            'unidad': str(p.unidad) if p.unidad else 'unidad',
            'categoria': str(p.categoria) if p.categoria else 'Sin categoría',
            'disponible': p.disponible,
        })

    return {
        'total': len(productos),
        'productos': productos,
        'busqueda': nombre_producto or 'todos',
    }


def productos_por_agotarse(limite: int = 5):
    """Retorna productos con stock menor o igual al límite."""
    from producto.models import Producto

    qs = Producto.objects.filter(
        stock__lte=limite,
        disponible=True
    ).select_related('categoria', 'unidad').order_by('stock')

    productos = []
    for p in qs:
        productos.append({
            'nombre': p.nombre,
            'stock': float(p.stock or 0),
            'unidad': str(p.unidad) if p.unidad else 'unidad',
            'categoria': str(p.categoria) if p.categoria else 'Sin categoría',
        })

    return {
        'total': len(productos),
        'limite_alerta': limite,
        'productos': productos,
    }


# ── PEDIDOS ────────────────────────────────────────────────────────────────────

def ver_pedidos_activos():
    """Retorna pedidos pendientes y en preparación."""
    from menu.models import Pedido

    qs = Pedido.objects.filter(
        estado__in=['pendiente', 'preparando']
    ).prefetch_related('items__menu').select_related('mesa', 'mesero').order_by('fecha_creacion')

    pedidos = []
    for p in qs:
        items = [
            f"{i.cantidad}x {i.menu.nombre}" for i in p.items.all() if i.menu
        ]
        pedidos.append({
            'numero': p.numero_pedido,
            'estado': p.get_estado_display(),
            'mesa': str(p.mesa) if p.mesa else 'Para llevar',
            'mesero': p.mesero.get_full_name() if p.mesero else 'Sin asignar',
            'items': items,
            'total': float(p.total),
            'hora': p.fecha_creacion.strftime('%H:%M'),
        })

    return {
        'total': len(pedidos),
        'pedidos': pedidos,
    }


def crear_pedido(mesa_nombre: str, items: list, cliente_nombre: str = 'Cliente', usuario_id: int = None):
    """
    Crea un pedido con los items indicados y genera la venta automáticamente.
    items = [{'menu_nombre': 'Sancocho', 'cantidad': 2}, ...]
    usuario_id: ID del usuario logueado (mesero)
    """
    from menu.models import Pedido, PedidoItem, Menu
    from mesa.models import Mesa
    from venta.models import Venta, VentaItem
    from usuario.models import Usuario

    # Buscar mesa
    mesa = None
    if mesa_nombre and mesa_nombre.lower() != 'para llevar':
        mesa = Mesa.objects.filter(numero__icontains=mesa_nombre).first()

    # Obtener mesero logueado
    mesero = None
    if usuario_id:
        mesero = Usuario.objects.filter(id=usuario_id).first()

    # Crear pedido
    pedido = Pedido.objects.create(
        cliente_nombre=cliente_nombre,
        mesa=mesa,
        mesero=mesero,
        tipo_pedido='mesa' if mesa else 'llevar',
        estado='pendiente',
    )

    items_creados = []
    items_no_encontrados = []

    for item_data in items:
        nombre = item_data.get('menu_nombre', '')
        cantidad = int(item_data.get('cantidad', 1))

        menu = Menu.objects.filter(
            nombre__icontains=nombre,
            disponible=True
        ).first()

        if menu:
            PedidoItem.objects.create(
                pedido=pedido,
                menu=menu,
                cantidad=cantidad,
                precio_unitario=menu.get_precio_final(),
                descuento_aplicado=menu.descuento or 0,
            )
            items_creados.append(f"{cantidad}x {menu.nombre}")
        else:
            items_no_encontrados.append(nombre)

    # Calcular totales del pedido
    pedido.calcular_totales()
    pedido.refresh_from_db()

    # Crear venta asociada automáticamente
    try:
        venta = Venta.objects.create(
            pedido=pedido,
            mesero=mesero,
            cliente_nombre=cliente_nombre,
            tipo_pedido=pedido.tipo_pedido,
            mesa=mesa,
            subtotal=pedido.subtotal,
            descuento_total=pedido.descuento_total,
            total=pedido.total,
            estado='pendiente',
        )
        venta_creada = venta.numero_factura
    except Exception as e:
        venta_creada = f'Error al crear venta: {str(e)}'

    return {
        'exito': True,
        'numero_pedido': pedido.numero_pedido,
        'numero_factura': venta_creada,
        'mesa': str(mesa) if mesa else 'Para llevar',
        'mesero': mesero.get_full_name() if mesero else 'Sin asignar',
        'items_creados': items_creados,
        'items_no_encontrados': items_no_encontrados,
        'total': float(pedido.total),
    }


# ── VENTAS ─────────────────────────────────────────────────────────────────────

def ventas_del_dia():
    """Retorna el resumen de ventas del día actual."""
    from venta.models import Venta, VentaItem
    from menu.models import Pedido

    hoy = timezone.now().date()

    # Ventas pagadas hoy
    qs_ventas = Venta.objects.filter(fecha_venta__date=hoy, estado='pagado')
    total_ventas = qs_ventas.aggregate(total=Sum('total'))['total'] or Decimal('0')
    cantidad_ventas = qs_ventas.count()

    # Top productos vendidos hoy
    top = VentaItem.objects.filter(
        venta__fecha_venta__date=hoy,
        venta__estado='pagado'
    ).values('nombre').annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:5]

    # Pedidos entregados hoy
    pedidos_entregados = Pedido.objects.filter(
        fecha_actualizacion__date=hoy,
        estado='entregado'
    ).count()

    # Pedidos activos ahora
    pedidos_activos = Pedido.objects.filter(
        estado__in=['pendiente', 'preparando']
    ).count()

    resultado = {
        'fecha': hoy.strftime('%d/%m/%Y'),
        'total_ventas': float(total_ventas),
        'cantidad_ventas': cantidad_ventas,
        'pedidos_entregados_hoy': pedidos_entregados,
        'pedidos_activos_ahora': pedidos_activos,
        'top_productos': list(top),
    }

    if cantidad_ventas == 0:
        resultado['mensaje'] = 'No hay ventas pagadas hoy. Se muestran pedidos entregados como referencia.'

    return resultado


# ── MAPA DE TOOLS PARA GROQ ───────────────────────────────────────────────────

TOOLS_GROQ = [
    {
        "type": "function",
        "function": {
            "name": "consultar_stock",
            "description": "Consulta el stock de productos. Si se da un nombre, busca ese producto específico. Sin nombre retorna todos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_producto": {
                        "type": "string",
                        "description": "Nombre o parte del nombre del producto a buscar. Opcional."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "productos_por_agotarse",
            "description": "Retorna productos con stock bajo, por defecto los que tienen 5 o menos unidades.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limite": {
                        "type": "integer",
                        "description": "Stock máximo para considerar que un producto está por agotarse. Default: 5"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ver_pedidos_activos",
            "description": "Retorna todos los pedidos pendientes y en preparación en este momento.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crear_pedido",
            "description": "Crea un nuevo pedido en el sistema con los items indicados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mesa_nombre": {
                        "type": "string",
                        "description": "Nombre o número de la mesa. Usar 'para llevar' si no es en mesa."
                    },
                    "items": {
                        "type": "array",
                        "description": "Lista de items del pedido",
                        "items": {
                            "type": "object",
                            "properties": {
                                "menu_nombre": {"type": "string", "description": "Nombre del plato/menú"},
                                "cantidad": {"type": "integer", "description": "Cantidad a pedir"}
                            },
                            "required": ["menu_nombre", "cantidad"]
                        }
                    },
                    "cliente_nombre": {
                        "type": "string",
                        "description": "Nombre del cliente. Default: Cliente"
                    }
                },
                "required": ["mesa_nombre", "items"],
                "note": "El mesero se asigna automáticamente con el usuario logueado."
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ventas_del_dia",
            "description": "Retorna el resumen de ventas del día actual: total en dinero, cantidad de ventas y productos más vendidos.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
]

# Mapa nombre → función Python

# ── NUEVAS TOOLS ───────────────────────────────────────────────────────────────

def mesas_ocupadas():
    """Retorna mesas con pedidos activos en este momento."""
    from menu.models import Pedido
    from mesa.models import Mesa

    pedidos_activos = Pedido.objects.filter(
        estado__in=['pendiente', 'preparando', 'listo'],
        mesa__isnull=False
    ).select_related('mesa', 'mesero').prefetch_related('items__menu')

    mesas = []
    for p in pedidos_activos:
        items = [f"{i.cantidad}x {i.menu.nombre}" for i in p.items.all() if i.menu]
        mesas.append({
            'mesa': str(p.mesa),
            'pedido': p.numero_pedido,
            'estado': p.get_estado_display(),
            'mesero': p.mesero.get_full_name() if p.mesero else 'Sin asignar',
            'items': items,
            'total': float(p.total),
            'tiempo': p.fecha_creacion.strftime('%H:%M'),
        })

    mesas_libres = Mesa.objects.exclude(
        pedido__estado__in=['pendiente', 'preparando', 'listo']
    ).count()

    return {
        'mesas_ocupadas': len(mesas),
        'mesas_libres': mesas_libres,
        'detalle': mesas,
    }


def consultar_pedido(numero_pedido: str):
    """Consulta el estado y detalle de un pedido específico por número."""
    from menu.models import Pedido

    try:
        pedido = Pedido.objects.prefetch_related(
            'items__menu'
        ).select_related('mesa', 'mesero').get(numero_pedido__icontains=numero_pedido)
    except Pedido.DoesNotExist:
        return {'error': f'No se encontró el pedido {numero_pedido}'}
    except Pedido.MultipleObjectsReturned:
        return {'error': f'Hay múltiples pedidos con ese número, sé más específico'}

    items = [
        f"{i.cantidad}x {i.menu.nombre} (${float(i.get_total())})"
        for i in pedido.items.all() if i.menu
    ]

    return {
        'numero': pedido.numero_pedido,
        'estado': pedido.get_estado_display(),
        'cliente': pedido.cliente_nombre,
        'mesa': str(pedido.mesa) if pedido.mesa else 'Para llevar',
        'mesero': pedido.mesero.get_full_name() if pedido.mesero else 'Sin asignar',
        'items': items,
        'total': float(pedido.total),
        'creado': pedido.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
        'actualizado': pedido.fecha_actualizacion.strftime('%d/%m/%Y %H:%M'),
    }


def cambiar_estado_pedido(numero_pedido: str, nuevo_estado: str):
    """Cambia el estado de un pedido específico."""
    from menu.models import Pedido

    estados_validos = ['pendiente', 'preparando', 'listo', 'entregado', 'cancelado']
    if nuevo_estado not in estados_validos:
        return {'error': f'Estado inválido. Usa uno de: {", ".join(estados_validos)}'}

    try:
        pedido = Pedido.objects.select_related('mesero').get(
            numero_pedido__icontains=numero_pedido
        )
    except Pedido.DoesNotExist:
        return {'error': f'No se encontró el pedido {numero_pedido}'}

    if pedido.estado == 'entregado':
        return {'error': 'Este pedido ya fue entregado y no puede modificarse'}
    if pedido.estado == 'cancelado':
        return {'error': 'Este pedido ya fue cancelado y no puede modificarse'}

    estado_anterior = pedido.get_estado_display()
    pedido.estado = nuevo_estado
    pedido.save()

    # Si se entrega, cerrar la venta
    if nuevo_estado == 'entregado' and hasattr(pedido, 'venta'):
        pedido.venta.estado = 'pagado'
        pedido.venta.save()

    return {
        'exito': True,
        'numero': pedido.numero_pedido,
        'estado_anterior': estado_anterior,
        'estado_nuevo': pedido.get_estado_display(),
        'venta_cerrada': nuevo_estado == 'entregado',
    }


def top_ventas(dias: int = 7, limite: int = 10):
    """Retorna los productos más vendidos en los últimos N días."""
    from venta.models import VentaItem
    from django.utils import timezone
    from django.db.models import Sum

    desde = timezone.now() - timezone.timedelta(days=dias)

    top = VentaItem.objects.filter(
        venta__fecha_venta__gte=desde,
        venta__estado='pagado'
    ).values('nombre').annotate(
        total_vendido=Sum('cantidad'),
        total_ingresos=Sum('subtotal')
    ).order_by('-total_vendido')[:limite]

    return {
        'periodo_dias': dias,
        'desde': desde.strftime('%d/%m/%Y'),
        'hasta': timezone.now().strftime('%d/%m/%Y'),
        'top_productos': [
            {
                'nombre': t['nombre'],
                'cantidad_vendida': t['total_vendido'],
                'ingresos': float(t['total_ingresos'] or 0),
            }
            for t in top
        ],
    }


def ventas_por_mesero(dias: int = 7):
    """Retorna el resumen de ventas agrupado por mesero."""
    from venta.models import Venta
    from django.utils import timezone
    from django.db.models import Sum, Count

    desde = timezone.now() - timezone.timedelta(days=dias)

    resultados = Venta.objects.filter(
        fecha_venta__gte=desde,
        estado='pagado',
        mesero__isnull=False
    ).values(
        'mesero__nombre', 'mesero__email'
    ).annotate(
        total_ventas=Sum('total'),
        cantidad_ventas=Count('id')
    ).order_by('-total_ventas')

    return {
        'periodo_dias': dias,
        'meseros': [
            {
                'mesero': r['mesero__nombre'] or r['mesero__email'],
                'total_ventas': float(r['total_ventas'] or 0),
                'cantidad_ventas': r['cantidad_ventas'],
            }
            for r in resultados
        ],
    }
FUNCIONES = {
    'consultar_stock': consultar_stock,
    'productos_por_agotarse': productos_por_agotarse,
    'ver_pedidos_activos': ver_pedidos_activos,
    'crear_pedido': crear_pedido,
    'ventas_del_dia': ventas_del_dia,
    'mesas_ocupadas': mesas_ocupadas,
    'consultar_pedido': consultar_pedido,
    'cambiar_estado_pedido': cambiar_estado_pedido,
    'top_ventas': top_ventas,
    'ventas_por_mesero': ventas_por_mesero,
}

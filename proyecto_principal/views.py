# proyecto_principal/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from decimal import Decimal
import json
from datetime import timedelta

from venta.models import Venta
from menu.models import Pedido
from mesa.models import Mesa
from producto.models import Producto


def home(request):
    return render(request, 'public/home.html')


@login_required(login_url='/login/')
def dashboard(request):
    cargo = getattr(request.user, 'cargo', None)

    if cargo == 'administrador':
        contexto = _contexto_administrador()
    elif cargo == 'cajera':
        contexto = _contexto_cajera()
    elif cargo == 'cocinero':
        contexto = _contexto_cocinero()
    elif cargo == 'parrilla':
        contexto = _contexto_parrilla()
    elif cargo == 'mesero':
        contexto = _contexto_mesero()
    else:
        contexto = {}

    contexto['cargo'] = cargo
    return render(request, 'dashboard/aside/Dashboard.html', contexto)


# ══════════════════════════════════════════════
# CONTEXTO ADMINISTRADOR — Ve todo
# ══════════════════════════════════════════════
def _contexto_administrador():
    hoy        = timezone.now().date()
    inicio_mes = hoy.replace(day=1)

    # ── Tarjetas resumen ──
    ventas_hoy = Venta.objects.filter(
        fecha_venta__date=hoy,
        estado='pagado'
    ).aggregate(total=Sum('total'), cantidad=Count('id'))

    ventas_mes = Venta.objects.filter(
        fecha_venta__date__gte=inicio_mes,
        estado='pagado'
    ).aggregate(total=Sum('total'), cantidad=Count('id'))

    pedidos_activos = Pedido.objects.exclude(
        estado__in=['entregado', 'cancelado']
    ).count()

    mesas_ocupadas = Mesa.objects.filter(
        pedido__estado__in=['pendiente', 'preparando', 'listo']
    ).distinct().count()

    total_mesas = Mesa.objects.count()

    productos_bajo_stock = Producto.objects.filter(
        disponible=True,
        stock__lt=10
    ).order_by('stock')[:5]

    # ── Pedidos por estado (gráfico dona) ──
    estados_pedidos = Pedido.objects.values('estado').annotate(
        cantidad=Count('id')
    ).order_by('estado')

    estados_labels  = [e['estado'].capitalize() for e in estados_pedidos]
    estados_data    = [e['cantidad'] for e in estados_pedidos]
    estados_colores = {
        'pendiente':  '#f6c23e',
        'preparando': '#36b9cc',
        'listo':      '#1cc88a',
        'entregado':  '#4e73df',
        'cancelado':  '#e74a3b',
    }
    estados_bg = [
        estados_colores.get(e['estado'], '#858796')
        for e in estados_pedidos
    ]

    # ── Ingresos últimos 7 días (gráfico línea) ──
    ingresos_semana = []
    labels_semana   = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        total_dia = Venta.objects.filter(
            fecha_venta__date=dia,
            estado='pagado'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        ingresos_semana.append(float(total_dia))
        labels_semana.append(dia.strftime('%d/%m'))

    # ── Ventas por método de pago (gráfico dona) ──
    metodos = Venta.objects.filter(
        estado='pagado'
    ).values('metodo_pago').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('-total')

    metodos_labels  = [m['metodo_pago'].capitalize() if m['metodo_pago'] else 'Sin especificar' for m in metodos]
    metodos_data    = [float(m['total'] or 0) for m in metodos]
    metodos_colores = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e']

    # ── Últimos 8 pedidos ──
    ultimos_pedidos = Pedido.objects.select_related(
        'mesa'
    ).order_by('-fecha_creacion')[:8]

    return {
        # Tarjetas
        'ventas_hoy_total':    ventas_hoy['total'] or Decimal('0'),
        'ventas_hoy_cantidad': ventas_hoy['cantidad'] or 0,
        'ventas_mes_total':    ventas_mes['total'] or Decimal('0'),
        'ventas_mes_cantidad': ventas_mes['cantidad'] or 0,
        'pedidos_activos':     pedidos_activos,
        'mesas_ocupadas':      mesas_ocupadas,
        'total_mesas':         total_mesas,
        'mesas_libres':        total_mesas - mesas_ocupadas,
        'productos_bajo_stock': productos_bajo_stock,

        # Gráficos (JSON para Chart.js)
        'estados_labels':   json.dumps(estados_labels),
        'estados_data':     json.dumps(estados_data),
        'estados_bg':       json.dumps(estados_bg),
        'labels_semana':    json.dumps(labels_semana),
        'ingresos_semana':  json.dumps(ingresos_semana),
        'metodos_labels':   json.dumps(metodos_labels),
        'metodos_data':     json.dumps(metodos_data),
        'metodos_colores':  json.dumps(metodos_colores[:len(metodos_labels)]),

        # Tabla
        'ultimos_pedidos': ultimos_pedidos,
    }


# ══════════════════════════════════════════════
# CONTEXTO CAJERA — Ventas y pedidos
# ══════════════════════════════════════════════
def _contexto_cajera():
    hoy        = timezone.now().date()
    inicio_mes = hoy.replace(day=1)

    ventas_hoy = Venta.objects.filter(
        fecha_venta__date=hoy,
        estado='pagado'
    ).aggregate(total=Sum('total'), cantidad=Count('id'))

    ventas_mes = Venta.objects.filter(
        fecha_venta__date__gte=inicio_mes,
        estado='pagado'
    ).aggregate(total=Sum('total'), cantidad=Count('id'))

    ventas_pendientes = Venta.objects.filter(estado='pendiente').count()

    metodos = Venta.objects.filter(
        estado='pagado'
    ).values('metodo_pago').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('-total')

    metodos_labels  = [m['metodo_pago'].capitalize() if m['metodo_pago'] else 'Sin especificar' for m in metodos]
    metodos_data    = [float(m['total'] or 0) for m in metodos]
    metodos_colores = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e']

    ultimas_ventas = Venta.objects.select_related(
        'pedido'
    ).order_by('-fecha_venta')[:8]

    # Ingresos últimos 7 días
    ingresos_semana = []
    labels_semana   = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        total_dia = Venta.objects.filter(
            fecha_venta__date=dia,
            estado='pagado'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        ingresos_semana.append(float(total_dia))
        labels_semana.append(dia.strftime('%d/%m'))

    return {
        'ventas_hoy_total':    ventas_hoy['total'] or Decimal('0'),
        'ventas_hoy_cantidad': ventas_hoy['cantidad'] or 0,
        'ventas_mes_total':    ventas_mes['total'] or Decimal('0'),
        'ventas_mes_cantidad': ventas_mes['cantidad'] or 0,
        'ventas_pendientes':   ventas_pendientes,
        'metodos_labels':      json.dumps(metodos_labels),
        'metodos_data':        json.dumps(metodos_data),
        'metodos_colores':     json.dumps(metodos_colores[:len(metodos_labels)]),
        'labels_semana':       json.dumps(labels_semana),
        'ingresos_semana':     json.dumps(ingresos_semana),
        'ultimas_ventas':      ultimas_ventas,
    }


# ══════════════════════════════════════════════
# CONTEXTO COCINERO — Solo su cocina
# ══════════════════════════════════════════════
def _contexto_cocinero():
    pedidos_pendientes  = Pedido.objects.filter(estado='pendiente').order_by('fecha_creacion')
    pedidos_preparando  = Pedido.objects.filter(estado='preparando').order_by('fecha_creacion')
    pedidos_listos      = Pedido.objects.filter(estado='listo').order_by('fecha_creacion')

    estados_pedidos = Pedido.objects.values('estado').annotate(
        cantidad=Count('id')
    ).order_by('estado')
    estados_labels  = [e['estado'].capitalize() for e in estados_pedidos]
    estados_data    = [e['cantidad'] for e in estados_pedidos]
    estados_colores = {
        'pendiente':  '#f6c23e',
        'preparando': '#36b9cc',
        'listo':      '#1cc88a',
        'entregado':  '#4e73df',
        'cancelado':  '#e74a3b',
    }
    estados_bg = [
        estados_colores.get(e['estado'], '#858796')
        for e in estados_pedidos
    ]

    return {
        'pedidos_pendientes':  pedidos_pendientes,
        'pedidos_preparando':  pedidos_preparando,
        'pedidos_listos':      pedidos_listos,
        'total_pendientes':    pedidos_pendientes.count(),
        'total_preparando':    pedidos_preparando.count(),
        'total_listos':        pedidos_listos.count(),
        'estados_labels':      json.dumps(estados_labels),
        'estados_data':        json.dumps(estados_data),
        'estados_bg':          json.dumps(estados_bg),
    }


# ══════════════════════════════════════════════
# CONTEXTO PARRILLA — Igual que cocinero
# ══════════════════════════════════════════════
def _contexto_parrilla():
    return _contexto_cocinero()


# ══════════════════════════════════════════════
# CONTEXTO MESERO — Sus mesas y pedidos
# ══════════════════════════════════════════════
def _contexto_mesero():
    todas_las_mesas = Mesa.objects.all().order_by('numero')

    # Obtenemos todos los pedidos activos de una sola consulta
    pedidos_activos_ids = Pedido.objects.filter(
        mesa__isnull=False,
        estado__in=['pendiente', 'preparando', 'listo']
    ).values_list('mesa_id', flat=True)

    pedidos_por_mesa = {}
    for pedido in Pedido.objects.filter(
        mesa__isnull=False,
        estado__in=['pendiente', 'preparando', 'listo']
    ).select_related('mesa'):
        pedidos_por_mesa[pedido.mesa_id] = pedido

    mesas_con_estado = []
    for mesa in todas_las_mesas:
        pedido_activo = pedidos_por_mesa.get(mesa.id)
        mesas_con_estado.append({
            'mesa':          mesa,
            'pedido_activo': pedido_activo,
            'ocupada':       pedido_activo is not None,
        })

    mesas_libres   = sum(1 for m in mesas_con_estado if not m['ocupada'])
    mesas_ocupadas = sum(1 for m in mesas_con_estado if m['ocupada'])

    pedidos_recientes = Pedido.objects.exclude(
        estado__in=['entregado', 'cancelado']
    ).order_by('-fecha_creacion')[:8]

    return {
        'mesas_con_estado': mesas_con_estado,
        'mesas_libres':     mesas_libres,
        'mesas_ocupadas':   mesas_ocupadas,
        'total_mesas':      mesas_libres + mesas_ocupadas,
        'pedidos_recientes': pedidos_recientes,
    }
from django.shortcuts import render
from django.db.models import Sum, Count
from venta.models import Venta
from compra.models import Compra
from inventario.models import InventarioDiario  # ajusta la app si es diferente
from menu.models import Menu
from django.utils import timezone
import datetime

def informe_list(request):
    tipo = request.GET.get('tipo', 'ventas')
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    contexto = {
        'titulo': 'Consulta de Reportes',
        'tipo_actual': tipo,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'mensaje': "Selecciona un tipo y un rango de fechas para consultar.",
        'resultados': None,
        'total': 0,
        'cantidad': 0,
    }

    fecha_inicio = None
    fecha_fin = None
    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        except:
            pass
    if fecha_fin_str:
        try:
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        except:
            pass

    if fecha_inicio and fecha_fin:
        if fecha_inicio > fecha_fin:
            contexto['mensaje'] = "La fecha de inicio no puede ser mayor que la fecha final."
        else:
            try:
                if tipo == 'ventas':
                    qs = Venta.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)\
                                      .select_related('pedido', 'pedido__mesa', 'admin')\
                                      .order_by('-fecha')
                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    contexto['total'] = qs.aggregate(Sum('total'))['total__sum'] or 0
                    contexto['mensaje'] = f"{contexto['cantidad']} ventas encontradas - Total: ${contexto['total']:,.2f}"

                elif tipo == 'compras':
                    qs = Compra.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)\
                                       .select_related('producto', 'proveedor')\
                                       .order_by('-fecha')
                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    # Total = precio unitario × cantidad
                    contexto['total'] = sum(c.precio * c.cantidad for c in qs)
                    contexto['mensaje'] = f"{contexto['cantidad']} compras encontradas - Total: ${contexto['total']:,.2f}"

                elif tipo == 'inventario':
                    qs = InventarioDiario.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)\
                                                .order_by('-fecha')
                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    contexto['abiertos'] = qs.filter(estado='abierto').count()
                    contexto['cerrados'] = qs.filter(estado='cerrado').count()
                    contexto['mensaje'] = f"{contexto['cantidad']} registros diarios - {contexto['abiertos']} abiertos, {contexto['cerrados']} cerrados"

                elif tipo == 'menu':
                    contexto['resultados'] = Menu.objects.all().order_by('nombre')
                    contexto['cantidad'] = contexto['resultados'].count()
                    contexto['mensaje'] = f"Mostrando {contexto['cantidad']} productos del menú actual (sin filtro por fecha)"

                else:
                    contexto['mensaje'] = "Tipo de reporte no reconocido."

            except Exception as e:
                contexto['mensaje'] = f"Error al consultar: {str(e)}"

    return render(request, 'modulos/informe.html', contexto)
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from venta.models import Venta
from compra.models import Compra
from inventario.models import InventarioDiario
from menu.models import Menu
from .models import Informe
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
            contexto['mensaje'] = "Formato de fecha de inicio inválido."
    if fecha_fin_str:
        try:
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        except:
            contexto['mensaje'] = "Formato de fecha de fin inválido."

    if fecha_inicio and fecha_fin:
        if fecha_inicio > fecha_fin:
            contexto['mensaje'] = "La fecha de inicio no puede ser mayor que la fecha final."
        else:
            try:
                if tipo == 'ventas':
                    qs = Venta.objects.filter(
                        fecha__gte=fecha_inicio,
                        fecha__lte=fecha_fin
                    ).select_related('pedido', 'admin').order_by('-fecha')
                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    total_sum = qs.aggregate(total_sum=Sum('total'))['total_sum']
                    contexto['total'] = total_sum if total_sum is not None else 0
                    contexto['mensaje'] = f"Se encontraron {contexto['cantidad']} ventas - Total: ${contexto['total']:,.2f}"

                elif tipo == 'compras':
                    qs = Compra.objects.filter(
                        fecha__gte=fecha_inicio,
                        fecha__lte=fecha_fin
                    ).select_related('producto', 'proveedor').order_by('-fecha')

                    # Calculamos subtotal en cada objeto
                    for compra in qs:
                        compra.subtotal = compra.precio * compra.cantidad

                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    contexto['total'] = sum(compra.subtotal for compra in qs)
                    contexto['mensaje'] = f"Se encontraron {contexto['cantidad']} compras - Total: ${contexto['total']:,.2f}"

                elif tipo == 'pedidos':
                    from pedido.models import Pedido
                    qs = Pedido.objects.filter(
                        fecha__gte=fecha_inicio,
                        fecha__lte=fecha_fin
                    ).prefetch_related('detalles__menu').order_by('-fecha')

                    # Calcular el total de cada pedido y preparar detalles
                    for pedido in qs:
                        total = 0
                        detalles_list = []
                        for detalle in pedido.detalles.all():
                            # Usar get_precio_final() que calcula el precio con descuento
                            precio = detalle.menu.get_precio_final() if hasattr(detalle.menu, 'get_precio_final') else (detalle.menu.precio_base if hasattr(detalle.menu, 'precio_base') else 0)
                            subtotal = precio * detalle.cantidad
                            total += subtotal
                            detalles_list.append({
                                'menu': detalle.menu.nombre,
                                'cantidad': detalle.cantidad,
                                'precio': precio,
                                'subtotal': subtotal
                            })
                        pedido.total_calculado = total
                        pedido.detalles_list = detalles_list

                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    contexto['total'] = sum(p.total_calculado for p in qs)
                    contexto['mensaje'] = f"Se encontraron {contexto['cantidad']} pedidos - Total: ${contexto['total']:,.2f}"

                elif tipo == 'inventario':
                    qs = InventarioDiario.objects.filter(
                        fecha__gte=fecha_inicio,
                        fecha__lte=fecha_fin
                    ).order_by('-fecha')
                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    contexto['abiertos'] = qs.filter(estado='abierto').count()
                    contexto['cerrados'] = qs.filter(estado='cerrado').count()
                    contexto['mensaje'] = f"{contexto['cantidad']} registros diarios encontrados ({contexto['abiertos']} abiertos, {contexto['cerrados']} cerrados)"

                elif tipo == 'menu':
                    qs = Menu.objects.all().order_by('nombre')
                    contexto['resultados'] = qs
                    contexto['cantidad'] = qs.count()
                    contexto['mensaje'] = f"Mostrando {contexto['cantidad']} productos del menú actual (sin filtro por fecha)"

                else:
                    contexto['mensaje'] = "Tipo de reporte no reconocido."

            except Exception as e:
                contexto['mensaje'] = f"Error al consultar: {str(e)}"

    return render(request, 'modulos/informe.html', contexto)


# Vistas CRUD para Informe (modelo de informes guardados)
class InformeListView(ListView):
    model = Informe
    template_name = 'modulos/informe.html'
    context_object_name = 'informes'


class InformeCreateView(CreateView):
    model = Informe
    fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin']
    template_name = 'forms/formulario_crear.html'
    success_url = reverse_lazy('apl:informe:informe_list')

    def form_valid(self, form):
        messages.success(self.request, "Informe creado correctamente")
        return super().form_valid(form)


class InformeUpdateView(UpdateView):
    model = Informe
    fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin']
    template_name = 'forms/formulario_actualizacion.html'
    success_url = reverse_lazy('apl:informe:informe_list')

    def form_valid(self, form):
        messages.success(self.request, "Informe actualizado correctamente")
        return super().form_valid(form)


class InformeDeleteView(DeleteView):
    model = Informe
    success_url = reverse_lazy('apl:informe:informe_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


def exportar_excel(request):
    # Implementación básica
    return HttpResponse("Exportar a Excel - En desarrollo", content_type="text/plain")


def exportar_pdf(request):
    # Implementación básica
    return HttpResponse("Exportar a PDF - En desarrollo", content_type="text/plain")
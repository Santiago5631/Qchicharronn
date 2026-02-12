from django.views.generic import ListView
from .models import Venta
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView

class VentaListView(ListView):
    model = Venta
    template_name = 'modulos/venta.html'
    context_object_name = 'ventas'
    ordering = ['-fecha_venta']  # más recientes primero

    def get_queryset(self):
        # optimización (no rompe nada)
        return Venta.objects.select_related('pedido').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔹 Separar ventas
        context['ventas_pendientes'] = self.object_list.filter(estado='pendiente')
        context['ventas_pagadas'] = self.object_list.filter(estado='pagado')

        context['titulo'] = 'Listado de Ventas'
        return context


class VentaDetailView(DetailView):
    model = Venta
    template_name = 'forms/venta_detalle.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        context['titulo'] = f'Detalle de Venta #{self.object.numero_factura}'
        return context



class VentaFacturaView(DetailView):
    model = Venta
    template_name = 'ventas/factura.html'
    context_object_name = 'venta'

    def get_object(self, queryset=None):
        venta = super().get_object(queryset)
        if venta.estado != 'pagado':
            raise Http404("La venta aún no está pagada")
        return venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Factura {self.object.numero_factura}'
        return context


class VentaFinalizarView(View):
    def post(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)

        if venta.estado == 'pagado':
            messages.warning(request, 'Esta venta ya está finalizada.')
            return redirect('apl:venta:venta_list')

        # 🔹 Obtener método de pago
        metodo_pago = request.POST.get('metodo_pago')

        if not metodo_pago:
            messages.error(request, 'Debe seleccionar un método de pago.')
            return redirect('apl:venta:venta_detail', pk=venta.pk)

        # 🔹 Guardar datos
        venta.metodo_pago = metodo_pago
        venta.estado = 'pagado'
        venta.save()

        # 🔄 Marcar pedido como entregado
        if venta.pedido:
            venta.pedido.estado = 'entregado'
            venta.pedido.save()

        messages.success(
            request,
            f'Venta #{venta.numero_factura} finalizada correctamente.'
        )

        return redirect('apl:venta:venta_detail', pk=venta.pk)

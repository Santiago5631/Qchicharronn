# venta/views.py
from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404

from .models import Venta

from usuario.permisos import RolRequeridoMixin, rol_requerido, SOLO_ADMIN, CAJA


# ADMIN_MESERO = ['administrador', 'mesero']
# Los cocineros no gestionan ventas/facturación


class VentaListView(RolRequeridoMixin, ListView):
    """
    Admin y Meseros pueden ver las ventas.
    (El mesero necesita ver el estado para saber cuándo cobrar)
    """
    roles_permitidos = CAJA
    model = Venta
    template_name = 'modulos/venta.html'
    context_object_name = 'ventas'
    ordering = ['-fecha_venta']

    def get_queryset(self):
        return Venta.objects.select_related('pedido').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ventas_pendientes'] = self.object_list.filter(estado='pendiente')
        context['ventas_pagadas']    = self.object_list.filter(estado='pagado')
        context['titulo']            = 'Listado de Ventas'
        return context


class VentaDetailView(RolRequeridoMixin, DetailView):
    """Admin y Meseros pueden ver el detalle de una venta."""
    roles_permitidos = CAJA
    model = Venta
    template_name = 'forms/venta_detalle.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items']  = self.object.items.all()
        context['titulo'] = f'Detalle de Venta #{self.object.numero_factura}'
        return context


class VentaFacturaView(RolRequeridoMixin, DetailView):
    """
    Admin y Meseros pueden ver la factura.
    Solo se muestra si la venta está pagada.
    """
    roles_permitidos = CAJA
    model = Venta
    template_name = 'forms/factura.html'
    context_object_name = 'venta'

    def get_queryset(self):
        return Venta.objects.select_related('pedido', 'mesa').prefetch_related('items')

    def get_object(self, queryset=None):
        venta = super().get_object(queryset)
        if venta.estado != 'pagado':
            raise Http404("La venta aún no está pagada")
        return venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = self.object
        context['titulo']       = f'Factura {venta.numero_factura}'
        context['items']        = venta.items.all()
        context['fecha']        = venta.fecha_venta
        context['metodo_pago']  = venta.get_metodo_pago_display()
        return context


class VentaFinalizarView(RolRequeridoMixin, View):
    """
    Admin y Meseros pueden finalizar/cobrar una venta.
    (El mesero es quien cobra al cliente)
    """
    roles_permitidos = CAJA

    def post(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)

        if venta.estado == 'pagado':
            messages.warning(request, 'Esta venta ya está finalizada.')
            return redirect('apl:venta:venta_list')

        metodo_pago = request.POST.get('metodo_pago')

        if not metodo_pago:
            messages.error(request, 'Debe seleccionar un método de pago.')
            return redirect('apl:venta:venta_detail', pk=venta.pk)

        venta.metodo_pago = metodo_pago
        venta.estado      = 'pagado'
        venta.save()

        if venta.pedido:
            venta.pedido.estado = 'entregado'
            venta.pedido.save()

        messages.success(
            request,
            f'Venta #{venta.numero_factura} finalizada correctamente.'
        )
        return redirect('apl:venta:venta_detail', pk=venta.pk)
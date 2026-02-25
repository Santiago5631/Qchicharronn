from django.views.generic import ListView
from .models import Venta
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from clientes.models import Cliente


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
        context['clientes'] = Cliente.objects.all()
        context['titulo'] = f'Detalle de Venta #{self.object.numero_factura}'
        venta = self.object
        if venta.cliente_factura:
            context['cliente_display'] = venta.cliente_factura
        elif venta.cliente:
            context['cliente_display'] = venta.cliente
        else:
            context['cliente_display'] = None
        return context





class VentaFacturaView(DetailView):
    model = Venta
    template_name = 'forms/factura.html'
    context_object_name = 'venta'

    def get_queryset(self):
        return Venta.objects.select_related(
            'pedido',
            'mesa',
            'cliente',
            'cliente_factura'
        ).prefetch_related(
            'items'
        )

    def get_object(self, queryset=None):
        venta = super().get_object(queryset)
        if venta.estado != 'pagado' and venta.estado != 'pendiente':
            raise Http404("Estado inválido")
        return venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        venta = self.object

        # Prioridad
        if venta.cliente_factura_id:  # usar _id es más confiable
            try:
                cliente_mostrar = Cliente.objects.get(pk=venta.cliente_factura_id)
            except Cliente.DoesNotExist:
                cliente_mostrar = None
        elif venta.cliente_id:
            try:
                cliente_mostrar = Cliente.objects.get(pk=venta.cliente_id)
            except Cliente.DoesNotExist:
                cliente_mostrar = None
        else:
            cliente_mostrar = None

        context['cliente_display'] = cliente_mostrar
        context['clientes'] = Cliente.objects.all()
        context['titulo'] = f'Factura {venta.numero_factura}'
        context['items'] = venta.items.all()

        return context


class VentaFinalizarView(View):
    def post(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)

        if venta.estado == 'pagado':
            messages.warning(request, 'Esta venta ya está finalizada.')
            return redirect('apl:venta:venta_list')

        # Obtener método de pago
        metodo_pago = request.POST.get('metodo_pago')
        if not metodo_pago:
            messages.error(request, 'Debe seleccionar un método de pago.')
            return redirect('apl:venta:venta_detail', pk=venta.pk)

        # 🔹 NUEVO: obtener cliente_factura del form
        cliente_factura_id = request.POST.get('cliente_factura', '').strip()

        if cliente_factura_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_factura_id)
                venta.cliente_factura = cliente
            except Cliente.DoesNotExist:
                messages.warning(request, 'Cliente seleccionado no encontrado.')
                venta.cliente_factura = None
        else:
            venta.cliente_factura = venta.cliente if venta.cliente else None

        # Guardar datos
        venta.metodo_pago = metodo_pago
        venta.estado = 'pagado'
        venta.save()

        # Marcar pedido como entregado
        if venta.pedido:
            venta.pedido.estado = 'entregado'
            venta.pedido.save()

        messages.success(
            request,
            f'Venta #{venta.numero_factura} finalizada correctamente.'
        )

        return redirect('apl:venta:factura', pk=venta.pk)


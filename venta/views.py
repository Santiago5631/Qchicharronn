from django.views.generic import ListView
from .models import Venta
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from clientes.models import Cliente

from usuario.permisos import RolRequeridoMixin, rol_requerido, SOLO_ADMIN, CAJA

# ── CAMBIO 3: importar el servicio de inventario ──
from inventario.services import descontar_stock_por_venta


class VentaListView(RolRequeridoMixin, ListView):
    roles_permitidos = CAJA
    model = Venta
    template_name = 'modulos/venta.html'
    context_object_name = 'ventas'
    ordering = ['-fecha_venta']

    def get_queryset(self):
        queryset = Venta.objects.select_related('pedido', 'mesero')
        if self.request.user.cargo == 'mesero':
            queryset = queryset.filter(mesero=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ventas_pendientes'] = self.object_list.filter(estado='pendiente')
        context['ventas_pagadas']    = self.object_list.filter(estado='pagado')
        context['titulo']            = 'Listado de Ventas'
        return context


class VentaDetailView(RolRequeridoMixin, DetailView):
    roles_permitidos = CAJA
    model = Venta
    template_name = 'forms/venta_detalle.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items']   = self.object.items.all()
        context['clientes'] = Cliente.objects.all()
        context['titulo']   = f'Detalle de Venta #{self.object.numero_factura}'
        venta = self.object
        if venta.cliente_factura:
            context['cliente_display'] = venta.cliente_factura
        elif venta.cliente:
            context['cliente_display'] = venta.cliente
        else:
            context['cliente_display'] = None
        return context


class VentaFacturaView(RolRequeridoMixin, DetailView):
    roles_permitidos = CAJA
    model = Venta
    template_name = 'forms/factura.html'
    context_object_name = 'venta'

    def get_queryset(self):
        return Venta.objects.select_related(
            'pedido', 'mesa', 'cliente', 'cliente_factura'
        ).prefetch_related('items')

    def get_object(self, queryset=None):
        venta = super().get_object(queryset)
        if venta.estado != 'pagado':
            raise Http404("La venta aún no está pagada")
        return venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = self.object

        if venta.cliente_factura_id:
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
        context['clientes']        = Cliente.objects.all()
        context['titulo']          = f'Factura {venta.numero_factura}'
        context['items']           = venta.items.all()
        context['metodo_pago']     = venta.get_metodo_pago_display()
        return context


class VentaFinalizarView(RolRequeridoMixin, View):
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

        venta.metodo_pago = metodo_pago
        venta.estado      = 'pagado'
        venta.save()

        if venta.pedido:
            venta.pedido.estado = 'entregado'
            venta.pedido.save()

        # ── CAMBIO 3: descontar stock del inventario abierto ──
        # Se ejecuta después de guardar la venta para no bloquear
        # Si no hay inventario abierto, la función lo omite silenciosamente
        try:
            descontar_stock_por_venta(
                pedido=venta.pedido,
                usuario=request.user.get_full_name() or request.user.username
            )
        except Exception as e:
            # No bloqueamos la venta si hay error en inventario
            # Solo notificamos al usuario
            messages.warning(
                request,
                f'Venta finalizada pero hubo un problema al descontar del inventario: {e}'
            )

        messages.success(
            request,
            f'Venta #{venta.numero_factura} finalizada correctamente.'
        )
        return redirect('apl:venta:factura', pk=venta.pk)
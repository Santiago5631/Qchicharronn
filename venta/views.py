from django.views.generic import ListView
from .models import Venta
from django.http import Http404

class VentaListView(ListView):
    model = Venta
    template_name = 'modulos/venta.html'
    context_object_name = 'ventas'
    ordering = ['fecha_venta']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        return context
from django.views.generic import DetailView

class VentaDetailView(DetailView):
    model = Venta
    template_name = 'forms/venta_detalle.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

# venta/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

def crear_venta_desde_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Evitar duplicados: si ya existe una venta pagada para este pedido
    if Venta.objects.filter(pedido=pedido, estado="pagado").exists():
        messages.error(request, f"El pedido {pedido.id} ya fue facturado.")
        return redirect('apl:pedido:detalle_pedido', pedido_id=pedido.id)  # ajusta esta url si es diferente

    # Si ya existe una venta en borrador o pendiente, la reutilizamos
    venta_existente = Venta.objects.filter(pedido=pedido).first()
    if venta_existente:
        messages.info(request, f"Ya existe una venta para este pedido. Redirigiendo...")
        return redirect('apl:venta:editar_venta', pk=venta_existente.pk)

    # Crear la venta automáticamente
    venta = Venta.objects.create(
        pedido=pedido,
        total=pedido.total,                    # asumiendo que Pedido tiene campo total
        metodo_pago="efectivo",                # puedes cambiar o luego editar
        estado="pendiente",
        admin=request.user.administrador if hasattr(request.user, 'administrador') else None
    )

    messages.success(request, f"Venta #{venta.id} creada correctamente desde el pedido {pedido.id}")
    return redirect('apl:venta:editar_venta', pk=venta.pk)

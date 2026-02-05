from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import *
from .forms import VentaForm


def listar_ventas(request):
    data = {
        "titulo": "Listado de Ventas",
        "ventas": Venta.objects.all()
    }
    return render(request, 'modulos/venta.html', data)


class VentaListView(ListView):
    model = Venta
    template_name = 'modulos/venta.html'
    context_object_name = 'ventas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        return context


class VentaCreateView(CreateView):
    model = Venta
    template_name = 'forms/formulario_crear.html'
    form_class = VentaForm
    success_url = '/apps/ventas/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Venta'
        context['modulo'] = "ventas "
        return context


class VentaUpdateView(UpdateView):
    model = Venta
    template_name = 'forms/formulario_actualizacion.html'
    form_class = VentaForm
    success_url = '/apps/ventas/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class VentaDeleteView(DeleteView):
    model = Venta
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/ventas/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Venta'
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

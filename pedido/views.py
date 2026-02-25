# pedido/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from pedido.forms import PedidoForm
from pedido.models import *

from usuario.permisos import RolRequeridoMixin, rol_requerido, TODOS, SOLO_ADMIN


class PedidoListView(RolRequeridoMixin, ListView):
    """Todos los roles pueden ver pedidos."""
    roles_permitidos = TODOS
    model = Pedido
    template_name = 'modulos/pedido.html'
    context_object_name = 'pedidos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Pedidos'
        return context


class PedidoCreateView(RolRequeridoMixin, CreateView):
    """Todos los roles pueden crear pedidos."""
    roles_permitidos = TODOS
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido/crear_pedido.html'
    success_url = '/apps/pedidos/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.filter(disponible=True)
        return context

    def post(self, request, *args, **kwargs):
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            productos_ids = request.POST.get('productos_seleccionados', '').split(',')
            cantidades    = request.POST.get('cantidades', '').split(',')

            for i, producto_id in enumerate(productos_ids):
                if producto_id.strip():
                    PedidoDetalle.objects.create(
                        pedido=pedido,
                        menu_id=int(producto_id),
                        cantidad=int(cantidades[i])
                    )

            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form))


class PedidoUpdateView(RolRequeridoMixin, UpdateView):
    """Todos los roles pueden editar pedidos."""
    roles_permitidos = TODOS
    model = Pedido
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['usuario', 'plato', 'cantidad', 'fecha']
    success_url = '/apps/pedidos/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class PedidoDeleteView(RolRequeridoMixin, DeleteView):
    """Solo administradores pueden eliminar pedidos."""
    roles_permitidos = SOLO_ADMIN
    model = Pedido
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/pedidos/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pedido'
        return context


# ──────────────────────────────────────────────
# COMANDAS — Acceso diferenciado por tipo de cocina
# ──────────────────────────────────────────────

@rol_requerido('administrador', 'parrilla')
def comanda_parrilla(request, pk):
    """
    Comanda para cocineros de PARRILLA.
    Acceso: Administrador y Cocinero de Parrilla.
    """
    pedido   = get_object_or_404(Pedido, pk=pk)
    detalles = pedido.obtener_comanda_parrilla()
    return render(request, 'templates/pedido/comanda_parrilla.html', {
        'pedido': pedido,
        'detalles': detalles
    })


@rol_requerido('administrador', 'cocinero')
def comanda_cocina(request, pk):
    """
    Comanda para cocineros de COCINA.
    Acceso: Administrador y Cocinero de Cocina.
    """
    pedido   = get_object_or_404(Pedido, pk=pk)
    detalles = pedido.obtener_comanda_cocina()
    return render(request, 'templates/pedido/comanda_cocina.html', {
        'pedido': pedido,
        'detalles': detalles
    })
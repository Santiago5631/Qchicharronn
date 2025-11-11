from django.shortcuts import render, get_object_or_404, redirect

from pedido.forms import PedidoForm
from pedido.models import *
from django.views.generic import *


def listar_pedidos(request):
    data = {
        "pedidos": "pedidos",
        "titulo": "Listado de Pedidos",
        "pedido": Pedido.objects.all()
    }
    return render(request, 'modulos/pedido.html', data)


class PedidoListView(ListView):
    model = Pedido
    template_name = 'modulos/pedido.html'
    context_object_name = 'pedidos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Pedidos'
        return context


class PedidoCreateView(CreateView):
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
            cantidades = request.POST.get('cantidades', '').split(',')

            for i, producto_id in enumerate(productos_ids):
                if producto_id.strip():
                    PedidoDetalle.objects.create(
                        pedido=pedido,
                        menu_id=int(producto_id),
                        cantidad=int(cantidades[i])
                    )

            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form))


class PedidoUpdateView(UpdateView):
    model = Pedido
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['usuario', 'plato', 'cantidad', 'fecha']
    success_url = '/apps/pedidos/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/pedidos/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pedido'
        return context

def comanda_parrilla(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    detalles = pedido.obtener_comanda_parrilla()
    return render(request, 'templates/pedido/comanda_parrila.html', {'pedido': pedido, 'detalles': detalles})

def comanda_cocina(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    detalles = pedido.obtener_comanda_cocina()
    return render(request, 'templates/pedido/comanda_cocina.html', {'pedido': pedido, 'detalles': detalles})
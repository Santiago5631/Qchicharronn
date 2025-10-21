from django.shortcuts import render
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
        return super().get_context_data(**kwargs)


class PedidoCreateView(CreateView):
    model = Pedido
    template_name = 'forms/formulario_crear.html'
    fields = ['mesa', 'fecha', 'estado', 'subtotal']
    success_url = '/apps/pedidos/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Pedido'
        context['modulo'] = "pedido"
        return context


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


from django.shortcuts import render

# Create your views here.

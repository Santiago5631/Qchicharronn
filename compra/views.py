from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import *
from .forms import CompraForm


def listar_compras(request):
    data = {
        "titulo": "Listado de Compras",
        "compras": Compra.objects.all()
    }
    return render(request, 'modulos/compra.html', data)


class CompraListView(ListView):
    model = Compra
    template_name = 'modulos/compra.html'
    context_object_name = 'compras'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Compras'
        return context


class CompraCreateView(CreateView):
    model = Compra
    template_name = 'forms/formulario_crear.html'
    form_class = CompraForm
    success_url = '/apps/compras/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Compra'
        context['modulo'] = "compra"
        return context


class CompraUpdateView(UpdateView):
    model = Compra
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['producto', 'fecha', 'precio', 'proveedor', 'cantidad', 'unidad']
    success_url = '/apps/compras/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/compras/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Compra'
        return context


from django.shortcuts import render

# Create your views here.

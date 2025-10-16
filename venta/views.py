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


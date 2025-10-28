from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Proveedor


class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'modulos/proveedor.html'
    context_object_name = 'proveedores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Proveedores'
        return context


class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = 'forms/formulario_crear.html'
    fields = ['nit', 'nombre']

    def get_success_url(self):
        return reverse_lazy('apl:proveedor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Proveedor'
        context['modulo'] = "proveedor"
        return context


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nit', 'nombre']

    def get_success_url(self):
        return reverse_lazy('apl:proveedor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Proveedor'
        return context


class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:proveedor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Proveedor'
        return context

# Create your views here.

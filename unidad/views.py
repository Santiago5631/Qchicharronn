from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from unidad.models import Unidad

class UnidadListView(ListView):
    model = Unidad
    template_name = 'modulos/unidad.html'
    context_object_name = 'unidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Unidades'
        return context


class UnidadCreateView(CreateView):
    model = Unidad
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'descripcion']

    def get_success_url(self):
        return reverse_lazy('apl:unidad:unidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Unidad'
        context['modulo'] = "unidad"
        return context


class UnidadUpdateView(UpdateView):
    model = Unidad
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'descripcion']

    def get_success_url(self):
        return reverse_lazy('apl:unidad:unidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Unidad'
        return context


class UnidadDeleteView(DeleteView):
    model = Unidad
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:unidad:unidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Unidad'
        return context


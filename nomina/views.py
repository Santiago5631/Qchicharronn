from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Nomina


class NominaListView(ListView):
    model = Nomina
    template_name = 'modulos/nomina.html'
    context_object_name = 'nominas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Nómina'
        return context


class NominaCreateView(CreateView):
    model = Nomina
    template_name = 'forms/formulario_crear.html'
    fields = ['empleado', 'nombre', 'valor_hora', 'pago', 'admin']

    def get_success_url(self):
        return reverse_lazy('apl:nomina_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nómina'
        context['modulo'] = "nomina"
        return context


class NominaUpdateView(UpdateView):
    model = Nomina
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['empleado', 'nombre', 'valor_hora', 'pago', 'admin']

    def get_success_url(self):
        return reverse_lazy('apl:nomina_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Nómina'
        return context


class NominaDeleteView(DeleteView):
    model = Nomina
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:nomina_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Nómina'
        return context

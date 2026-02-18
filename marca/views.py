from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render


def listar_marca(request):
    data = {
        'marca': 'marca',
        'titulo': 'Lista de Marcas',
        'marcas': Marca.objects.all()
    }
    return render(request, 'modulos/marca.html', data)


class MarcaListView(ListView):
    model = Marca
    template_name = 'modulos/marca.html'
    context_object_name = 'marcas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Marcas'
        context['marca'] = 'marca'
        return context


class MarcaUpdateView(UpdateView):
    model = Marca
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'descripcion', 'pais_origen']

    def get_success_url(self):
        return reverse_lazy('apl:marca:marca_list')


class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:marca:marca_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Marca'
        return context

    def get(self, request, *args, **kwargs):
        # Renderiza solo el contenido para el modal
        self.object = self.get_object()
        return render(request, self.template_name, {'object': self.object})


class MarcaCreateView(CreateView):
    model = Marca
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'descripcion', 'pais_origen']

    def get_success_url(self):
        return reverse_lazy('apl:marca:marca_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nueva Marca'
        context['modulo'] = "informe"
        return context

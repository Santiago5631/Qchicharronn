from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from models import *

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render


def listar_categoria(request):
    data = {
        'categoria': 'categoria',
        'titulo': 'Lista de Categorías',
        'categorias': Categoria.objects.all()
    }
    return render(request, 'modulos/categoria.html', data)


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'modulos/categoria.html'
    context_object_name = 'categorias'
    success_url = reverse_lazy('apl:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Categorías'
        context['categoria'] = 'categoria'
        return context


class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'descripcion']

    def get_success_url(self):
        return reverse_lazy('apl:listar_categoria')


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categoría'
        return context

    def get(self, request, *args, **kwargs):
        # Renderiza solo el contenido para el modal
        self.object = self.get_object()
        return render(request, self.template_name, {'object': self.object})


class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'descripcion']

    def get_success_url(self):
        return reverse_lazy('apl:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nueva Categoría'
        context['modulo'] = "categoria"
        return context


# categoria/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CategoriaForm

from usuario.permisos import RolRequeridoMixin, SOLO_ADMIN


class CategoriaListView(RolRequeridoMixin, ListView):
    """Solo administradores pueden ver las categorías."""
    roles_permitidos = SOLO_ADMIN
    model = Categoria
    template_name = 'modulos/categoria.html'
    context_object_name = 'categorias'
    success_url = reverse_lazy('apl:categoria:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Categorías'
        context['categoria'] = 'categoria'
        return context


class CategoriaCreateView(RolRequeridoMixin, CreateView):
    """Solo administradores pueden crear categorías."""
    roles_permitidos = SOLO_ADMIN
    model = Categoria
    form_class = CategoriaForm
    template_name = 'forms/formulario_crear.html'
    success_url = reverse_lazy('apl:categoria:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nueva Categoría'
        context['modulo'] = 'categoria'
        return context


class CategoriaUpdateView(RolRequeridoMixin, UpdateView):
    """Solo administradores pueden editar categorías."""
    roles_permitidos = SOLO_ADMIN
    model = Categoria
    form_class = CategoriaForm
    template_name = 'forms/formulario_actualizacion.html'
    success_url = reverse_lazy('apl:categoria:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Categoría: {self.object.nombre}'
        context['modulo'] = 'categoria'
        return context


class CategoriaDeleteView(RolRequeridoMixin, DeleteView):
    """Solo administradores pueden eliminar categorías."""
    roles_permitidos = SOLO_ADMIN
    model = Categoria
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:categoria:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categoría'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, self.template_name, {'object': self.object})
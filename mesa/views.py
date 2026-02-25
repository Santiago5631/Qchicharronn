# mesa/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Mesa
from .forms import MesaForm

from usuario.permisos import RolRequeridoMixin, ADMIN_MESERO
# ADMIN_MESERO = ['administrador', 'mesero']
# Los cocineros no gestionan mesas


class MesaListView(RolRequeridoMixin, ListView):
    """Admin y Meseros pueden ver mesas."""
    roles_permitidos = ADMIN_MESERO
    model = Mesa
    template_name = 'modulos/mesa.html'
    context_object_name = 'mesa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Mesas'
        return context


class MesaCreateView(RolRequeridoMixin, CreateView):
    """Solo administradores pueden CREAR mesas."""
    roles_permitidos = ['administrador']
    model = Mesa
    form_class = MesaForm
    template_name = 'forms/formulario_crear.html'
    success_url = reverse_lazy('apl:mesa:mesa_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Mesa'
        context['modulo'] = 'mesa'
        context['boton']  = 'Guardar'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Mesa creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrige los errores en el formulario.')
        return super().form_invalid(form)


class MesaUpdateView(RolRequeridoMixin, UpdateView):
    """Solo administradores pueden EDITAR mesas."""
    roles_permitidos = ['administrador']
    model = Mesa
    form_class = MesaForm
    template_name = 'forms/formulario_actualizacion.html'
    success_url = reverse_lazy('apl:mesa:mesa_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Mesa'
        context['modulo'] = 'mesa'
        context['boton']  = 'Actualizar'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Mesa actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrige los errores en el formulario.')
        return super().form_invalid(form)


class MesaDeleteView(RolRequeridoMixin, DeleteView):
    """Solo administradores pueden ELIMINAR mesas."""
    roles_permitidos = ['administrador']
    model = Mesa
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:mesa:mesa_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']  = 'Eliminar Mesa'
        context['modulo']  = 'mesa'
        context['objeto']  = self.object
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Mesa eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
# unidad/views.py
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from unidad.models import Unidad
from unidad.forms import UnidadForm

from usuario.permisos import RolRequeridoMixin, SOLO_ADMIN


class UnidadListView(RolRequeridoMixin, ListView):
    """Solo administradores pueden ver unidades."""
    roles_permitidos = SOLO_ADMIN
    model = Unidad
    template_name = 'modulos/unidad.html'
    context_object_name = 'unidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Unidades'
        return context


class UnidadCreateView(RolRequeridoMixin, CreateView):
    """Solo administradores pueden crear unidades."""
    roles_permitidos = SOLO_ADMIN
    model = Unidad
    template_name = 'forms/formulario_crear.html'
    form_class = UnidadForm

    def get_success_url(self):
        return reverse_lazy('apl:unidad:unidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Unidad'
        context['modulo'] = "unidad"
        return context


class UnidadUpdateView(RolRequeridoMixin, UpdateView):
    """Solo administradores pueden editar unidades."""
    roles_permitidos = SOLO_ADMIN
    model = Unidad
    template_name = 'forms/formulario_actualizacion.html'
    form_class = UnidadForm

    def get_success_url(self):
        return reverse_lazy('apl:unidad:unidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Unidad'
        return context


class UnidadDeleteView(RolRequeridoMixin, DeleteView):
    """Solo administradores pueden eliminar unidades."""
    roles_permitidos = SOLO_ADMIN
    model = Unidad
    template_name = 'forms/confirmar_eliminacion.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('apl:unidad:unidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Unidad'
        return context
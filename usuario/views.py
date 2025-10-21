from django.shortcuts import render
from django.urls import reverse_lazy
from usuario.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render


def prueba(request):
    data = {
        'usuario': 'usuario',
        'titulo': 'lista de Usuarios',
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'modulos/usuarios.html', data)


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'modulos/usuarios.html'
    context_object_name = 'usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de usuarios'
        context['usuario'] = 'usuario'
        return context


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'cedula', 'cargo', 'correo_electronico', 'numero_celular', 'estado', 'contraseña']

    def get_success_url(self):
        return reverse_lazy('apl:usuario_list')


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar usuario'
        return context

    def get(self, request, *args, **kwargs):
        # Renderiza solo el contenido para el modal
        self.object = self.get_object()
        return render(request, self.template_name, {'object': self.object})


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'cedula', 'cargo', 'correo_electronico', 'numero_celular', 'estado', 'contraseña']

    def get_success_url(self):
        return reverse_lazy('apl:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo usuario'
        context['modulo'] = "usuario"
        return context


from django.shortcuts import render

# Create your views here.

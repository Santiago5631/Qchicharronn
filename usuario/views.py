from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from usuario.models import Usuario


# Vista de prueba (puedes mantenerla o eliminarla)
def prueba(request):
    data = {
        'usuario': 'usuario',
        'titulo': 'Lista de Usuarios',
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'modulos/usuarios.html', data)


# Lista de usuarios (está bien, solo actualizo el contexto si hace falta)
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'modulos/usuarios.html'
    context_object_name = 'usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de usuarios'
        context['usuario'] = 'usuario'
        return context


# Creación de usuario (formulario corregido)
class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'forms/formulario_crear.html'
    fields = [
        'nombre', 'cedula', 'cargo', 'email',  # ← email en vez de correo_electronico
        'numero_celular', 'estado'
    ]  # NO incluimos contraseña aquí

    def get_success_url(self):
        return reverse_lazy('apl:usuario:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo usuario'
        context['modulo'] = "usuario"
        return context

    def form_valid(self, form):
        # Creamos el usuario con contraseña encriptada
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')  # si agregas campo temporal en form
        if password:
            user.set_password(password)  # encripta la contraseña
        user.save()
        return super().form_valid(form)


# Actualización de usuario (sin tocar contraseña)
class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'forms/formulario_actualizacion.html'
    fields = [
        'nombre', 'cedula', 'cargo', 'email',
        'numero_celular', 'estado'
    ]  # NO incluimos contraseña

    def get_success_url(self):
        return reverse_lazy('apl:usuario:usuario_list')


# Eliminación (está bien, pero ajusto contexto si quieres)
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:usuario:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar usuario'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, self.template_name, {'object': self.object})
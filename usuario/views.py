# usuario/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from .forms import CustomPasswordResetForm
from .models import Usuario
from .utils import generar_password
from usuario.permisos import RolRequeridoMixin, SOLO_ADMIN


# ══════════════════════════════════════════════
# LISTA DE USUARIOS — Solo administradores
# ══════════════════════════════════════════════
class UsuarioListView(RolRequeridoMixin, ListView):
    """Solo administradores pueden ver la lista de usuarios."""
    roles_permitidos = SOLO_ADMIN
    model = Usuario
    template_name = 'modulos/usuarios.html'
    context_object_name = 'usuarios'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']  = 'Lista de usuarios'
        context['usuario'] = 'usuario'
        return context


# ══════════════════════════════════════════════
# CREAR USUARIO — Solo administradores
# ══════════════════════════════════════════════
class UsuarioCreateView(RolRequeridoMixin, CreateView):
    """Solo administradores pueden crear usuarios."""
    roles_permitidos = SOLO_ADMIN
    model = Usuario
    template_name = 'forms/formulario_crear.html'
    login_url = '/login/'

    fields = [
        'nombre',
        'cedula',
        'cargo',
        'email',
        'numero_celular',
        'estado'
    ]

    def get_success_url(self):
        return reverse_lazy('apl:usuario:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo usuario'
        context['modulo'] = "usuario"
        return context

    def form_valid(self, form):
        password_temporal = generar_password()
        user = form.save(commit=False)
        user.set_password(password_temporal)
        user.save()

        try:
            send_mail(
                subject="Tu cuenta ha sido creada",
                message=f"""
Hola {user.nombre},

Tu cuenta fue creada correctamente.

Usuario: {user.email}
Contraseña temporal: {password_temporal}

Puedes iniciar sesión aquí:
http://127.0.0.1:8000/login/

Te recomendamos cambiar tu contraseña después de ingresar.
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print("Error enviando correo:", e)

        self.object = user
        return super().form_valid(form)


# ══════════════════════════════════════════════
# ACTUALIZAR USUARIO — Solo administradores
# ══════════════════════════════════════════════
class UsuarioUpdateView(RolRequeridoMixin, UpdateView):
    """Solo administradores pueden editar usuarios."""
    roles_permitidos = SOLO_ADMIN
    model = Usuario
    template_name = 'forms/formulario_actualizacion.html'
    login_url = '/login/'

    fields = [
        'nombre',
        'cedula',
        'cargo',
        'email',
        'numero_celular',
        'estado'
    ]

    def get_success_url(self):
        return reverse_lazy('apl:usuario:usuario_list')


# ══════════════════════════════════════════════
# ELIMINAR USUARIO — Solo administradores
# ══════════════════════════════════════════════
class UsuarioDeleteView(RolRequeridoMixin, View):
    """Solo administradores pueden eliminar usuarios."""
    roles_permitidos = SOLO_ADMIN
    login_url = '/login/'

    def post(self, request, pk, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                usuario = get_object_or_404(Usuario, pk=pk)
                usuario.delete()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        return JsonResponse({'success': False}, status=400)


# ══════════════════════════════════════════════
# PASSWORD RESET — Accesible sin restricción de rol
# (el usuario ya está autenticado cuando llega aquí)
# ══════════════════════════════════════════════
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'
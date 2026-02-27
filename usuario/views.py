# usuario/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages

from .forms import CustomPasswordResetForm, PerfilForm, CambiarPasswordForm
from .models import Usuario
from .utils import generar_password
from usuario.permisos import RolRequeridoMixin, SOLO_ADMIN


# ══════════════════════════════════════════════
# LISTA DE USUARIOS — Solo administradores
# ══════════════════════════════════════════════
class UsuarioListView(RolRequeridoMixin, ListView):
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
    roles_permitidos = SOLO_ADMIN
    model = Usuario
    template_name = 'forms/formulario_crear.html'
    login_url = '/login/'
    fields = ['nombre', 'cedula', 'cargo', 'email', 'numero_celular', 'estado']

    def get_success_url(self):
        return reverse_lazy('apl:usuario:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo usuario'
        context['modulo'] = 'usuario'
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
    roles_permitidos = SOLO_ADMIN
    model = Usuario
    template_name = 'forms/formulario_actualizacion.html'
    login_url = '/login/'
    fields = ['nombre', 'cedula', 'cargo', 'email', 'numero_celular', 'estado']

    def get_success_url(self):
        return reverse_lazy('apl:usuario:usuario_list')


# ══════════════════════════════════════════════
# ELIMINAR USUARIO — Solo administradores
# ══════════════════════════════════════════════
class UsuarioDeleteView(RolRequeridoMixin, View):
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
# RESET DE CONTRASEÑA POR ADMIN
# ══════════════════════════════════════════════
class UsuarioResetPasswordView(RolRequeridoMixin, View):
    roles_permitidos = SOLO_ADMIN

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        password_temporal = generar_password()
        usuario.set_password(password_temporal)
        usuario.save()

        try:
            send_mail(
                subject="Restablecimiento de contraseña",
                message=f"""
Hola {usuario.nombre},

Tu contraseña fue restablecida por el administrador.

Usuario: {usuario.email}
Nueva contraseña temporal: {password_temporal}

Puedes iniciar sesión aquí:
http://127.0.0.1:8000/login/

Te recomendamos cambiar tu contraseña después de ingresar.
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
                fail_silently=False,
            )
            messages.success(request, f'Contraseña restablecida y enviada a {usuario.email}')
        except Exception as e:
            messages.error(request, f'Error al enviar correo: {str(e)}')

        return redirect('apl:usuario:usuario_list')


# ══════════════════════════════════════════════
# PERFIL PROPIO — Cualquier usuario autenticado
# Cada usuario puede ver y editar su propio perfil
# ══════════════════════════════════════════════
class PerfilView(LoginRequiredMixin, View):
    """Vista del perfil propio del usuario."""
    template_name = 'usuario/perfil.html'
    login_url = '/login/'

    def get(self, request):
        form_perfil   = PerfilForm(instance=request.user)
        form_password = CambiarPasswordForm(user=request.user)
        context = {
            'titulo':        'Mi Perfil',
            'form_perfil':   form_perfil,
            'form_password': form_password,
            'usuario':       request.user,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        accion = request.POST.get('accion')

        # ── Actualizar datos del perfil ──
        if accion == 'actualizar_perfil':
            form_perfil = PerfilForm(
                request.POST,
                request.FILES,
                instance=request.user
            )
            form_password = CambiarPasswordForm(user=request.user)

            if form_perfil.is_valid():
                form_perfil.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('apl:usuario:perfil')
            else:
                messages.error(request, 'Por favor corrige los errores.')

        # ── Cambiar contraseña ──
        elif accion == 'cambiar_password':
            form_perfil   = PerfilForm(instance=request.user)
            form_password = CambiarPasswordForm(
                user=request.user,
                data=request.POST
            )

            if form_password.is_valid():
                user = form_password.save()
                # Mantener la sesión activa después del cambio
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña cambiada correctamente.')
                return redirect('apl:usuario:perfil')
            else:
                messages.error(request, 'Por favor corrige los errores.')

        else:
            form_perfil   = PerfilForm(instance=request.user)
            form_password = CambiarPasswordForm(user=request.user)

        context = {
            'titulo':        'Mi Perfil',
            'form_perfil':   form_perfil,
            'form_password': form_password,
            'usuario':       request.user,
        }
        return render(request, self.template_name, context)


# ══════════════════════════════════════════════
# PASSWORD RESET — Accesible sin restricción de rol
# ══════════════════════════════════════════════
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'


# ══════════════════════════════════════════════
# ACCIÓN DE EMERGENCIA: Resetear clave desde la lista
# ══════════════════════════════════════════════
# Asegúrate de que el nombre sea exactamente este:
class Administradorresetpasword(RolRequeridoMixin, View):
    roles_permitidos = SOLO_ADMIN

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        password_temporal = generar_password()  # Tu función que ya tienes
        usuario.set_password(password_temporal)
        usuario.save()

        try:
            # Enviar el correo usando tu configuración de Gmail
            send_mail(
                subject="Cambio de contraseña - Q'Chicharrón",
                message=f"Hola {usuario.nombre},\n\nUn administrador ha generado una nueva contraseña para tu cuenta.\n\nContraseña: {password_temporal}\n\nIngresa aquí: http://127.0.0.1:8000/login/",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
                fail_silently=False,
            )

            # Devolvemos el JSON que el JavaScript está esperando
            return JsonResponse({
                'success': True,
                'message': f'Contraseña de {usuario.nombre} actualizada correctamente.',
                'password_visible': password_temporal
            })
        except Exception as e:
            # Si falla el correo (por internet o SMTP), igual devolvemos la clave al admin
            return JsonResponse({
                'success': True,
                'message': 'Contraseña cambiada, pero hubo un problema enviando el correo.',
                'password_visible': password_temporal,
                'error': str(e)
            })
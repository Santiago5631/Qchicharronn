from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .forms import CustomPasswordResetForm
from .models import Usuario
from .utils import generar_password


# ===============================
# Vista de prueba (opcional)
# ===============================
def prueba(request):
    data = {
        'usuario': 'usuario',
        'titulo': 'Lista de Usuarios',
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'modulos/usuarios.html', data)


# ===============================
# LISTA DE USUARIOS
# ===============================
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'modulos/usuarios.html'
    context_object_name = 'usuarios'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de usuarios'
        context['usuario'] = 'usuario'
        return context


# ===============================
# CREAR USUARIO
# ===============================
class UsuarioCreateView(LoginRequiredMixin, CreateView):
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
        # 🔥 Generar contraseña temporal
        password_temporal = generar_password()

        # Crear usuario sin guardar todavía
        user = form.save(commit=False)

        # Encriptar contraseña correctamente
        user.set_password(password_temporal)

        user.save()

        # 🔥 Enviar correo
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

# ===============================
# ACTUALIZAR USUARIO
# ===============================
class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
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


# ===============================
# ELIMINAR USUARIO (AJAX)
# ===============================
class UsuarioDeleteView(LoginRequiredMixin, View):
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


# ===============================
# PASSWORD RESET PERSONALIZADO
# ===============================
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'

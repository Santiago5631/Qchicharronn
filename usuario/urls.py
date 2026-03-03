# usuario/urls.py
from django.urls import path
from usuario.views import (
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,
    UsuarioResetPasswordView,
    PerfilView, Administradorresetpasword
)
from .views import CustomPasswordResetView

app_name = 'usuario'

urlpatterns = [
    # ── Gestión de usuarios (solo admin) ──
    path('listar/',                          UsuarioListView.as_view(),         name='usuario_list'),
    path('crear/',                           UsuarioCreateView.as_view(),       name='crear_usuario'),
    path('editar/<int:pk>/',                 UsuarioUpdateView.as_view(),       name='editar_usuario'),
    path('eliminar/<int:pk>/',               UsuarioDeleteView.as_view(),       name='eliminar_usuario'),
    path('reset-password/<int:pk>/',         UsuarioResetPasswordView.as_view(), name='usuario_reset_password'),

    # ── Perfil propio (cualquier usuario autenticado) ──
    path('perfil/',                          PerfilView.as_view(),              name='perfil'),

    # ── Reset de contraseña por email ──
    path('accounts/password/reset/',         CustomPasswordResetView.as_view(), name='password_reset'),
    #-------cuando el administrador cambia la contraseña----
path('forzar-reset/<int:pk>/', Administradorresetpasword.as_view(), name='admin_forzar_reset'),
]
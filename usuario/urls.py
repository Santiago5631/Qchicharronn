from django.urls import path
from usuario.views import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView
from .views import CustomPasswordResetView

app_name = 'usuario'
urlpatterns = [
    path('accounts/password/reset/',CustomPasswordResetView.as_view(), name='password_reset'),
    path('listar/', UsuarioListView.as_view(), name='usuario_list'),
    path('editar/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
]
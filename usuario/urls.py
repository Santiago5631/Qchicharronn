from django.urls import path
from usuario.views import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView

urlpatterns = [
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
]
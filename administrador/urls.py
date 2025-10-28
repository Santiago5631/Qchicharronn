from administrador.views import *
from django.urls import path

app_name = 'administrador'
urlpatterns = [

    # -------------------- Administrador --------------------
    path('listar/', AdministradorListView.as_view(), name='administrador_list'),
    path('crear/', AdministradorCreateView.as_view(), name='crear_administrador'),
    path('editar/<int:pk>/', AdministradorUpdateView.as_view(), name='editar_administrador'),
    path('eliminar/<int:pk>/', AdministradorDeleteView.as_view(), name='eliminar_administrador'),
]

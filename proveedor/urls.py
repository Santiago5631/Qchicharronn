from proveedor.views import *
from django.urls import path

app_name = 'proveedor'

urlpatterns = [
    path('listar/', ProveedorListView.as_view(), name='proveedor_list'),
    path('crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),
]
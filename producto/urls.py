from producto.views import *
from django.urls import path

urlpatterns = [
    path('listar/', ProductoListView.as_view(), name='producto_list'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('editar/<str:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('eliminar/<str:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
]
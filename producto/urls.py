from producto import views
from producto.views import *
from django.urls import path

app_name = 'producto'

urlpatterns = [
    path('listar/', ProductoListView.as_view(), name='producto_list'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('editar/<str:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('eliminar/<str:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),

    # Rutas AJAX
    path('ajax/crear_marca/', views.crear_marca_ajax, name='crear_marca_ajax'),
    path('ajax/crear_categoria/', views.crear_categoria_ajax, name='crear_categoria_ajax'),
    path('ajax/crear_proveedor/', views.crear_proveedor_ajax, name='crear_proveedor_ajax'),
    path('ajax/crear_proveedor/', views.crear_unidad_ajax, name='crear_unidad_ajax'),
]
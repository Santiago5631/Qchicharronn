from django.urls import path,include
from plato.views import *

app_name = 'plato'
urlpatterns = [

path('listar/', PlatoListView.as_view(), name='listar_plato'),
path('crear/', PlatoCreateView.as_view(), name='crear_plato'),
path('editar/<int:pk>/', PlatoUpdateView.as_view(), name='editar_plato'),
path('eliminar/<int:pk>/', PlatoDeleteView.as_view(), name='eliminar_plato'),
path('ajax/agregar_producto/', agregar_producto_ajax, name='agregar_producto_ajax'),
]
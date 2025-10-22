from django.urls import path,include
from pedido.views import *

urlpatterns = [
    path('pedidos/listar/', PedidoListView.as_view(), name='listar_pedido'),
    path('pedidos/crear/', PedidoCreateView.as_view(), name='crear_pedido'),
    path('pedidos/editar/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('pedidos/eliminar/<int:pk>/', PedidoDeleteView.as_view(), name='eliminar_pedido'),
]
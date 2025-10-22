from django.urls import path,include
from pedido.views import *

urlpatterns = [
    path('listar/', PedidoListView.as_view(), name='listar_pedido'),
    path('crear/', PedidoCreateView.as_view(), name='crear_pedido'),
    path('editar/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('eliminar/<int:pk>/', PedidoDeleteView.as_view(), name='eliminar_pedido'),
]
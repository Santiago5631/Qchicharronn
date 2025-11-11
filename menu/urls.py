from menu.views import *
from django.urls import path

app_name = 'menu'

urlpatterns = [
    # URLs de Menú
    path('listar/', MenuListView.as_view(), name='menu_list'),
    path('crear/', MenuCreateView.as_view(), name='menu_create'),
    path('actualizar/<int:pk>/', MenuUpdateView.as_view(), name='menu_update'),
    path('eliminar/<int:pk>/', MenuDeleteView.as_view(), name='menu_delete'),
    path('detalle/<int:pk>/', MenuDetailView.as_view(), name='menu_detail'),

    # URLs de Pedidos
    path('pedidos/listar/', PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/crear/', PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/detalle/<int:pk>/', PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedidos/actualizar-estado/<int:pk>/', PedidoUpdateEstadoView.as_view(), name='pedido_update_estado'),
    path('pedidos/cancelar/<int:pk>/', PedidoDeleteView.as_view(), name='pedido_delete'),
    path('pedidos/limpiar-carrito/', LimpiarCarritoView.as_view(), name='limpiar_carrito'),
]
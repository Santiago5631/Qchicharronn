from django.urls import path,include
from pedido import views
from pedido.views import *

app_name = 'pedido'
urlpatterns = [
    path('listar/', PedidoListView.as_view(), name='listar_pedido'),
    path('crear/', PedidoCreateView.as_view(), name='crear_pedido'),
    path('editar/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('eliminar/<int:pk>/', PedidoDeleteView.as_view(), name='eliminar_pedido'),
    path('comanda/parrilla/<int:pk>/', views.comanda_parrilla, name='comanda_parrilla'),
    path('comanda/cocina/<int:pk>/', views.comanda_cocina, name='comanda_cocina'),
]
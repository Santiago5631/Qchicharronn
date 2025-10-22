from django.urls import path,include
import categoria
import empleado
import pedido
import plato
import usuario
from mesa.views import *
from menu.views import *
from categoria.views import *
from marca.views import *
from . import views
from proyecto_principal import views

app_name = 'proyecto_principal'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # -------------------- Mesa --------------------
    path('mesas/', MesaListView.as_view(), name='mesa_list'),
    path('mesas/crear/', MesaCreateView.as_view(), name='crear_mesa'),
    path('mesas/editar/<int:pk>/', MesaUpdateView.as_view(), name='editar_mesa'),
    path('mesas/eliminar/<int:pk>/', MesaDeleteView.as_view(), name='eliminar_mesa'),

    # -------------------- Menú --------------------
    path('menus/listar/', MenuListView.as_view(), name='menu_list'),
    path('menus/crear/', MenuCreateView.as_view(), name='menu_create'),
    path('menus/actualizar/<int:pk>/', MenuUpdateView.as_view(), name='menu_update'),
    path('menus/eliminar/<int:pk>/', MenuDeleteView.as_view(), name='menu_delete'),

    # -------------------- Categoría --------------------
    path('categorias/listar/', CategoriaListView.as_view(), name='listar_categoria'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),

    # -------------------- Marca --------------------
    path('marcas/listar/', MarcaListView.as_view(), name='marca_list'),
    path('marcas/crear/', MarcaCreateView.as_view(), name='marca_create'),
    path('marcas/actualizar/<int:pk>/', MarcaUpdateView.as_view(), name='marca_update'),
    path('marcas/eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_delete'),

    # _________________________ Modulos de Usuario __________________________
    path('usuarios/', include(usuario.urls), name='usuario_list'),

    # _________________________ Modulos de Plato __________________________
    path('platos/listar/', include(plato.urls), name='listar_plato'),

    # _________________________ Modulos de Pedido __________________________
    path('pedidos/listar/', include(pedido.urls), name='listar_pedido'),
    # _________________________ Modulos de Empleado __________________________
    path('empleados/listar/', include(empleado.urls), name='listar_empleado'),
]

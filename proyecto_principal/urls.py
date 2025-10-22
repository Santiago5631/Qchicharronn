from django.urls import path,include
import empleado
import pedido
import plato
import usuario
from proyecto_principal import views

app_name = 'proyecto_principal'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #-------------- Mesa ----------------------
    path('mesas/', include('mesa.urls', namespace='mesa')),
    #---------------- Menus ---------------------------
    path('menus/', include('menu.urls', namespace='menu')),
    #----------------- Categoria ------------------
    path('categorias/', include('categoria.urls', namespace='categoria')),
    #------------------ Marca ------------------------------
    path('marcas/', include('marca.urls', namespace='marca')),
    # _________________________ Modulos de Usuario __________________________
    path('usuarios/', include(usuario.urls), name='usuario_list'),
    # _________________________ Modulos de Plato __________________________
    path('platos/listar/', include(plato.urls), name='listar_plato'),
    # _________________________ Modulos de Pedido __________________________
    path('pedidos/listar/', include(pedido.urls), name='listar_pedido'),
    # _________________________ Modulos de Empleado __________________________
    path('empleados/listar/', include(empleado.urls), name='listar_empleado'),
]

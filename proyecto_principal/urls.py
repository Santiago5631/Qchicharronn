from django.urls import path,include
import empleado
import pedido
import plato
import usuario
import compra
import venta
import administrador
import informe
from proyecto_principal import views

app_name = 'apl'

urlpatterns = [
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
    path('usuarios/', include(("usuario.urls", 'usuario'), namespace='usuario')),
    # _________________________ Modulos de Plato __________________________
    path('platos/', include(("plato.urls", 'plato'), namespace='plato')),
    # _________________________ Modulos de Pedido __________________________
    path('pedidos/', include(("pedido.urls", 'pedido'), namespace='pedido')),
    # _________________________ Modulos de Empleado __________________________
    path('empleados/', include(('empleado.urls', 'empleado'), namespace='empleado')),
    path('empleados/', include("empleado.urls"), name='listar_empleado'),

    # -------------------- Compra --------------------
    path('compras/', include('compra.urls', namespace='compra')),

    # -------------------- Venta --------------------
    path('ventas/', include('venta.urls', namespace='venta')),

    # -------------------- Administrador --------------------
    path('administradores/', include('administrador.urls', namespace='administrador')),

    # -------------------- Informe --------------------
    path('informes/', include('informe.urls', namespace='informe')),
]

from django.urls import path,include
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
    path('usuarios/', include("usuario.urls"), name='usuario'),
    # _________________________ Modulos de Plato __________________________
    path('platos/', include("plato.urls"), name='plato'),
    # _________________________ Modulos de Pedido __________________________
    path('pedidos/', include("pedido.urls"), name='pedido'),
    # _________________________ Modulos de Empleado __________________________
    path('empleados/', include("empleado.urls"), name='empleado'),
    #---------------------------Modulo de Producto ----------------------------
    path('producto/', include("producto.urls"), name='producto'),
    #----------------------------Modulo de proveedor ---------------------------
    path('proveedor/', include("proveedor.urls"), name='proveedor'),

]

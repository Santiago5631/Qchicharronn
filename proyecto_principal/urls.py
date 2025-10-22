from django.urls import path,include
import categoria
from mesa.views import *
from menu.views import *
from categoria.views import *
from marca.views import *
from proyecto_principal import views

app_name = 'proyecto_principal'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', include('proyecto_principal.urls')),
    path('mesas/', include('mesa.urls', namespace='mesa')),
    path('menus/', include('menu.urls', namespace='menu')),
    path('categorias/', include('categoria.urls', namespace='categoria')),
    path('marcas/', include('marca.urls', namespace='marca')),
]

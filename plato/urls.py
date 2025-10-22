from django.urls import path,include
from plato.views import *

urlpatterns = [

path('listar/', PlatoListView.as_view(), name='listar_plato'),
path('crear/', PlatoCreateView.as_view(), name='crear_plato'),
path('editar/', PlatoUpdateView.as_view(), name='editar_plato'),
path('eliminar/', PlatoDeleteView.as_view(), name='eliminar_plato'),

]
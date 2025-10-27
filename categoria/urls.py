from django.urls import path,include
from categoria.views import *

app_name = 'categoria'



urlpatterns =[
    path('listar/', CategoriaListView.as_view(), name='listar_categoria'),
    path('crear/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
]
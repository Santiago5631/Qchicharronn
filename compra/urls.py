from compra.views import *
from django.urls import path

app_name = 'compra'
urlpatterns = [

    # -------------------- Compra --------------------
    path('listar/', CompraListView.as_view(), name='compra_list'),
    path('crear/', CompraCreateView.as_view(), name='crear_compra'),
    path('editar/<int:pk>/', CompraUpdateView.as_view(), name='editar_compra'),
    path('eliminar/<int:pk>/', CompraDeleteView.as_view(), name='eliminar_compra'),
]

from venta.views import *
from django.urls import path

app_name = 'venta'
urlpatterns = [

    # -------------------- Venta --------------------
    path('listar/', VentaListView.as_view(), name='venta_list'),
    path('crear/', VentaCreateView.as_view(), name='crear_venta'),
    path('editar/<int:pk>/', VentaUpdateView.as_view(), name='editar_venta'),
    path('eliminar/<int:pk>/', VentaDeleteView.as_view(), name='eliminar_venta'),
]
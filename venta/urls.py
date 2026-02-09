from venta.views import *
from django.urls import path

app_name = 'venta'
urlpatterns = [

    # -------------------- Venta --------------------
    path('listar/', VentaListView.as_view(), name='venta_list'),
    path('factura/<int:pk>/', VentaFacturaView.as_view(), name='factura'),
    ]

